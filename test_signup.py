#!/usr/bin/env python
"""
Simple test script to verify the signup endpoint.
Run this after starting the Django server with: python manage.py runserver
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth/signup"

def test_valid_signup():
    """Test valid user registration"""
    print("Test 1: Valid signup")
    data = {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "securepass123"
    }
    response = requests.post(BASE_URL, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 201, "Expected 201 Created"
    print("✅ Test passed\n")

def test_duplicate_email():
    """Test duplicate email validation"""
    print("Test 2: Duplicate email")
    data = {
        "username": "testuser2",
        "email": "testuser1@example.com",  # Same as test 1
        "password": "anotherpass456"
    }
    response = requests.post(BASE_URL, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 400, "Expected 400 Bad Request"
    assert "email" in response.json(), "Expected email error"
    print("✅ Test passed\n")

def test_duplicate_username():
    """Test duplicate username validation"""
    print("Test 3: Duplicate username")
    data = {
        "username": "testuser1",  # Same as test 1
        "email": "different@example.com",
        "password": "anotherpass789"
    }
    response = requests.post(BASE_URL, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 400, "Expected 400 Bad Request"
    assert "username" in response.json(), "Expected username error"
    print("✅ Test passed\n")

def test_empty_password():
    """Test empty password validation"""
    print("Test 4: Empty password")
    data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": ""
    }
    response = requests.post(BASE_URL, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 400, "Expected 400 Bad Request"
    print("✅ Test passed\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Signup Endpoint")
    print("=" * 60 + "\n")
    
    try:
        test_valid_signup()
        test_duplicate_email()
        test_duplicate_username()
        test_empty_password()
        
        print("=" * 60)
        print("All tests passed! ✅")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server.")
        print("Please start the Django server with: python manage.py runserver")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
