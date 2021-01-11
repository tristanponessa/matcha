from flask import Flask, render_template, request, redirect, url_for, flash, make_response

@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res

@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res


@app.route('/article/', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60 * 60 * 24 * 15)
        res.headers['location'] = url_for('article')
        return res, 302

    return render_template('article.html')

"""
<body style="{% if request.cookies.get('font') %}font-family:{{ request.cookies.get('font') }}{% endif %}">

Select Font Preference: <br>
<form action="" method="post">
    <select name="font" onchange="submit()">
        <option value="">----</option>
        <option value="consolas" {% if request.cookies.get('font') == 'consolas' %}selected{% endif %}>consolas</option>
        <option value="arial" {% if request.cookies.get('font') == 'arial' %}selected{% endif %}>arial</option>
        <option value="verdana" {% if request.cookies.get('font') == 'verdana' %}selected{% endif %}>verdana</o
"""