from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pyodbc
import time


# Conectando ao banco e conferindo Conta Ativa
con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=LEADSCORING;UID=DataScience;PWD=brasil@1;Trusted_Connection=no')

query = """select nome, usuario, senha from CONTA_API_CONSUMO
           where data_final is NULL;"""
base = pd.read_sql_query(query, con)

for i in range(len(base)):
    conta = str(base.nome[i].strip())
    usuario = str(base.usuario[i].strip())
    senha = str(base.senha[i].strip())

login = usuario
passw = senha

# Busca e Raspagem
def automacao():

    #abrir navegador
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    nav = webdriver.Chrome(chrome_options = options, executable_path="C:\\ChromeDriver\\chromedriver.exe")
    try:
        nav.get('https://docs.microsoft.com/en-us/rest/api/power-bi/available-features/get-available-features#code-try-0')
    except:
        nav.close()
        automacao()

    time.sleep(3)

    # botão "sign in"
    nav.find_element_by_xpath('//*[@id="action-panel"]/div/div/div/button').click()

    time.sleep(3)

    # encontra campo, passa login e avança
    nav.find_element_by_xpath('//*[@id="i0116"]').send_keys(f'{login}')
    nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()

    time.sleep(3)

    # encontra campo, passa senha e avança
    nav.find_element_by_xpath('//*[@id="i0118"]').send_keys(f'{passw}')
    nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()

    time.sleep(3)

    # escolhe não continuar conectado
    nav.find_element_by_xpath('//*[@id="idBtn_Back"]').click()

    time.sleep(3)

    # botão "try it"
    nav.find_element_by_xpath('//*[@id="code-try-0"]/button[2]').click()

    time.sleep(3)

    # clica no botão "Run"
    nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[2]/div[5]/button').click()

    time.sleep(3)

    # armazenando a % do consumo atual
    uso = nav.find_element_by_xpath('/html/body/div[3]/div/form/div[3]/div[2]/pre/span/span[18]').text

    time.sleep(3)  

    # parâmetros para inserir dados na tabela de consumo
    nome = conta
    df_uso = uso
    data_atual = date.today()

    uso = {'nome':[nome],'uso':[df_uso],'data_atual':[data_atual]}
    tb_consumo = pd.DataFrame(uso)

    # Cursor para o banco
    cursor = con.cursor()                    
    insert_str = """INSERT INTO dbo.CONSUMO_API_RECURSO(nome,uso,data_atual)
        values(?,?,?)"""
    cursor.fast_executemany = True
    cursor.executemany(insert_str,  tb_consumo.values.tolist())                  
    con.commit()
    con.close()

automacao()

print("******** RASPAGEM DO CONSUMO E ATUALIZAÇÃO DO BANCO DE DADOS CONCLUÍDA ********")