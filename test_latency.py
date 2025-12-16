#!/usr/bin/env python
"""
Test script to verify the latency measurement feature
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
CHAT_URL = f"{BASE_URL}/api/chat"

# Test credentials (you'll need to use real credentials)
USERNAME = "testuser"  # Replace with your username
PASSWORD = "testpass"  # Replace with your password

def test_latency():
    """Test the latency measurement feature"""
    
    print("=" * 60)
    print("LATENCY MEASUREMENT TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        tokens = response.json()
        access_token = tokens.get('access')
        print(f"   ✅ Login successful")
        
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Step 2: Send a test message
    print("\n2. Sending test message...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    test_message = "What is Django?"
    chat_data = {
        "message": test_message
    }
    
    try:
        # Measure client-side latency
        client_start = time.time()
        response = requests.post(CHAT_URL, json=chat_data, headers=headers)
        client_end = time.time()
        
        client_latency = (client_end - client_start) * 1000  # Convert to ms
        
        if response.status_code != 201:
            print(f"   ❌ Chat request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        data = response.json()
        print(f"   ✅ Chat request successful")
        
        # Step 3: Display latency information
        print("\n3. Latency Metrics:")
        print("   " + "-" * 56)
        
        if 'latency' in data:
            latency = data['latency']
            
            print(f"   📊 CLIENT-SIDE LATENCY:")
            print(f"      Total Round-Trip Time: {client_latency:.2f}ms")
            
            print(f"\n   ⚙️  SERVER-SIDE LATENCY:")
            print(f"      Total Processing Time: {latency['total_ms']}ms")
            print(f"      RAG Processing Time:   {latency['rag_processing_ms']}ms")
            print(f"      Database Time:         {latency['database_ms']}ms")
            
            if 'breakdown' in latency:
                breakdown = latency['breakdown']
                print(f"\n   🔍 DETAILED BREAKDOWN:")
                print(f"      Conversation Setup: {breakdown['conversation_setup_ms']}ms")
                print(f"      RAG Query:          {breakdown['rag_query_ms']}ms")
                print(f"      Database Save:      {breakdown['database_save_ms']}ms")
            
            # Calculate network latency
            network_latency = client_latency - latency['total_ms']
            print(f"\n   🌐 NETWORK LATENCY:")
            print(f"      Estimated Network Time: {network_latency:.2f}ms")
            
            # Performance rating
            print(f"\n   📈 PERFORMANCE RATING:")
            if client_latency < 1500:
                rating = "🟢 Fast"
            elif client_latency < 3000:
                rating = "🟡 Medium"
            else:
                rating = "🔴 Slow"
            print(f"      {rating} ({client_latency:.0f}ms)")
            
        else:
            print("   ⚠️  No latency data in response")
        
        print("\n   " + "-" * 56)
        
        # Display partial response
        print(f"\n4. AI Response Preview:")
        ai_response = data.get('ai_response', 'No response')
        preview = ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
        print(f"   {preview}")
        
        print("\n" + "=" * 60)
        print("✅ LATENCY TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"   ❌ Chat error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n⚠️  Note: Make sure to update USERNAME and PASSWORD in the script")
    print("    with valid credentials before running this test.\n")
    
    # Uncomment the line below to run the test
    # test_latency()
    
    print("To run the test, edit this file and:")
    print("1. Set your username and password")
    print("2. Uncomment the test_latency() call at the end")
    print("3. Run: python test_latency.py\n")
