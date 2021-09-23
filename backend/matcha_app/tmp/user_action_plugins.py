class SignIn(SiteBody):

    def __init__(self):

         msgs = {'block' : 'you have been blocked contact admin'}
                {'not_activated': 'please activate your account threw the mail, if expired request new'}
                {'already signedin' : 'you are already signed in'}
                {'wrong_auth' : 'pwd or login failed'}

    endpoint : '/signin/<email>'
    GET: FUN
    POST: FUN  restrictioms FUNS: must target his, be signed in, not blocked  return :

    return_data  if sign_in sucess : FUN

    CLEAN : fun


    log:

    restrictions  pwd -> OWNS CHECK FUN
                  email -> owns check fun

    def clean():


    def get():



