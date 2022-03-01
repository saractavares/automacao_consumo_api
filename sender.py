from flask import Flask
from flask_mail import Mail, Message
import pandas as pd
import time
import pyodbc


print('Init DB')
con = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=CONSUMO_DASH;UID=DataScience;PWD=brasil@1;Trusted_Connection=no')

# cursor = con.cursor()
query = """SELECT TOP 1 [nome],[uso],[data_atual] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY data_atual DESC"""
bd = pd.read_sql_query(query, con)


for i in range(len(bd)):
        conta = str(bd.nome[i].strip())
        uso = str(bd.uso[i].strip())
        data = str(bd.data_atual[i])

        print(conta, uso, data)

print('Peguei as credenciais')


app = Flask(__name__)
with app.app_context():

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = "apicrmconsumo@gmail.com"
    app.config["MAIL_PASSWORD"] = "ap1con5umo@crm"
    app.config["MAIL_DEFAULT_SENDER"] = "apicrmconsumo@gmail.com"
    app.config["MAIL_MAX_EMAILS"] = 4
    app.config["MAIL_ASCII_ATTACHMENTS"] = True
    app.config["MAIL_TO"] = ["luiz.felipe@crmeducacional.com"] # 

    mail = Mail(app)

    msg = Message(" Report Diário do Consumo do Recurso",
                recipients=app.config["MAIL_TO"])

    msg.body = f'Olá, equipe! \nO recurso de Dashboards da {conta} foi extraído em {data} e está em {uso}% !'

    mail.send(msg)

    time.sleep(3)

    print('Email Enviado')

    # send_email()

if __name__ == '__main__':
    app.run(debug=True)



