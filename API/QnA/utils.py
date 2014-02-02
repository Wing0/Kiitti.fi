def compose_message(content, identifier=""):
    return {"content":content, "identifier":identifier}

def create_message(content, identifier=""):
    return {"messages": [compose_message(content, identifier)]}
