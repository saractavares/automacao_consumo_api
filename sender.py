from flask import Flask, request, redirect, send_from_directory, render_template, session, url_for, Response, flash
from flask_mail import Mail, Message
import pandas as pd
import time
import pyodbc
from __main__ import app


class sender_email():
    def con_banco():
        print('Init DB')
        global con
        con = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=CONSUMO_DASH;UID=DataScience;PWD=brasil@1;Trusted_Connection=no')

        query = """SELECT TOP 1 [nome],[uso],[data_atual] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY data_atual DESC"""
        bd = pd.read_sql_query(query, con)
        

        for i in range(len(bd)):
                global conta, uso, data
                conta = str(bd.nome[i].strip())
                uso = str(bd.uso[i].strip())
                data = str(bd.data_atual[i])

                print(conta, uso, data)

        print('Peguei as credenciais')


    def enviar_email():

        print('Init DB d9 Sender')

        query = """SELECT TOP 1 [uso] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY data_atual DESC"""
        bd = pd.read_sql_query(query, con)

        for i in range(len(bd)):

            # global uso_atual
            uso_atual = str(bd.uso[i].strip())
            uso_atual = int(uso_atual)

        con.close()

        if uso_atual >= 65:
                                    
            app.config["MAIL_SERVER"] = "smtp.gmail.com"
            app.config["MAIL_PORT"] = 587
            app.config["MAIL_USE_TLS"] = True
            app.config["MAIL_USE_SSL"] = False
            app.config["MAIL_USERNAME"] = "apicrmconsumo@gmail.com"
            app.config["MAIL_PASSWORD"] = "ap1con5umo@crm"
            app.config["MAIL_DEFAULT_SENDER"] = "apicrmconsumo@gmail.com"
            app.config["MAIL_MAX_EMAILS"] = 4
            app.config["MAIL_ASCII_ATTACHMENTS"] = True
            app.config["MAIL_TO"] = ["sara.centeno@crmeducacional.com"] # luiz.felipe@crmeducacional.com       analytics@crmeducacional.com

            mail = Mail(app)

            msg = Message(" Report Diário do Consumo do Recurso",
                        recipients=app.config["MAIL_TO"])

            msg.body = f'Olá, equipe! \nO recurso de Dashboards da {conta} foi extraído em {data} e está em {uso}% !'

            mail.send(msg)

            # time.sleep(3)

            print('Email Enviado')

        else:
            print(f'\nO Uso do Recurso Está em {uso_atual}%\n')  

            

    

# def ret():
#     return True

# ret()