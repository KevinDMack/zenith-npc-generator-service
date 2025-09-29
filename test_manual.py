#!/usr/bin/env python3
"""
Manual testing example for the Dapr-based NPC Generator Service
This script demonstrates how to manually test the topic-based communication
"""

import json
import uuid
import requests
import time

def test_dapr_subscription_endpoint():
    """Test the Dapr subscription endpoint"""
    print("🔍 Testing Dapr subscription endpoint...")
    
    try:
        response = requests.get("http://localhost:50051/dapr/subscribe")
        if response.status_code == 200:
            subscriptions = response.json()
            print("✅ Subscription endpoint working")
            print(f"   Subscriptions: {json.dumps(subscriptions, indent=2)}")
            return True
        else:
            print(f"❌ Subscription endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing subscription endpoint: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    
    try:
        response = requests.get("http://localhost:50051/health")
        if response.status_code == 200:
            health = response.json()
            print("✅ Health check working")
            print(f"   Status: {json.dumps(health, indent=2)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health check: {e}")
        return False

def test_direct_npc_request():
    """Test sending a request directly to the NPC generation endpoint (for testing)"""
    print("🔍 Testing direct NPC generation request...")
    
    try:
        # Create a test request (JSON format for easier manual testing)
        request_data = {
            "request_id": str(uuid.uuid4()),
            "response_topic": "test-response-topic",
            "count": 1,
            "species_preference": "Elf",
            "district_preference": "Mystic Gardens"
        }
        
        response = requests.post(
            "http://localhost:50051/npc-generation-request",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Direct NPC request working")
            print(f"   Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Direct NPC request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing direct NPC request: {e}")
        return False

def test_dapr_publish():
    """Test publishing via Dapr (requires Dapr runtime)"""
    print("🔍 Testing Dapr publish...")
    
    try:
        # Create a test request  
        request_data = {
            "request_id": str(uuid.uuid4()),
            "response_topic": "npc-generation-response",
            "count": 1,
            "species_preference": "Dwarf",
            "district_preference": "Forge District"
        }
        
        # Publish via Dapr
        response = requests.post(
            "http://localhost:3500/v1.0/publish/pubsub/npc-generation-request",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 204]:
            print("✅ Dapr publish working")
            print(f"   Published request ID: {request_data['request_id']}")
            print("   Check service logs for processing details")
            return True
        else:
            print(f"❌ Dapr publish failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing Dapr publish: {e}")
        return False

def test_dapr_service_invocation():
    """Test Dapr service invocation for health check"""
    print("🔍 Testing Dapr service invocation...")
    
    try:
        response = requests.post("http://localhost:3500/v1.0/invoke/zenith-npc-generator/method/health")
        
        if response.status_code == 200:
            health = response.json()
            print("✅ Dapr service invocation working")
            print(f"   Response: {json.dumps(health, indent=2)}")
            return True
        else:
            print(f"❌ Dapr service invocation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing Dapr service invocation: {e}")
        return False

def main():
    """Run all manual tests"""
    print("🧪 Manual Testing for Zenith NPC Generator Service (Dapr Mode)")
    print("=" * 70)
    
    print("\n📋 Prerequisites:")
    print("   1. Service running: python dapr_app.py")
    print("   2. Dapr runtime: dapr run --app-id zenith-npc-generator --app-port 50051 --dapr-http-port 3500 -- python dapr_app.py")
    print("   3. MongoDB running (for actual NPC generation)")
    print("   4. Azure OpenAI credentials in .env file")
    print()
    
    time.sleep(1)
    
    results = []
    
    # Test 1: Direct Flask endpoints (no Dapr required)
    print("🟦 Phase 1: Direct Flask Endpoints")
    print("-" * 40)
    results.append(("Subscription Endpoint", test_dapr_subscription_endpoint()))
    results.append(("Health Check", test_health_check()))
    results.append(("Direct NPC Request", test_direct_npc_request()))
    
    print()
    
    # Test 2: Dapr runtime integration (requires Dapr)
    print("🟦 Phase 2: Dapr Runtime Integration")
    print("-" * 40)
    results.append(("Dapr Service Invocation", test_dapr_service_invocation()))
    results.append(("Dapr Topic Publish", test_dapr_publish()))
    
    print()
    
    # Summary
    print("📊 Test Results Summary")
    print("-" * 40)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Service is ready for Dapr deployment.")
    elif passed >= 3:
        print("⚠️  Service is working but some Dapr features may not be available.")
        print("   Make sure Dapr runtime is running for full functionality.")
    else:
        print("🚨 Service has issues. Check logs and configuration.")

if __name__ == "__main__":
    main()