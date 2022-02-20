from xml.etree.ElementTree import tostring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from  sqlalchemy import create_engine
import pandas as pd
import pyodbc
import time


driver = webdriver.Chrome(ChromeDriverManager().install())

login = 'crmdashboard04@crmdashboard04.onmicrosoft.com'
passw = '4dm1n@CRM04'

# Conexão com o servidor

def conexao_db():

    #abrir navegador
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    nav = webdriver.Chrome(chrome_options = options, executable_path="C:\\ChromeDriver\\chromedriver.exe")
    nav.get('https://docs.microsoft.com/en-us/rest/api/power-bi/available-features/get-available-features#code-try-0')


    time.sleep(3)
    # botão "sign in"
    nav.find_element_by_xpath('//*[@id="action-panel"]/div/div/div/button').click()
    time.sleep(3)

    # encontra campo, passa login e avança
    nav.find_element_by_xpath('//*[@id="i0116"]').send_keys(f'{login}')
    nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(5)

    # encontra campo, passa senha e avança
    nav.find_element_by_xpath('//*[@id="i0118"]').send_keys(f'{passw}')
    nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(5)

    # escolhe não continuar conectado
    nav.find_element_by_xpath('//*[@id="idBtn_Back"]').click()
    time.sleep(5)

    # botão "try it"
    nav.find_element_by_xpath('//*[@id="code-try-0"]/button[2]').click()
    time.sleep(3)

    # clica no botão "Run"
    nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[2]/div[5]/button').click()
    time.sleep(5)

    # armazenando a % do consumo atual
    usage= nav.find_element_by_xpath('/html/body/div[3]/div/form/div[3]/div[2]/pre/span/span[18]').text
    

    uso = str(usage)
    print(uso)

    time.sleep(3)

    # Server = 'tcp:f4f8ugzf66.database.windows.net'
    # Database = 'LEADSCORING'
    # Driver = 'ODBC Driver 17 for SQL Server'
    User = 'DataScience'
    Passw = "brasil@1'"
    # Database_con = f"mssql+pyodbc://{User}:{Passw}@tcp:f4f8ugzf66.database.windows.net/LEADSCORING?driver=ODBC Driver 17 for SQL Server"

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=LEADSCORING;UID=DataScience;PWD=brasil@1')

    # engine = create_engine(f"mssql+pyodbc://{User}:{Passw}@tcp:f4f8ugzf66.database.windows.net/LEADSCORING?driver=ODBC+Driver+17+for+SQL+Server")
    # conn = engine.connect()

    #  Conexão com o servidor
    # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
    #                     SERVER=tcp:f4f8ugzf66.database.windows.net; \
    #                     DATABASE= LEADSCORING; \
    #                     UID=DataScience; \
    #                     PWD=brasil@1')
    print(uso)
    # query =                         
    # query_select = "SELECT * FROM [dbo].[API_CONSUMO_RECURSO]"                    
    # print(type(query))
    base = pd.read_sql_query(f"INSERT INTO API_CONSUMO_RECURSO (perc_consumo) VALUES ('{uso}')", conn)
    # conn.commit()
    base

conexao_db()

print("Terminado Aqui")