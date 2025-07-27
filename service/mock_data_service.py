import json
import os

class MockDataService:
    def __init__(self):
        # Resolve absolute path to mock_data.json
        mock_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock_data.json')
        with open(mock_data_path, 'r') as f:
            self.mock_data = json.load(f)

    def get_users(self):
        return self.mock_data.get("users", [])

    def get_events(self):
        return self.mock_data.get("events", [])

    def get_incidents(self):
        return self.mock_data.get("incidents", [])

    def get_alerts(self):
        return self.mock_data.get("alerts", [])

    def get_documents(self):
        return self.mock_data.get("documents", [])

    def get_lost_and_found(self):
        return self.mock_data.get("lost_and_found", [])
    
    def get_all_data(self):
        return self.mock_data
