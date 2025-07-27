import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Mock admin queries for testing
ADMIN_QUERIES = [
    # Database Search Queries
    {
        "user_type": "admin",
        "query": "How many users are registered in the system?"
    },
    {
        "user_type": "admin", 
        "query": "What are the different user roles in the system?"
    },
    {
        "user_type": "admin",
        "query": "Show me all the events happening today"
    },
    {
        "user_type": "admin",
        "query": "How many security incidents have been reported?"
    },
    {
        "user_type": "admin",
        "query": "What alerts are currently active?"
    },
    {
        "user_type": "admin",
        "query": "List all lost and found items"
    },
    {
        "user_type": "admin",
        "query": "What documents are available in the system?"
    },
    {
        "user_type": "admin",
        "query": "Which zones have the most users?"
    },
    {
        "user_type": "admin",
        "query": "Generate a summary report of all activities"
    },
    {
        "user_type": "admin",
        "query": "What is the current status of all events?"
    }
]

def test_admin_queries():
    """Test admin queries one by one"""
    print("🧪 Testing Admin Queries\n")
    
    for i, query_data in enumerate(ADMIN_QUERIES, 1):
        print(f"📝 Test {i}: {query_data['query']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{BASE_URL}/generate",
                headers={"Content-Type": "application/json"},
                json=query_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response: {result}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "="*60 + "\n")

def test_single_query(query_text):
    """Test a single custom query"""
    query_data = {
        "user_type": "admin",
        "query": query_text
    }
    
    print(f"🔍 Testing: {query_text}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            headers={"Content-Type": "application/json"},
            json=query_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Response: {result}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 CrowdGuard AI - Admin Query Tester")
    print("=" * 60)
    
    # Test all predefined queries
    test_admin_queries()
    
    # You can also test custom queries
    # test_single_query("Your custom query here") 