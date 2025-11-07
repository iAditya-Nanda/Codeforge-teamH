"""
Quick test to verify Flask server API endpoints
Run this AFTER starting the server with: python server.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print()

def test_api():
    """Test all API endpoints"""
    
    print("\n🚀 Testing Green Points Blockchain API\n")
    
    # 1. Health check
    response = requests.get("http://localhost:5000/health")
    print_response("Health Check", response)
    
    # 2. Get API documentation
    response = requests.get("http://localhost:5000/")
    print_response("API Documentation", response)
    
    # 3. Register a user
    response = requests.post(f"{BASE_URL}/sync-user", json={
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1234567890"
    })
    print_response("Register User", response)
    
    if response.json().get('success'):
        user_id = response.json()['data']['user_id']
        
        # 4. Get user profile
        response = requests.get(f"{BASE_URL}/profile/{user_id}")
        print_response("Get User Profile", response)
        
        # 5. Get user balance
        response = requests.get(f"{BASE_URL}/balance/{user_id}")
        print_response("Get User Balance", response)
        
        # 6. Get available tasks
        response = requests.get(f"{BASE_URL}/tasks")
        print_response("Get Available Tasks", response)
        
        # 7. Submit waste disposal
        response = requests.post(f"{BASE_URL}/submit-waste", json={
            "user_id": user_id,
            "evidence": "Disposed plastic bottle in recycling bin",
            "waste_type": "recyclable"
        })
        print_response("Submit Waste Disposal", response)
        
        if response.json().get('success'):
            verification_id = response.json()['data']['verification_id']
            
            # 8. Get pending verifications (admin)
            response = requests.get(f"{BASE_URL}/admin/verifications")
            print_response("Get Pending Verifications (Admin)", response)
            
            # 9. Approve verification (admin)
            response = requests.post(f"{BASE_URL}/admin/approve/{verification_id}", json={
                "admin_name": "TestAdmin"
            })
            print_response("Approve Verification (Admin)", response)
            
            # 10. Get updated balance
            response = requests.get(f"{BASE_URL}/balance/{user_id}")
            print_response("Get Updated Balance After Reward", response)
        
        # 11. Get user submissions
        response = requests.get(f"{BASE_URL}/submissions/{user_id}")
        print_response("Get User Submissions", response)
        
        # 12. Get transaction history
        response = requests.get(f"{BASE_URL}/transactions/{user_id}?limit=10")
        print_response("Get Transaction History", response)
    
    # 13. Register a business
    response = requests.post(f"{BASE_URL}/sync-user", json={
        "name": "Test Cafe",
        "email": "cafe@example.com"
    })
    print_response("Register Business", response)
    
    if response.json().get('success'):
        business_id = response.json()['data']['user_id']
        
        # 14. Generate QR code
        response = requests.post(f"{BASE_URL}/qr/generate", json={
            "business_id": business_id,
            "reward_amount": 15,
            "service_description": "Coffee purchase"
        })
        print_response("Generate QR Code (Business)", response)
        
        if response.json().get('success'):
            qr_code = response.json()['data']['qr_code']
            
            # 15. Get QR code info
            response = requests.get(f"{BASE_URL}/qr/info/{qr_code}")
            print_response("Get QR Code Info", response)
            
            # 16. Scan QR code (as first user)
            if 'user_id' in locals():
                response = requests.post(f"{BASE_URL}/qr/scan", json={
                    "user_id": user_id,
                    "qr_code": qr_code
                })
                print_response("Scan QR Code (User)", response)
    
    # 17. Get leaderboard
    response = requests.get(f"{BASE_URL}/leaderboard?limit=5")
    print_response("Get Leaderboard", response)
    
    # 18. Get system stats
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Get System Statistics", response)
    
    print("\n✅ All tests completed!\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server!")
        print("Please start the server first with: python server.py")
        print("Then run this test script again.\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
