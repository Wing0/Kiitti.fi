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
    if value == "True" or value == "true":
        return True
    elif value == "False" or value == "false":
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
        if not isinstance(value, basestring):
            raise Exception()
        return int(value)
    except Exception:
        return None
