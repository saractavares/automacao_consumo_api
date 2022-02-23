from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import pandas as pd
import pyodbc
import time


# Conectando ao banco e conferindo Conta Ativa
try:
    con = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=CONSUMO_DASH;UID=DataScience;PWD=brasil@1;Trusted_Connection=no')
    print('Conexão com banco estabelecida')
except:
    print('Conexão com Banco Perdida')
query = """select nome, usuario, senha from CONTA_API_CONSUMO
           where data_final is NULL;"""
base = pd.read_sql_query(query, con)

for i in range(len(base)):
    conta = str(base.nome[i].strip())
    usuario = str(base.usuario[i].strip())
    senha = str(base.senha[i].strip())

login = usuario
passw = senha
print('fez as querys')

def extract():

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    nav = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
    nav.get(
        'https://docs.microsoft.com/en-us/rest/api/power-bi/available-features/get-available-features#code-try-0')

    time.sleep(3)

    # botão "sign in"
    nav.find_element_by_xpath(
        '//*[@id="action-panel"]/div/div/div/button').click()

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
    nav.find_element_by_xpath(
        '//*[@id="code-try-0"]/button[2]').click()

    time.sleep(3)

    # clica no botão "Run"
    nav.find_element_by_xpath(
        '//*[@id="action-panel"]/div/form/div[2]/div[5]/button').click()

    time.sleep(3)

    # armazenando a % do consumo atual
    uso = nav.find_element_by_xpath(
        '/html/body/div[3]/div/form/div[3]/div[2]/pre/span/span[18]').text

    time.sleep(3)

    # parâmetros para inserir dados na tabela de consumo
    nome = conta
    df_uso = uso
    data_atual = date.today()

    uso = {'nome': [nome], 'uso': [df_uso], 'data_atual': [data_atual]}
    tb_consumo = pd.DataFrame(uso)

    # Cursor para o banco
    cursor = con.cursor()
    insert_str = """INSERT INTO dbo.CONSUMO_API_RECURSO(nome,uso,data_atual)
        values(?,?,?)"""
    cursor.fast_executemany = True
    cursor.executemany(insert_str,  tb_consumo.values.tolist())
    con.commit()
    # con.close()
    print(
        "******** RASPAGEM DO CONSUMO E ATUALIZAÇÃO DO BANCO DE DADOS CONCLUÍDA ********")
    print()
    print('iniciando envio de email')

    nav.close()
    
extract()

# Conferindo se o uso chegou em 65% e se sim, mandar o email de aviso
query = """SELECT [uso] FROM [dbo].[CONSUMO_API_RECURSO] WHERE data_atual = CONVERT (DATE, SYSDATETIME())"""
bd = pd.read_sql_query(query, con)
for i in range(len(bd)):
        uso_atual = str(bd.uso[i].strip())
        uso_atual = int(uso_atual)

if uso_atual >= 65:
    import sender
    sender    
else:
    print(f'\nO Uso do Recurso Está em {uso_atual}%')  

print()
print('PROCESSO COMPLETO CONCLUÍDO')