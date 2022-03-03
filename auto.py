from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import pandas as pd
import pyodbc
import time
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='auto.log', level=logging.INFO, encoding='utf-8',
                    filemode = 'w', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def db_connect():
# Conectando ao banco e conferindo Conta Ativa
    try:
        global con
        con = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:f4f8ugzf66.database.windows.net;DATABASE=CONSUMO_DASH;UID=DataScience;PWD=brasil@1;Trusted_Connection=no')
        print('Conexão com banco estabelecida')
    except:
        logger.error('Conexão com o banco de dados perdida.')
        print('Conexão com Banco Perdida')
    else:    
        query = """select nome, usuario, senha from CONTA_API_CONSUMO
                where data_final is NULL;"""
        base = pd.read_sql_query(query, con)

        for i in range(len(base)):
            nome = str(base.nome[i].strip())
            usuario = str(base.usuario[i].strip())
            senha = str(base.senha[i].strip())

        global login, passw, conta
        login = usuario
        passw = senha
        conta = nome
    
db_connect()

def extract():

    def scrap():

        try:
            # abrir navegador
            chrome_options = Options()
            # chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            global nav
            nav = webdriver.Chrome(
                chrome_options=chrome_options, executable_path="/usr/bin/chromedriver") #  C:\\ChromeDriver\\chromedriver.exe

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

            global nome, df_uso, data_atual
            nome = conta
            df_uso = uso
            data_atual = date.today()

        except:
            print('\nEntrou no except')
            scrap()
            exit
            logger.exception('XPath não encontrado. Processo reiniciado.')

    scrap()
    

    def update_db():
        # parâmetros para inserir dados na tabela de consumo
        
        uso = {'nome': [nome], 'uso': [df_uso], 'data_atual': [data_atual]}
        tb_consumo = pd.DataFrame(uso)

        # Cursor para o banco
        cursor = con.cursor()
        query = """SELECT TOP 1 [uso] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY data_atual DESC"""
        bd = pd.read_sql_query(query, con)
        for i in range(len(bd)):
            uso_ontem = str(bd.uso[i].strip())
            uso_ontem = int(uso_ontem)
            uso_hoje = int(df_uso)
            if uso_hoje > uso_ontem:
            
                insert_str = """INSERT INTO dbo.CONSUMO_API_RECURSO(nome,uso,data_atual)
                    values(?,?,?)"""
                cursor.fast_executemany = True
                cursor.executemany(insert_str,  tb_consumo.values.tolist())
                con.commit()
            else:
                print('\nUso não aumentou, não foi necessário novo registro no Banco\n')
        print(
            "******** RASPAGEM DO CONSUMO E ATUALIZAÇÃO DO BANCO DE DADOS CONCLUÍDA ********")
        print()
        print('iniciando envio de email')

        nav.close()

    update_db()

extract()

# Conferindo se o uso chegou em 65% e se sim, mandar o email de aviso
query = """SELECT TOP 1 [uso] FROM [dbo].[CONSUMO_API_RECURSO] ORDER BY data_atual DESC"""
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
logger.info('Processo executado com sucesso.')
print('PROCESSO COMPLETO CONCLUÍDO')