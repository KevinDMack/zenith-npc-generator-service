#!/usr/bin/env python3
"""
Test script for both HTTP (legacy) and Dapr-based (new) NPC Generator Service
This allows testing both implementations during the migration
"""

import requests
import json
import time
import asyncio
import uuid
from typing import Optional

# Try to import Dapr components (may not be available in all environments)
try:
    from dapr.clients import DaprClient
    from npc_pb2 import NPCGenerationRequest, GenerateNPCTopicMessage
    DAPR_AVAILABLE = True
except ImportError:
    DAPR_AVAILABLE = False
    print("⚠️  Dapr components not available. Will test HTTP endpoints only.")

BASE_URL = "http://localhost:5000"
DAPR_BASE_URL = "http://localhost:3500"


class Colors:
    """Console colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'  
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def test_http_health_check():
    """Test the legacy HTTP health check endpoint"""
    print(f"{Colors.BLUE}Testing HTTP health check...{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ HTTP Health check passed{Colors.END}")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"{Colors.RED}❌ HTTP Health check failed: {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ HTTP Health check error: {e}{Colors.END}")
    print()


def test_dapr_health_check():
    """Test the Dapr service health check"""
    if not DAPR_AVAILABLE:
        print(f"{Colors.YELLOW}⚠️  Skipping Dapr health check (Dapr not available){Colors.END}")
        return
        
    print(f"{Colors.BLUE}Testing Dapr health check...{Colors.END}")
    try:
        # Use Dapr service invocation to call health method
        response = requests.post(
            f"{DAPR_BASE_URL}/v1.0/invoke/zenith-npc-generator/method/health",
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ Dapr Health check passed{Colors.END}")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"{Colors.RED}❌ Dapr Health check failed: {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Dapr Health check error: {e}{Colors.END}")
    print()


def test_http_single_npc():
    """Test legacy HTTP single NPC generation"""
    print(f"{Colors.BLUE}Testing HTTP single NPC generation...{Colors.END}")
    try:
        data = {
            "species_preference": "Elf", 
            "district_preference": "Mystic Gardens"
        }
        response = requests.post(f"{BASE_URL}/generate-npc", json=data)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ HTTP Single NPC generation passed{Colors.END}")
            result = response.json()
            print(f"Generated NPC: {result['npc']['Name']}")
            print(f"Saved to: {result['saved_to']}")
        else:
            print(f"{Colors.RED}❌ HTTP Single NPC generation failed: {response.status_code}{Colors.END}")
            print(response.text)
    except Exception as e:
        print(f"{Colors.RED}❌ HTTP Single NPC generation error: {e}{Colors.END}")
    print()


async def test_dapr_single_npc():
    """Test Dapr topic-based single NPC generation"""
    if not DAPR_AVAILABLE:
        print(f"{Colors.YELLOW}⚠️  Skipping Dapr NPC generation (Dapr not available){Colors.END}")
        return
        
    print(f"{Colors.BLUE}Testing Dapr single NPC generation...{Colors.END}")
    try:
        # Create a unique request ID
        request_id = str(uuid.uuid4())
        response_topic = f"npc-generation-response-{request_id}"
        
        # Build protobuf request
        generation_request = NPCGenerationRequest()
        generation_request.count = 1
        generation_request.species_preference = "Elf"
        generation_request.district_preference = "Mystic Gardens"
        
        # Create topic message
        topic_message = GenerateNPCTopicMessage()
        topic_message.request_id = request_id
        topic_message.request.CopyFrom(generation_request)
        topic_message.response_topic = response_topic
        
        # Publish to Dapr topic
        dapr_client = DaprClient()
        dapr_client.publish_event(
            pubsub_name='pubsub',
            topic_name='npc-generation-request',
            data=topic_message.SerializeToString(),
            data_content_type='application/x-protobuf'
        )
        
        print(f"{Colors.GREEN}✅ Dapr NPC request published (ID: {request_id}){Colors.END}")
        print(f"Check logs for processing details")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Dapr NPC generation error: {e}{Colors.END}")
    print()


def test_http_multiple_npcs():
    """Test legacy HTTP multiple NPC generation"""
    print(f"{Colors.BLUE}Testing HTTP multiple NPC generation...{Colors.END}")
    try:
        data = {
            "count": 2,
            "species_preference": "Human"
        }
        response = requests.post(f"{BASE_URL}/generate-npcs", json=data)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ HTTP Multiple NPC generation passed{Colors.END}")
            result = response.json()
            print(f"Generated {result['generated_count']} NPCs")
            print(f"Collection saved to: {result['collection_file']}")
        else:
            print(f"{Colors.RED}❌ HTTP Multiple NPC generation failed: {response.status_code}{Colors.END}")
            print(response.text)
    except Exception as e:
        print(f"{Colors.RED}❌ HTTP Multiple NPC generation error: {e}{Colors.END}")
    print()


def test_service_availability():
    """Test which services are available"""
    print(f"{Colors.BLUE}🔍 Checking service availability...{Colors.END}")
    
    # Check HTTP service
    http_available = False
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        http_available = response.status_code == 200
    except:
        pass
    
    # Check Dapr service
    dapr_available = False
    if DAPR_AVAILABLE:
        try:
            response = requests.post(
                f"{DAPR_BASE_URL}/v1.0/invoke/zenith-npc-generator/method/health",
                timeout=2
            )
            dapr_available = response.status_code == 200
        except:
            pass
    
    print(f"HTTP Service (Legacy): {'🟢 Available' if http_available else '🔴 Not Available'}")
    print(f"Dapr Service (New): {'🟢 Available' if (dapr_available and DAPR_AVAILABLE) else '🔴 Not Available'}")
    print()
    
    return http_available, dapr_available


async def main():
    """Run all tests"""
    print(f"{Colors.BLUE}🧪 Testing Zenith NPC Generator Service{Colors.END}")
    print("=" * 60)
    
    # Check availability
    http_available, dapr_available = test_service_availability()
    
    # Wait a moment for services to be ready
    time.sleep(1)
    
    # Test HTTP endpoints (legacy)
    if http_available:
        print(f"{Colors.YELLOW}🔄 Testing HTTP Endpoints (Legacy){Colors.END}")
        print("-" * 40)
        test_http_health_check()
        test_http_single_npc()
        test_http_multiple_npcs()
    
    # Test Dapr endpoints (new)
    if dapr_available and DAPR_AVAILABLE:
        print(f"{Colors.YELLOW}🔄 Testing Dapr Endpoints (New){Colors.END}")
        print("-" * 40)
        test_dapr_health_check()
        await test_dapr_single_npc()
    
    if not http_available and not dapr_available:
        print(f"{Colors.RED}❌ No services are running. Please start either:{Colors.END}")
        print(f"   HTTP service: python app.py")
        print(f"   Dapr service: ./start_dapr.sh")
    
    print(f"{Colors.BLUE}🎉 Test suite completed!{Colors.END}")


if __name__ == "__main__":
    asyncio.run(main())