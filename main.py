from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.agent_executor import AgentExecutorBuilder
from utils.logger import setup_logger

app = FastAPI(title="CrowdGuard AI", description="AI-powered crowd management system")

logger = setup_logger("crowdguard", "logs/crowdguard.log")

@app.get("/")
async def root():
    """Root endpoint to check if server is running"""
    return {"message": "CrowdGuard AI Server is running!", "endpoints": ["/generate"]}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T12:00:00Z"}

@app.post("/generate")
async def generate_content(request: Request):
    try:
        logger.info("Received request to /generate endpoint")
        data = await request.json()
        user_type = data.get("user_type")
        query = data.get("query")

        logger.info(f"Received request with user_type: {user_type}, query: {query}")

        if not user_type:
            return JSONResponse(status_code=400, content={"error": "Missing user_type"})
        if not query:
            return JSONResponse(status_code=400, content={"error": "Missing query"})

        agent = AgentExecutorBuilder(user_type).create()
        logger.info("AgentExecutor created, running query...")
        # Pass empty chat history for ConversationalChatAgent
        response = agent.run({"input": query, "chat_history": []})
        logger.info(f"Agent response: {response}")

        return response

    except Exception as e:
        logger.error(f"Exception in /generate endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )
