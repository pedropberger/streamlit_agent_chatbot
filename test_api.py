import requests
import json

def test_api_connection():
    """Test connection to the API"""
    try:
        response = requests.get("http://localhost:1234/health")
        if response.status_code == 200:
            print("✅ API health check successful")
            return True
        else:
            print(f"❌ API health check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API connection failed. Is the API server running at localhost:1234?")
        return False

def test_api_prompt():
    """Test sending a prompt to the API"""
    try:
        url = "http://localhost:1234/api/prompt"
        payload = {"prompt": "This is a test prompt from the test script"}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            print("✅ API prompt test successful")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API prompt test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API connection failed. Is the API server running at localhost:1234?")
        return False
    except Exception as e:
        print(f"❌ Error during API test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing API connection...")
    connection_ok = test_api_connection()
    
    if connection_ok:
        print("\nTesting API prompt endpoint...")
        test_api_prompt()
    else:
        print("\nSkipping API prompt test due to connection failure.")
    
    print("\nTest completed.")