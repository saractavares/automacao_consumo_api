from flask import Flask, Request, request, redirect, send_from_directory, render_template, session, url_for, Response, flash
import warnings


warnings.filterwarnings("ignore")

app = Flask(__name__)



print('entrou na api flask')



@app.route('/', methods=['GET','POST'])
def principal():
    
    
    return "<center><a href ='https://teste6.azurewebsites.net/api'><button type='button'><h2>Iniciar API</h2></button></a></center>"


@app.route('/api', methods=['GET','POST'])
def api_consumo():
       
    
    from auto import scrap_master
    scrap_master.db_connect()
    scrap_master.scrap()
    scrap_master.update_db()

    from sender import sender_email

    sender_email.con_banco()
    sender_email.enviar_email()


    print('\n\n\n----- Fim do processo ----- \n')
    
    return "<center> <br> <h1>----- Fim do processo -----</h1> </br> <h3>Processo concluído</h3> <center>"


  # debug=True, 
    # app.run(debug=True)
if __name__ == '__main__':
    from waitress import serve
    

    serve(app, host="0.0.0.0", port=80)