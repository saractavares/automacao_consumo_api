from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import pandas as pd
import pyodbc
import time
import logging
# import sender



class scrap_master():

    
    def db_connect():

        global logger
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='auto.log', level=logging.INFO, encoding='utf-8',
                            filemode = 'w', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    # Conectando ao banco e conferindo Conta Ativa
        try:
            global con
            con = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:SERVER;DATABASE=DATABASE;UID=UID;PWD=PWD;Trusted_Connection=no')
            print('Conexão com banco estabelecida')
        except:
            logger.error('Conexão com o banco de dados perdida.')
            print('Conexão com Banco Perdida')
        else:    
            query = """select * from CONTA_API_CONSUMO where data_final is NULL """ #
            base = pd.read_sql_query(query, con)

            for i in range(len(base)):
                nome = str(base.nome[i].strip())
                usuario = str(base.usuario[i].strip())
                senha = str(base.senha[i].strip())

            global login, passw, conta, site
            login = usuario
            passw = senha
            conta = nome
            site = 'https://docs.microsoft.com/en-us/rest/api/power-bi/available-features/get-available-features#code-try-0'
            print(login,passw,conta)

    def scrap():
      
        try:                 

            # abrir navegador
            chrome_options = Options()
            # chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" # ---> ambiente de teste no Windows, desabilitar as 3 chrome.options abaixo
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            global nav

            from requests_futures.sessions import FuturesSession

            
            session = FuturesSession(max_workers = 100) 
            global nav   
            nav = session
            nav = webdriver.Chrome( chrome_options=chrome_options,executable_path="/usr/bin/chromedriver") #    C:\\ChromeDriver\\chromedriver.exe ---> ambiente de teste Windows, trocar o path
            nav.get(site)
            
            time.sleep(3)

            # botão "sign in"
            nav.find_element_by_xpath('//*[@id="action-panel"]/div/div/div/button').click()
            print('clicou em sign in')
            time.sleep(3)

            # encontra campo, passa login e avança
            nav.find_element_by_xpath('//*[@id="i0116"]').send_keys(f'{login}')
            nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()
            print('mandou o loggin')

            time.sleep(3)

            # encontra campo, passa senha e avança
            nav.find_element_by_xpath('//*[@id="i0118"]').send_keys(f'{passw}')
            nav.find_element_by_xpath('//*[@id="idSIButton9"]').click()
            print('mandou a senha')

            time.sleep(3)

            # escolhe não continuar conectado
            nav.find_element_by_xpath('//*[@id="idBtn_Back"]').click()
            print('escolheu não ficar conectado')

            time.sleep(3)

            # botão "try it"
            nav.find_element_by_xpath('//*[@id="code-try-0"]/button[2]').click()
            print('clicou em try it')

            time.sleep(3)

            # clica no botão "Run"
            nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[2]/div[5]/button').click()
            print('clicou em Run')

            time.sleep(3)

            # armazenando a % do consumo atual
            uso = nav.find_element_by_xpath('/html/body/div[3]/div/form/div[3]/div[2]/pre/span/span[18]').text
            print('Pegou o consumo')

            time.sleep(3)

            global nome, df_uso, data_atual
            nome = conta
            df_uso = uso
            data_atual = date.today()

        except:
            print('\nEntrou no except')
            time.sleep(3)
            nav.close()
            scrap_master.scrap()
            logger.exception('XPath não encontrado. Processo reiniciado.')    

        

    def update_db():
        # parâmetros para inserir dados na tabela de consumo
        
        uso = {'nome': [nome], 'uso': [df_uso], 'data_atual': [data_atual]}
        tb_consumo = pd.DataFrame(uso)

        # Cursor para o banco
        try:
            
            query = f"""SELECT COUNT(nome) as conta_nova FROM [dbo].[CONSUMO_API_RECURSO] WHERE nome =  '{conta}'"""
            bd = pd.read_sql_query(query, con)
            for i in range(len(bd)):
                print('FOR do TRY')
                qntd_registros = bd.conta_nova[i]
                
            if qntd_registros == 0:
                # se a conta nunca teve registro de consumo:
                cursor = con.cursor()
                print('entrou no if == 0')
                insert_str = """INSERT INTO dbo.CONSUMO_API_RECURSO(nome,uso,data_atual) values(?,?,?)"""
                print('passou o insert')

                cursor.fast_executemany = True
                print('passou o fast')

                cursor.executemany(insert_str,  tb_consumo.values.tolist())
                print('passou o execute')
            
                con.commit()
                print('passou o commit')

                con.close()

            else:
                # se a conta já tem registros de consumo anteriores
                query = f"""SELECT top 1 nome, uso, data_atual FROM [dbo].[CONSUMO_API_RECURSO] WHERE nome = '{conta}' order by data_atual DESC"""
                print("Fez a QUERY")        
                bd = pd.read_sql_query(query, con)
                
                for i in range(len(bd)):
                    print('FOR do TRY')
                    uso_ontem = str(bd.uso[i].strip())
                    uso_ontem = int(uso_ontem)
                    uso_hoje = int(df_uso)

                    if uso_hoje > uso_ontem :
                       
                        cursor = con.cursor()
                        insert_str = """INSERT INTO dbo.CONSUMO_API_RECURSO(nome,uso,data_atual) values(?,?,?)"""
                        cursor.fast_executemany = True
                        cursor.executemany(insert_str,  tb_consumo.values.tolist())
                        con.commit()
                        con.close()
                    else:
                        print('Uso não aumentou do TRY')

        except: 
            print('except SE a conta não existe')

        print(
            "******** RASPAGEM DO CONSUMO E ATUALIZAÇÃO DO BANCO DE DADOS CONCLUÍDA ********")
        print()
        print('iniciando envio de email')
        print('\nIniciando SENDER\n')

        nav.close()

