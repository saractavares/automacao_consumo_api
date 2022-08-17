from flask_mail import Mail, Message
import pandas as pd
import pyodbc
from __main__ import app


class sender_email():
    def con_banco():
        print('Init DB')
        global con
        con = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:<SERVER=tcp>;DATABASE=<DATABASE>;UID=<UID>;PWD=<PWD>;Trusted_Connection=no')

        query = """SELECT TOP 1 [nome],[uso],[data_atual] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY id DESC"""
        bd = pd.read_sql_query(query, con)
        

        for i in range(len(bd)):
            global conta, uso, data
            conta = str(bd.nome[i].strip())
            uso = str(bd.uso[i].strip())
            data = str(bd.data_atual[i])

            print(conta, uso, data)

        print('Peguei as credenciais')


    def enviar_email():

        print('Init DB do Sender')

        query = f"""SELECT TOP 1 [nome], [uso], [data_atual] FROM [dbo].[CONSUMO_API_RECURSO] WHERE nome = '{conta}' ORDER BY id DESC"""
        bd = pd.read_sql_query(query, con)

        for i in range(len(bd)):

            uso_atual = str(bd.uso[i].strip())
            uso_atual = int(uso_atual)

        con.close()

        if uso_atual >= 90:
                                    
            app.config["MAIL_SERVER"] = "smtp.gmail.com"
            app.config["MAIL_PORT"] = 587
            app.config["MAIL_USE_TLS"] = True
            app.config["MAIL_USE_SSL"] = False
            app.config["MAIL_USERNAME"] = "apicrmconsumo@gmail.com"
            app.config["MAIL_PASSWORD"] = "ap1con5umo@crm"
            app.config["MAIL_DEFAULT_SENDER"] = "apicrmconsumo@gmail.com"
            app.config["MAIL_MAX_EMAILS"] = 4
            app.config["MAIL_ASCII_ATTACHMENTS"] = True
            app.config["MAIL_TO"] = ["analytics@crmeducacional.com"] #  sara.centeno@crmeducacional.com

            mail = Mail(app)

            msg = Message(" Report Diário do Consumo do Recurso",
                        recipients=app.config["MAIL_TO"])

            msg.body = f'Olá, equipe! \nO recurso de Dashboards da {conta} foi extraído em {data} e está em {uso}% !'

            mail.send(msg)

            print('Email Enviado')

        else:
            print(f'\nO Uso do Recurso Está em {uso_atual}%\n')  
