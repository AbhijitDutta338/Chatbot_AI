from langchain.agents import Tool
from service.llm_service import LLMService
from service.mock_data_service import MockDataService

def admin_db_search_tool(query: str) -> str:
    """
    Handles admin queries on the event data. It provides a structured LLM-powered response based on mock DB.
    """

    # Step 1: Get mock data and convert into context string
    mock_data_service = MockDataService()
    mock_data = mock_data_service.get_all_data()
    
    formatted_data = ""
    for section, items in mock_data.items():
        formatted_data += f"\n### {section.upper()} ###\n"
        if isinstance(items, list):
            for item in items:
                formatted_data += f"{item}\n"
        else:
            formatted_data += f"{items}\n"

    # Step 2: Prepare the prompt
    prompt = f"""
        You are an event assistant AI for a safety platform.

        A user has asked: "{query}"

        You have access to the following data from the event database:
        {formatted_data}

        Please analyze the data and return a helpful, clear, human-readable answer to the query. Avoid technical language. Be brief but informative.
        """

    # Step 3: Pass to LLM
    return LLMService().model.invoke(prompt)

def get_admin_tools():
    # Define admin specific tools here, e.g., db_search, report generation
    db_search_tool = Tool(
        name="DBSearchTool",
        func=admin_db_search_tool,
        description="Search the database for admin queries."
    )
    report_tool = Tool(
        name="ReportTool",
        func=admin_report_tool,
        description="Generate summary reports based on mock data."
    )
    return [db_search_tool, report_tool]

def admin_report_tool(query: str = "Generate a summary report") -> str:
    """
    Generates a smart summary report from the mock database.
    """

    mock_data_service = MockDataService()
    mock_data = mock_data_service.get_all_data()
    
    users = mock_data.get("users", [])
    events = mock_data.get("events", [])
    alerts = mock_data.get("alerts", [])
    incidents = mock_data.get("incidents", [])
    lost_and_found = mock_data.get("lost_and_found", [])
    documents = mock_data.get("documents", [])

    # Basic counts
    user_count_by_role = {}
    zone_count = {}

    for user in users:
        role = user.get("user_role", "unknown")
        zone = user.get("user_zone", "unknown")
        user_count_by_role[role] = user_count_by_role.get(role, 0) + 1
        zone_count[zone] = zone_count.get(zone, 0) + 1

    stats = {
        "Total Events": len(events),
        "Total Users": len(users),
        "Users by Role": user_count_by_role,
        "Users by Zone": zone_count,
        "Total Alerts": len(alerts),
        "Total Incidents": len(incidents),
        "Total Lost & Found Items": len(lost_and_found),
        "Total Documents": len(documents)
    }

    # Format stats as context
    context = "\n".join([f"{k}: {v}" for k, v in stats.items()])

    prompt = f"""
    You are an Admin Summary Generator AI.

    Based on the following event platform statistics, generate a clean, readable summary for an admin:

    {context}

    Make it human-readable, short, and actionable.
    """

    return LLMService().model.invoke(prompt)
