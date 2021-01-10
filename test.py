from flask import Flask, session, redirect, url_for, escape, request
import os
app = Flask(__name__)
app.secret_key = os.urandom(12).hex() #generate once than copy paste


app.config.from_pyfile('config.py')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''

   <form action = "" method = "post">
      <p><input type = text name = username/></p>
      <p<<input type = submit value = Login/></p>
   </form>	
'''

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/settings")
@login_required
def settings():
    pass

{% if current_user.is_authenticated %}
  Hi {{ current_user.name }}!
{% endif %}

