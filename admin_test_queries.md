# Admin Query Test Commands

## Quick Test Commands (curl)

### 1. User Count Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "How many users are registered in the system?"}'
```

### 2. User Roles Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "What are the different user roles in the system?"}'
```

### 3. Events Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "Show me all the events happening today"}'
```

### 4. Security Incidents Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "How many security incidents have been reported?"}'
```

### 5. Active Alerts Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "What alerts are currently active?"}'
```

### 6. Lost and Found Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "List all lost and found items"}'
```

### 7. Documents Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "What documents are available in the system?"}'
```

### 8. Zone Analysis Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "Which zones have the most users?"}'
```

### 9. Summary Report Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "Generate a summary report of all activities"}'
```

### 10. Event Status Query
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "What is the current status of all events?"}'
```

## Python Test Script

You can also run the Python test script:
```bash
cd Chatbot_AI
python test_admin_queries.py
```

## Custom Queries

You can test any custom query by replacing the "query" value:
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_type": "admin", "query": "YOUR_CUSTOM_QUERY_HERE"}'
``` 