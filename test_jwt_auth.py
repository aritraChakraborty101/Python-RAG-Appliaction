#!/usr/bin/env python
"""
Test script for JWT authentication system.
Tests login, token refresh, and protected routes.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_valid_login():
    """Test login with valid credentials"""
    print("Test 1: Valid login")
    data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response keys: {result.keys()}")
    
    assert response.status_code == 200, "Expected 200 OK"
    assert 'access' in result, "Expected access token"
    assert 'refresh' in result, "Expected refresh token"
    assert 'user' in result, "Expected user info"
    print("✅ Test passed\n")
    return result['access'], result['refresh']

def test_invalid_login():
    """Test login with invalid credentials"""
    print("Test 2: Invalid login")
    data = {
        "username": "wronguser",
        "password": "wrongpass"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401, "Expected 401 Unauthorized"
    assert 'error' in response.json(), "Expected error message"
    print("✅ Test passed\n")

def test_missing_credentials():
    """Test login with missing credentials"""
    print("Test 3: Missing credentials")
    data = {
        "username": "testuser1"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 400, "Expected 400 Bad Request"
    print("✅ Test passed\n")

def test_protected_route_without_token():
    """Test accessing protected route without token"""
    print("Test 4: Protected route without token")
    response = requests.get(f"{BASE_URL}/chat-history")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401, "Expected 401 Unauthorized"
    print("✅ Test passed\n")

def test_protected_route_with_token(access_token):
    """Test accessing protected route with valid token"""
    print("Test 5: Protected route with valid token")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{BASE_URL}/chat-history", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    assert response.status_code == 200, "Expected 200 OK"
    assert 'chat_history' in result, "Expected chat history"
    print("✅ Test passed\n")

def test_protected_route_with_invalid_token():
    """Test accessing protected route with invalid token"""
    print("Test 6: Protected route with invalid token")
    headers = {
        "Authorization": "Bearer invalid_token_here"
    }
    response = requests.get(f"{BASE_URL}/chat-history", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401, "Expected 401 Unauthorized"
    print("✅ Test passed\n")

def test_token_refresh(refresh_token):
    """Test token refresh endpoint"""
    print("Test 7: Token refresh")
    data = {
        "refresh": refresh_token
    }
    response = requests.post(f"{BASE_URL}/token/refresh", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    assert response.status_code == 200, "Expected 200 OK"
    assert 'access' in result, "Expected new access token"
    print("✅ Test passed\n")
    return result['access']

def test_new_access_token(new_access_token):
    """Test using refreshed access token"""
    print("Test 8: Using refreshed access token")
    headers = {
        "Authorization": f"Bearer {new_access_token}"
    }
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    assert response.status_code == 200, "Expected 200 OK"
    print("✅ Test passed\n")

if __name__ == "__main__":
    print("=" * 70)
    print("Testing JWT Authentication System")
    print("=" * 70 + "\n")
    
    try:
        # Test login
        access_token, refresh_token = test_valid_login()
        test_invalid_login()
        test_missing_credentials()
        
        # Test protected routes
        test_protected_route_without_token()
        test_protected_route_with_token(access_token)
        test_protected_route_with_invalid_token()
        
        # Test token refresh
        new_access_token = test_token_refresh(refresh_token)
        test_new_access_token(new_access_token)
        
        print("=" * 70)
        print("All tests passed! ✅")
        print("=" * 70)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server.")
        print("Please start the Django server with: ./venv/bin/python manage.py runserver")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
