#clean user data funs

def clean_user_data(data):
    clean_data = {}
    for k,v in data:
        if v is None:
            v = ''
        clean_data[k] = v
    return clean_data
