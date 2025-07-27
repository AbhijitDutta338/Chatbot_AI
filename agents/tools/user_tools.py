from langchain.agents import Tool

def get_user_tools():
    # Define user/invitee specific tools here, e.g., incident report, lost & found
    incident_report_tool = Tool(
        name="IncidentReportTool",
        func=lambda query: "Incident report result for: " + query,
        description="Report incidents based on user queries."
    )
    lost_and_found_tool = Tool(
        name="LostAndFoundTool",
        func=lambda query: "Lost and found result for: " + query,
        description="Search lost and found items."
    )
    return [incident_report_tool, lost_and_found_tool]
