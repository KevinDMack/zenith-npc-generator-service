import os
import json
import logging
from datetime import datetime
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from models.npc import NPC


class NPCStorageService:
    """Service for storing NPCs to MongoDB database"""
    
    def __init__(self, connection_string: str = None):
        self.logger = logging.getLogger(__name__)
        
        # Get MongoDB connection string from environment or parameter
        self.connection_string = connection_string or os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/zenith_npc_db')
        
        try:
            # Initialize MongoDB client and collection
            self.client = MongoClient(self.connection_string)
            self.db = self.client.get_default_database()
            self.collection: Collection = self.db["NPCs"]
            
            # Test connection
            self.client.admin.command('ping')
            self.logger.info(f"Connected to MongoDB: {self.connection_string}")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def save_npc(self, npc: NPC) -> str:
        """Save a single NPC to MongoDB"""
        
        try:
            # Convert NPC to dict and add metadata
            npc_data = npc.model_dump()
            npc_data['_created_at'] = datetime.now()
            npc_data['_type'] = 'individual'
            
            # Insert the NPC
            result = self.collection.insert_one(npc_data)
            npc_id = str(result.inserted_id)
            
            self.logger.info(f"Saved NPC {npc.Name} with ID {npc_id}")
            return npc_id
            
        except Exception as e:
            self.logger.error(f"Failed to save NPC {npc.Name}: {e}")
            raise

    def save_npcs_batch(self, npcs: List[NPC]) -> List[str]:
        """Save multiple NPCs to individual MongoDB documents"""
        
        saved_ids = []
        for npc in npcs:
            try:
                npc_id = self.save_npc(npc)
                saved_ids.append(npc_id)
            except Exception as e:
                self.logger.error(f"Failed to save NPC in batch: {e}")
                continue
        
        return saved_ids

    def save_npcs_collection(self, npcs: List[NPC]) -> str:
        """Save multiple NPCs as a single collection document"""
        
        try:
            # Create collection document structure
            collection_data = {
                "_created_at": datetime.now(),
                "_type": "collection",
                "generated_at": datetime.now().isoformat(),
                "count": len(npcs),
                "npcs": [npc.model_dump() for npc in npcs]
            }
            
            # Insert the collection
            result = self.collection.insert_one(collection_data)
            collection_id = str(result.inserted_id)
            
            self.logger.info(f"Saved {len(npcs)} NPCs as collection with ID {collection_id}")
            return collection_id
            
        except Exception as e:
            self.logger.error(f"Failed to save NPC collection: {e}")
            raise

    def get_all_npcs(self) -> List[dict]:
        """Load all individual NPCs from MongoDB"""
        
        npcs = []
        try:
            # Query for individual NPCs only (not collections)
            cursor = self.collection.find({"_type": "individual"})
            
            for doc in cursor:
                # Remove MongoDB internal fields for API response
                doc.pop('_id', None)
                doc.pop('_created_at', None) 
                doc.pop('_type', None)
                npcs.append(doc)
                
        except Exception as e:
            self.logger.error(f"Failed to load NPCs: {e}")
        
        return npcs

    def get_storage_stats(self) -> dict:
        """Get statistics about stored NPCs in MongoDB"""
        
        try:
            # Count different types of documents
            total_docs = self.collection.count_documents({})
            individual_npcs = self.collection.count_documents({"_type": "individual"})
            collection_docs = self.collection.count_documents({"_type": "collection"})
            
            return {
                "total_documents": total_docs,
                "individual_npcs": individual_npcs,
                "collection_documents": collection_docs,
                "database": self.db.name,
                "collection": self.collection.name
            }
        except Exception as e:
            self.logger.error(f"Failed to get storage stats: {e}")
            return {"error": str(e)}