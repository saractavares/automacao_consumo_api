from flask import Flask
import warnings


warnings.filterwarnings("ignore")

app = Flask(__name__)
print('entrou na api flask')


@app.route('/', methods=['GET','POST'])
def principal():
    
    
    # return "<center><a href ='https://consumoapirecurso.azurewebsites.net/api'><button type='button'><h2>Iniciar API</h2></button></a></center>"
    return "<center><a href ='http://127.0.0.1:5000/api'><button type='button'><h2>Iniciar API</h2></button></a></center>"
    


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

    # app.run(debug=True) ---> em ambiente local, deve usar nesse formato no build
if __name__ == '__main__':
    from waitress import serve
    

    serve(app.run(debug=True), host="0.0.0.0", port=80)