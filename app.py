import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.azure_openai_service import AzureOpenAIService
from services.npc_storage_service import NPCStorageService
from models.npc import NPCGenerationRequest

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize services
openai_service = AzureOpenAIService()
storage_service = NPCStorageService()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "zenith-npc-generator-service",
        "version": "1.0.0"
    })


@app.route('/generate-npc', methods=['POST'])
def generate_single_npc():
    """Generate a single NPC"""
    
    try:
        data = request.get_json() or {}
        
        # Extract optional parameters
        species_preference = data.get('species_preference')
        district_preference = data.get('district_preference')
        age_range = data.get('age_range')
        
        # Generate NPC
        npc = openai_service.generate_npc(
            species_preference=species_preference,
            district_preference=district_preference,
            age_range=age_range
        )
        
        if not npc:
            return jsonify({"error": "Failed to generate NPC"}), 500
        
        # Save to MongoDB
        npc_id = storage_service.save_npc(npc)
        
        return jsonify({
            "success": True,
            "npc": npc.model_dump(),
            "saved_to": npc_id
        })
        
    except Exception as e:
        logger.error(f"Error in generate_single_npc: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/generate-npcs', methods=['POST'])
def generate_multiple_npcs():
    """Generate multiple NPCs"""
    
    try:
        data = request.get_json() or {}
        request_model = NPCGenerationRequest(**data)
        
        # Generate NPCs
        npcs = openai_service.generate_multiple_npcs(
            count=request_model.count,
            species_preference=request_model.species_preference,
            district_preference=request_model.district_preference,
            age_range=request_model.age_range
        )
        
        if not npcs:
            return jsonify({"error": "Failed to generate any NPCs"}), 500
        
        # Save NPCs individually and as a collection
        individual_ids = storage_service.save_npcs_batch(npcs)
        collection_id = storage_service.save_npcs_collection(npcs)
        
        return jsonify({
            "success": True,
            "generated_count": len(npcs),
            "requested_count": request_model.count,
            "npcs": [npc.model_dump() for npc in npcs],
            "individual_files": individual_ids,
            "collection_file": collection_id
        })
        
    except Exception as e:
        logger.error(f"Error in generate_multiple_npcs: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/npcs', methods=['GET'])
def get_all_npcs():
    """Get all stored NPCs"""
    
    try:
        npcs = storage_service.get_all_npcs()
        return jsonify({
            "success": True,
            "count": len(npcs),
            "npcs": npcs
        })
        
    except Exception as e:
        logger.error(f"Error in get_all_npcs: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/storage-stats', methods=['GET'])
def get_storage_stats():
    """Get storage statistics"""
    
    try:
        stats = storage_service.get_storage_stats()
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"Error in get_storage_stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
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
    
    logger.info("Starting Zenith NPC Generator Service...")
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')