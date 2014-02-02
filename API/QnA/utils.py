def compose_message(content, identifier=""):
    return {"content":content, "identifier":identifier}

def create_message(content, identifier=""):
    return {"messages": [compose_message(content, identifier)]}

def exclude_old_versions(message_list):
    # Sort all messages by version
    message_list.sort(key=lambda q: -q.version)

    used = []
    messages = []
    # Append first occurrence of message id to messages
    for q in message_list:
        if q.message_id not in used:
            messages.append(q)
            used.append(q.message_id)
    return messages
