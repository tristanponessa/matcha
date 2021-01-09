#user_data : dict

"""
    for password security use bycrypt which uses 
"""
"""
    cheap sql python sol : only add del  sort with python
    all this is suppsoed to be done in django but i can't
"""

def action_db(action, table, **data):

    conditions = ' AND '.join([f'{k}={v}' for k,v in d.items()])
    cmds = {
    'delete' : f"DELETE FROM {table_name} WHERE {conditions}"
    'add' : f"INSERT INTO {table} ({fields}) VALUES ({vals})"
    'get' : f"SELECT * FROM {table_name}"}

    return sql_execute(cmds[action])

def has_profile(user_email):
    x = action_db('get', 'users')
    return user_mail == x['email']

def sign_up(**data):
    """insert into db new user, check if user exists, prevent sql html code injection"""
    action_db('')

def sign_in():
    """check if user present , if so check pwd"""
    if not has_profile():
        return #launch sign up  , ask front to display you dont have n account
    #start session
    #return succeeded to front to change url to display profile

    #deal with blocked profiles


    

def change_user_data():
    pass

def disconnect():
    pass

def  