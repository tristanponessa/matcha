"""
      do not call this file email.py, wsgi uses it from flask
      
      https://mailtrap.io/inboxes/1165710/messages/2000654618
      sign in
      in tab email adress red dot disabled , use that to send me an email
      i will receive the email in the mailtrap account
      not on hotmail
      since this is not a real world project , we will not be testing real
      email activity like sending to gmail homtail or others.
      it demands a heavy setup and real accounts
      all fake accounts will be using the mailtrap email id 
      despite having a random account id
"""

from flask import Flask
from flask_mail import Mail, Message

from dict_ops import *

def activate_account(profile_dict):
      app = Flask(__name__)

      app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
      app.config['MAIL_PORT'] = 2525
      app.config['MAIL_USERNAME'] = '38d0520358c29a'
      app.config['MAIL_PASSWORD'] = 'd0ef6b5350f532'
      app.config['MAIL_USE_TLS'] = True
      app.config['MAIL_USE_SSL'] = False

      mail = Mail(app)
      mail.init_app(app)

      name = dict_val_similar_key(profile_dict, 'firstname')
      message = 'click on this link to activate your account url' 
      subject = f"welcome to Matcha, activate your account {name}"
      msg = Message(sender="1f7572dc99-8b0a18@inbox.mailtrap.io",
                  recipients=["tristanponessa@hotmail.com"],
                        body=message,
                        subject=subject)

      with app.app_context():
            mail.send(msg)

      print("sent")



if __name__ == '__main__':
    activate_account({"gen_random_firstname": "TRIS_Hreltpus", "gen_random_lastname": "Hreltpusctapi", "gen_random_profilepic": "./pics/c.png", "gen_random_pics": ["./pics/python-qhd-3840x2400.jpg"], "gen_random_email": "LIixMEOL123456@hotmail.com", "gen_random_pwd": "^>qV{+~]i{b+H?Dy+>?+Y0t", "gen_random_birthdate": "8/10/1989", "get_random_sexori": "straight"})