from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint

bp_site = Blueprint('site_', __name__)


@bp_site.route('/')
def home_page():
    return 'Hi'

@bp_site.route('/log_in', methods=['GET', 'POST'])
def login(request):
    #if clients wants to add data
    elif request == 'POST':
        #clean data
        #check if email exists in db
        #check pwd vadility

        #if success create session
        #if fail display errors









