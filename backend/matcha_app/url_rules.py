
class UrlRules:
    """
      admin contains auth that can do anything

          GET /tr@ht.com   get all info , user does what they want with it | 404 bad request if not exist    *need to be signed in
          DELETE   *must be signed in, you can only aim your account " | else 404

          POST /  *post by body,  | if not complete return errors json | 404 if not exist
          PUT     *must be signed in, you can only aim your account         in body | if key dont exist or cant be changed

    """
    """to avoid request payloads, put as much info as possible in link, a msg 1000 long has to be in body"""
    #urls_root = 'http://127.0.0.1:5000'

    home_page = {'url': '/', 'mthds': None, 'view': Views.home}
    sign_up = {'url': '/signup', 'mthds': ['GET', 'POST'], 'view': Views.signup}
    sign_in = {'url': '/signin', 'mthds': ['GET', 'POST'], 'view': Views.signin}
    activate_account = {'url': '/activate_account', 'mthds': ['GET'], 'view': Views.activate_account} # ?key= token
    #manage_account = {'url': '/<email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': Views.account_manager}  # to search or filter
    
    save_db_to_file = {'url': '/db_to_file', 'mthds': ['GET'], 'view': Views.save_db_to_file}  # to search or filter

    """
    log_in = {'url': '/login/<email>', 'mthds': ['POST'], 'view': Urlrules.home_page}
    sign_in = {'url': '/logout/<email>', 'mthds': ['POST'], 'view': FN}
    sign_up = {'url': '/signup', 'mthds': ['POST'], 'view': FN}
    sign_up = {'url': '/msg/<from_email>/<to_email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN} #body must contain json 'msg' :
    sign_up = {'url': '/<email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN} #to search or filter
    sign_up = {'url': '/users', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN}  # to search or filter ? + -   ?filter=likes+name+birthdate
    sign_up = {'url': '/like/<from_email>/<to_email>', 'mthds': ['GET', 'PUT'], 'view': FN}
    sign_up = {'url': '/block/<from_email>/<to_email>', 'mthds': ['GET' , 'PUT'], 'view': FN}
    activate_account = {'url': '/activate/<user>/<token>', 'mthds': ['POST'], 'view': FN}
    format_activate_account = 'http://127.0.0.1:5000/matcha_activate_account/{}'
    """

    @staticmethod
    def get_cls_data():
        return {k: v for k, v in UrlRules.__dict__.items() if isinstance(v, dict)}


