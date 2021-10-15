from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint
from ..app import Global

index = Blueprint('index', __name__)

@index.route('/')
def main_page():
    return 'Hi'




