#!/usr/bin/env python3
"""
Example client for interacting with the Dapr-based NPC Generator Service
This demonstrates how to send requests via Dapr topics and receive responses
"""

import uuid
import asyncio
import logging
from typing import Optional
from dapr.clients import DaprClient
from npc_pb2 import (
    NPCGenerationRequest, 
    GenerateNPCTopicMessage,
    NPCGenerationTopicResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPCGeneratorClient:
    """Client for interacting with NPC Generator via Dapr topics"""
    
    def __init__(self):
        self.dapr_client = DaprClient()
        self.response_handlers = {}
    
    async def generate_npc(self, 
                          count: int = 1,
                          species_preference: Optional[str] = None,
                          district_preference: Optional[str] = None,
                          age_range: Optional[str] = None) -> dict:
        """Generate NPCs and return the result"""
        
        # Create unique request ID
        request_id = str(uuid.uuid4())
        response_topic = f"npc-generation-response-{request_id}"
        
        # Build protobuf request
        generation_request = NPCGenerationRequest()
        generation_request.count = count
        if species_preference:
            generation_request.species_preference = species_preference
        if district_preference:
            generation_request.district_preference = district_preference
        if age_range:
            generation_request.age_range = age_range
        
        # Create topic message
        topic_message = GenerateNPCTopicMessage()
        topic_message.request_id = request_id
        topic_message.request.CopyFrom(generation_request)
        topic_message.response_topic = response_topic
        
        # Set up response handler
        response_future = asyncio.Future()
        self.response_handlers[request_id] = response_future
        
        try:
            # Publish request to topic
            self.dapr_client.publish_event(
                pubsub_name='pubsub',
                topic_name='npc-generation-request',
                data=topic_message.SerializeToString(),
                data_content_type='application/x-protobuf'
            )
            
            logger.info(f"Published NPC generation request with ID: {request_id}")
            
            # Wait for response (with timeout)
            try:
                response = await asyncio.wait_for(response_future, timeout=30.0)
                return response
            except asyncio.TimeoutError:
                logger.error(f"Timeout waiting for response to request {request_id}")
                return {"error": "Timeout waiting for response"}
            
        except Exception as e:
            logger.error(f"Error sending request: {e}")
            return {"error": str(e)}
        finally:
            # Clean up response handler
            self.response_handlers.pop(request_id, None)
    
    def handle_response(self, event_data: bytes):
        """Handle incoming response from topic"""
        
        try:
            # Parse protobuf response
            topic_response = NPCGenerationTopicResponse()
            topic_response.ParseFromString(event_data)
            
            request_id = topic_response.request_id
            response = topic_response.response
            
            # Find waiting future and complete it
            if request_id in self.response_handlers:
                future = self.response_handlers[request_id]
                
                # Convert protobuf response to dict
                response_dict = {
                    "success": response.success,
                    "generated_count": response.generated_count,
                    "requested_count": response.requested_count,
                    "individual_files": list(response.individual_files),
                    "npcs": []
                }
                
                # Add collection file if present
                if response.HasField('collection_file'):
                    response_dict["collection_file"] = response.collection_file
                
                # Add error if present
                if response.HasField('error'):
                    response_dict["error"] = response.error
                
                # Convert NPCs to dict format
                for npc in response.npcs:
                    npc_dict = {
                        "Name": npc.name,
                        "Age": npc.age,
                        "Species": npc.species,
                        "PhysicalDescription": npc.physical_description,
                        "PersonalityDescription": npc.personality_description,
                        "ResidentDistrict": npc.resident_district
                    }
                    response_dict["npcs"].append(npc_dict)
                
                # Complete the future
                if not future.done():
                    future.set_result(response_dict)
                
        except Exception as e:
            logger.error(f"Error handling response: {e}")


async def main():
    """Example usage of the NPC Generator client"""
    
    client = NPCGeneratorClient()
    
    print("🎭 Testing Dapr-based NPC Generator Service")
    print("=" * 50)
    
    # Generate a single NPC
    print("\n📝 Generating single NPC...")
    result = await client.generate_npc(
        count=1,
        species_preference="Elf",
        district_preference="Mystic Gardens"
    )
    
    if result.get("success"):
        print(f"✅ Generated {result['generated_count']} NPC(s)")
        for npc in result.get("npcs", []):
            print(f"   - {npc['Name']} (Age {npc['Age']}, {npc['Species']})")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Generate multiple NPCs
    print("\n📝 Generating multiple NPCs...")
    result = await client.generate_npc(
        count=2,
        species_preference="Human"
    )
    
    if result.get("success"):
        print(f"✅ Generated {result['generated_count']} NPC(s)")
        for npc in result.get("npcs", []):
            print(f"   - {npc['Name']} (Age {npc['Age']}, {npc['Species']})")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Test completed!")


if __name__ == "__main__":
    asyncio.run(main())