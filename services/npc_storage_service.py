import os
import json
import logging
from datetime import datetime
from typing import List
from models.npc import NPC


class NPCStorageService:
    """Service for storing NPCs to local JSON files"""
    
    def __init__(self, storage_dir: str = "citizens"):
        self.storage_dir = storage_dir
        self.logger = logging.getLogger(__name__)
        
        # Ensure the storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_npc(self, npc: NPC) -> str:
        """Save a single NPC to a JSON file"""
        
        try:
            # Generate filename with timestamp and NPC name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in npc.Name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            filename = f"{timestamp}_{safe_name}.json"
            filepath = os.path.join(self.storage_dir, filename)
            
            # Convert NPC to dict and save
            npc_data = npc.model_dump()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(npc_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved NPC {npc.Name} to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to save NPC {npc.Name}: {e}")
            raise

    def save_npcs_batch(self, npcs: List[NPC]) -> List[str]:
        """Save multiple NPCs to individual JSON files"""
        
        saved_files = []
        for npc in npcs:
            try:
                filepath = self.save_npc(npc)
                saved_files.append(filepath)
            except Exception as e:
                self.logger.error(f"Failed to save NPC in batch: {e}")
                continue
        
        return saved_files

    def save_npcs_collection(self, npcs: List[NPC]) -> str:
        """Save multiple NPCs to a single collection JSON file"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"npc_collection_{timestamp}.json"
            filepath = os.path.join(self.storage_dir, filename)
            
            # Convert all NPCs to dict format
            npcs_data = {
                "generated_at": datetime.now().isoformat(),
                "count": len(npcs),
                "npcs": [npc.model_dump() for npc in npcs]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(npcs_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(npcs)} NPCs to collection file {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to save NPC collection: {e}")
            raise

    def get_all_npcs(self) -> List[dict]:
        """Load all NPCs from the storage directory"""
        
        npcs = []
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json') and not filename.startswith('npc_collection_'):
                    filepath = os.path.join(self.storage_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        npc_data = json.load(f)
                        npcs.append(npc_data)
        except Exception as e:
            self.logger.error(f"Failed to load NPCs: {e}")
        
        return npcs

    def get_storage_stats(self) -> dict:
        """Get statistics about stored NPCs"""
        
        try:
            files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
            individual_files = [f for f in files if not f.startswith('npc_collection_')]
            collection_files = [f for f in files if f.startswith('npc_collection_')]
            
            return {
                "total_files": len(files),
                "individual_npcs": len(individual_files),
                "collection_files": len(collection_files),
                "storage_directory": self.storage_dir
            }
        except Exception as e:
            self.logger.error(f"Failed to get storage stats: {e}")
            return {"error": str(e)}