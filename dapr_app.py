import os
import json
import logging
import uuid
from typing import Dict, Any
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from dapr.clients import DaprClient

# Import protobuf classes
from npc_pb2 import (
    NPC, NPCGenerationRequest, NPCGenerationResponse, 
    GenerateNPCTopicMessage, NPCGenerationTopicResponse
)

# Import existing services
from services.azure_openai_service import AzureOpenAIService
from services.npc_storage_service_pb import NPCStorageService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

import os
import json
import logging
import uuid
import asyncio
from typing import Dict, Any
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from dapr.clients import DaprClient

# Import protobuf classes
from npc_pb2 import (
    NPC, NPCGenerationRequest, NPCGenerationResponse, 
    GenerateNPCTopicMessage, NPCGenerationTopicResponse
)

# Import existing services
from services.azure_openai_service import AzureOpenAIService
from services.npc_storage_service_pb import NPCStorageService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize services lazily to avoid startup issues during import
openai_service = None
storage_service = None
dapr_client = None

def get_services():
    """Lazy initialization of services"""
    global openai_service, storage_service, dapr_client
    
    if openai_service is None:
        openai_service = AzureOpenAIService()
    if storage_service is None:
        storage_service = NPCStorageService()
    if dapr_client is None:
        dapr_client = DaprClient()
    
    return openai_service, storage_service, dapr_client

# Topic names
REQUEST_TOPIC = "npc-generation-request"
RESPONSE_TOPIC = "npc-generation-response"


@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    """Return subscription configuration for Dapr"""
    subscriptions = [
        {
            'pubsubname': 'pubsub',
            'topic': REQUEST_TOPIC,
            'route': '/npc-generation-request'
        }
    ]
    return jsonify(subscriptions)


@app.route('/npc-generation-request', methods=['POST'])
def npc_generation_request_handler():
    """Handle NPC generation requests from Dapr topic"""
    
    try:
        logger.info("Received NPC generation request")
        
        # Get services
        openai_service, storage_service, dapr_client = get_services()
        
        # Get the raw data from Dapr
        event_data = request.get_data()
        
        # Try to parse as protobuf first, fallback to JSON
        try:
            topic_message = GenerateNPCTopicMessage()
            topic_message.ParseFromString(event_data)
            logger.info("Parsed protobuf message successfully")
        except Exception as proto_error:
            logger.warning(f"Failed to parse as protobuf: {proto_error}")
            # Fallback to JSON parsing for testing
            json_data = request.get_json()
            
            # Create protobuf message from JSON
            topic_message = GenerateNPCTopicMessage()
            topic_message.request_id = json_data.get('request_id', str(uuid.uuid4()))
            topic_message.response_topic = json_data.get('response_topic', RESPONSE_TOPIC)
            
            # Build generation request
            generation_request = NPCGenerationRequest()
            generation_request.count = json_data.get('count', 1)
            if 'species_preference' in json_data:
                generation_request.species_preference = json_data['species_preference']
            if 'district_preference' in json_data:
                generation_request.district_preference = json_data['district_preference'] 
            if 'age_range' in json_data:
                generation_request.age_range = json_data['age_range']
            
            topic_message.request.CopyFrom(generation_request)
        
        # Extract request details
        request_id = topic_message.request_id
        generation_request = topic_message.request
        response_topic = topic_message.response_topic
        
        logger.info(f"Processing request ID: {request_id}")
        
        # Generate NPCs using existing service
        if generation_request.count == 1:
            npc = openai_service.generate_npc(
                species_preference=generation_request.species_preference if generation_request.HasField('species_preference') else None,
                district_preference=generation_request.district_preference if generation_request.HasField('district_preference') else None,
                age_range=generation_request.age_range if generation_request.HasField('age_range') else None
            )
            
            npcs = [npc] if npc else []
        else:
            npcs = openai_service.generate_multiple_npcs(
                count=generation_request.count,
                species_preference=generation_request.species_preference if generation_request.HasField('species_preference') else None,
                district_preference=generation_request.district_preference if generation_request.HasField('district_preference') else None,
                age_range=generation_request.age_range if generation_request.HasField('age_range') else None
            )
        
        # Convert to protobuf format and save
        if npcs:
            # Save NPCs
            individual_ids = storage_service.save_npcs_batch(npcs)
            collection_id = storage_service.save_npcs_collection(npcs) if len(npcs) > 1 else None
            
            # Convert Pydantic NPCs to protobuf NPCs  
            pb_npcs = []
            for npc in npcs:
                pb_npc = NPC()
                pb_npc.name = npc.Name
                pb_npc.age = npc.Age
                pb_npc.species = npc.Species
                pb_npc.physical_description = npc.PhysicalDescription
                pb_npc.personality_description = npc.PersonalityDescription
                pb_npc.resident_district = npc.ResidentDistrict
                pb_npcs.append(pb_npc)
            
            # Create successful response
            response = NPCGenerationResponse()
            response.success = True
            response.npcs.extend(pb_npcs)
            response.generated_count = len(npcs)
            response.requested_count = generation_request.count
            response.individual_files.extend(individual_ids)
            if collection_id:
                response.collection_file = collection_id
        else:
            # Create error response
            response = NPCGenerationResponse()
            response.success = False
            response.generated_count = 0
            response.requested_count = generation_request.count
            response.error = "Failed to generate any NPCs"
        
        # Create topic response message
        topic_response = NPCGenerationTopicResponse()
        topic_response.request_id = request_id
        topic_response.response.CopyFrom(response)
        
        # Publish response to the specified topic
        try:
            dapr_client.publish_event(
                pubsub_name='pubsub',
                topic_name=response_topic,
                data=topic_response.SerializeToString(),
                data_content_type='application/x-protobuf'
            )
            logger.info(f"Published response for request {request_id} to topic {response_topic}")
        except Exception as publish_error:
            logger.error(f"Failed to publish response: {publish_error}")
            
        return jsonify({"status": "processed", "request_id": request_id}), 200
            
    except Exception as e:
        logger.error(f"Error processing NPC generation request: {e}")
        
        # Try to send error response if we have request details
        try:
            if 'request_id' in locals() and 'response_topic' in locals():
                error_response = NPCGenerationResponse()
                error_response.success = False
                error_response.generated_count = 0
                error_response.requested_count = 0
                error_response.error = str(e)
                
                error_topic_response = NPCGenerationTopicResponse()
                error_topic_response.request_id = request_id
                error_topic_response.response.CopyFrom(error_response)
                
                dapr_client.publish_event(
                    pubsub_name='pubsub',
                    topic_name=response_topic,
                    data=error_topic_response.SerializeToString(),
                    data_content_type='application/x-protobuf'
                )
        except Exception as error_publish_error:
            logger.error(f"Failed to publish error response: {error_publish_error}")
        
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint callable via Dapr service invocation"""
    
    return jsonify({
        "status": "healthy",
        "service": "zenith-npc-generator-service",
        "version": "2.0.0",
        "dapr_enabled": True
    })


def main():
    """Main entry point"""
    
    # Validate required environment variables
    required_env_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY", 
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please copy .env.example to .env and fill in your Azure OpenAI credentials")
        exit(1)
    
    logger.info("Starting Zenith NPC Generator Service with Dapr...")
    
    # Run the Flask app (Dapr will call it)
    app.run(host='0.0.0.0', port=int(os.getenv('DAPR_APP_PORT', 50051)), debug=False)


if __name__ == '__main__':
    main()


def main():
    """Main entry point"""
    
    # Validate required environment variables
    required_env_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY", 
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please copy .env.example to .env and fill in your Azure OpenAI credentials")
        exit(1)
    
    logger.info("Starting Zenith NPC Generator Service with Dapr...")
    
    # Run the Flask app (Dapr will call it)
    app.run(host='0.0.0.0', port=int(os.getenv('DAPR_APP_PORT', 50051)), debug=False)


if __name__ == '__main__':
    main()