from flask import Flask


app = Flask(__name__)
from .module.Main import *
