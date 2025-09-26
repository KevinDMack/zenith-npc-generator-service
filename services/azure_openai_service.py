import os
import json
import logging
from typing import List, Optional
from openai import AzureOpenAI
from models.npc import NPC


class AzureOpenAIService:
    """Service for interacting with Azure OpenAI to generate NPCs"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.logger = logging.getLogger(__name__)

    def generate_npc_prompt(self, species_preference: Optional[str] = None, 
                          district_preference: Optional[str] = None,
                          age_range: Optional[str] = None) -> str:
        """Generate a detailed prompt for NPC creation"""
        
        base_prompt = """Generate a unique NPC (Non-Player Character) for a fantasy mega city named Zenith. 
        Please provide the information in JSON format with the following exact structure:

        {
            "Name": "Character's full name",
            "Age": numeric_age,
            "Species": "Species/Race name",
            "PhysicalDescription": "Detailed physical appearance description",
            "PersonalityDescription": "Detailed personality traits and characteristics",
            "ResidentDistrict": "The district or area where they live"
        }

        Guidelines:
        - Make each character unique and interesting
        - Physical descriptions should be vivid and detailed (2-3 sentences)
        - Personality descriptions should include quirks, motivations, and behavioral traits
        - Districts can be fantasy/sci-fi themed (e.g., "Merchant Quarter", "Tech District", "Mystic Gardens")
        - Species can be fantasy races (elves, dwarves, orcs) or sci-fi aliens
        """
        
        # Add specific constraints if provided
        if species_preference:
            base_prompt += f"\n- Species should be: {species_preference}"
        if district_preference:
            base_prompt += f"\n- Resident District should be: {district_preference}"
        if age_range:
            base_prompt += f"\n- Age should be in range: {age_range}"
            
        base_prompt += "\n\nReturn ONLY the JSON object, no additional text."
        
        return base_prompt

    def generate_npc(self, species_preference: Optional[str] = None,
                    district_preference: Optional[str] = None,
                    age_range: Optional[str] = None) -> Optional[NPC]:
        """Generate a single NPC using Azure OpenAI"""
        
        try:
            prompt = self.generate_npc_prompt(species_preference, district_preference, age_range)
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative writer specializing in generating unique characters for fantasy and sci-fi settings. Always respond with valid JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            # Extract the response content
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to ensure it's valid JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Parse JSON and create NPC object
            npc_data = json.loads(content)
            npc = NPC(**npc_data)
            
            self.logger.info(f"Successfully generated NPC: {npc.Name}")
            return npc
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.error(f"Raw content: {content}")
            return None
        except Exception as e:
            self.logger.error(f"Error generating NPC: {e}")
            return None

    def generate_multiple_npcs(self, count: int = 1, 
                             species_preference: Optional[str] = None,
                             district_preference: Optional[str] = None,
                             age_range: Optional[str] = None) -> List[NPC]:
        """Generate multiple NPCs"""
        
        npcs = []
        for i in range(count):
            npc = self.generate_npc(species_preference, district_preference, age_range)
            if npc:
                npcs.append(npc)
            else:
                self.logger.warning(f"Failed to generate NPC {i+1}/{count}")
        
        return npcs