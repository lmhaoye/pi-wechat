from flask import Blueprint
pi = Blueprint('pi',__name__)
from . import views