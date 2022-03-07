from flask import Flask, Request, request, redirect, send_from_directory, render_template, session, url_for, Response, flash
import re
import hashlib
from functools import wraps
import pyodbc
from pytz import timezone
import pickle
import pandas as pd
import warnings
import os

import urllib3

http = urllib3.PoolManager(num_pools=200)

warnings.filterwarnings("ignore")


app = Flask(__name__)

print('entrou na api flask')
# Configurações do app
# app.config['SECRET_KEY'] = 'thisisthesecretkey'

# print('antes do auto')

# print('depois do auto')

# Criando a aplicação

# import auto



@app.route('/', methods=['GET','POST'])


def principal():
    
    
    return "<p> Hello World! 1000 </p>"


@app.route('/api', methods=['GET','POST'])

def api_consumo():

       
    from controller import master

    master.controller_master()
    print('\n\n\n saiu no controller.py\n')
    
    return "<p> Processo concluído </p>"


  # debug=True, 
    # app.run(debug=True)
if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=80)