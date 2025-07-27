def get_tools_for_role(user_type: str):
    """
    Return the list of tools for the given user_type by importing from respective modules.
    """
    if user_type == "admin":
        from .admin_tools import get_admin_tools
        return get_admin_tools()
    elif user_type == "responder":
        from .responder_tools import get_responder_tools
        return get_responder_tools()
    elif user_type == "user":
        from .user_tools import get_user_tools
        return get_user_tools()
    else:
        return []
