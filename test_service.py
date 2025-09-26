#!/usr/bin/env python3
"""
Simple test script for the NPC Generator Service
Run this after starting the service to verify it's working correctly
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    print()

def test_single_npc_generation():
    """Test single NPC generation"""
    print("Testing single NPC generation...")
    try:
        data = {
            "species_preference": "Elf",
            "district_preference": "Mystic Gardens"
        }
        response = requests.post(f"{BASE_URL}/generate-npc", json=data)
        if response.status_code == 200:
            print("✅ Single NPC generation passed")
            result = response.json()
            print(f"Generated NPC: {result['npc']['Name']}")
            print(f"Saved to: {result['saved_to']}")
        else:
            print(f"❌ Single NPC generation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Single NPC generation error: {e}")
    print()

def test_multiple_npc_generation():
    """Test multiple NPC generation"""
    print("Testing multiple NPC generation...")
    try:
        data = {
            "count": 2,
            "species_preference": "Human"
        }
        response = requests.post(f"{BASE_URL}/generate-npcs", json=data)
        if response.status_code == 200:
            print("✅ Multiple NPC generation passed")
            result = response.json()
            print(f"Generated {result['generated_count']} NPCs")
            print(f"Collection saved to: {result['collection_file']}")
        else:
            print(f"❌ Multiple NPC generation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Multiple NPC generation error: {e}")
    print()

def test_get_all_npcs():
    """Test getting all stored NPCs"""
    print("Testing get all NPCs...")
    try:
        response = requests.get(f"{BASE_URL}/npcs")
        if response.status_code == 200:
            print("✅ Get all NPCs passed")
            result = response.json()
            print(f"Found {result['count']} stored NPCs")
        else:
            print(f"❌ Get all NPCs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all NPCs error: {e}")
    print()

def test_storage_stats():
    """Test storage statistics"""
    print("Testing storage statistics...")
    try:
        response = requests.get(f"{BASE_URL}/storage-stats")
        if response.status_code == 200:
            print("✅ Storage statistics passed")
            result = response.json()
            print(json.dumps(result['stats'], indent=2))
        else:
            print(f"❌ Storage statistics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Storage statistics error: {e}")
    print()

def main():
    """Run all tests"""
    print("🧪 Testing Zenith NPC Generator Service")
    print("=" * 50)
    
    # Wait a moment for service to be ready
    time.sleep(1)
    
    test_health_check()
    test_single_npc_generation()
    test_multiple_npc_generation()
    test_get_all_npcs()
    test_storage_stats()
    
    print("🎉 Test suite completed!")

if __name__ == "__main__":
    main()