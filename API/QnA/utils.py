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

def string_to_boolean(value):
    '''
    Attempt to convert string value to boolean.

    @params
        value, string: String to convert to boolean.
    @return
        True: If string equals to "True" or "true"
        False: If string equals to "False" or "false"
        None: If string cannot be converted to boolean
    '''
    if value == "True" or value == "true" or value == True:
        return True
    elif value == "False" or value == "false" or value == False:
        return False
    return None

def string_to_int(value):
    '''
    Attempts to convert given string value to integer.

    @params
        value, string: String to convert to integer.
    @return
        int: Converted to integer.
        None: If given string cannot be converted to integer.
    '''
    try:
        return int(value)
    except (ValueError, TypeError), e:
        return None


def unique(a):
    ''' return the list with duplicate elements removed '''
    return list(set(a))

def intersect(a, b=False):
    '''
        return the intersection of two lists
        If the second list is not provided, and a is a list of lists:
            return intersection of sublists in a
    '''
    if a and b:
        return list(set(a) & set(b))
    else:
        a = [l for l in a if isinstance(l,list)]
        if a:
            b = a[0]
            for l in a:
                b = intersect(l,b)
            return b

def union(a, b):
    ''' return the union of two lists '''
    return list(set(a) | set(b))
