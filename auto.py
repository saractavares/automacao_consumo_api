from unittest import TestCase
from itsdangerous import json
from matplotlib.pyplot import text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os

driver = webdriver.Chrome(ChromeDriverManager().install())

login = 'crmdashboard04@crmdashboard04.onmicrosoft.com'
passw = '4dm1n@CRM04'

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
# print(nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[3]/div[1]/div/button').click())

# resultado = nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[3]/h2/span').get_attribute(text)

# print(resultado)

print(pd.read_html('https://docs.microsoft.com/en-us/rest/api/power-bi/available-features/get-available-features#code-try-0'))

# div = nav.find_elements_by_xpath('//*[@id="action-panel"]/div/form/div[3]/div[2]')

# div = open('div_resultado.txt','w')
# div.write(div)
# div.close()

# resultado = nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[3]/div[2]/pre/span/span[18]').get_attribute(text)

# print(div)

# nav.switch_to.window(driver.window_handles[1])
# nav.get('https://www.google.com/')
# nav.find_element_by_xpath('')


# resultado = nav.find_element_by_xpath('//*[@id="action-panel"]/div/form/div[3]/div[2]/pre/span/span[18]').send_keys('ctrl','v')

time.sleep(3)

print("Terminado Aqui")

# dolar = nav.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
# print(dolar)

# nav.get('https://www.google.com/')

# nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação euro agora')
# nav.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

# euro = nav.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
# print(euro)

# nav.get('https://www.melhorcambio.com/ouro-hoje#:~:text=O%20valor%20do%20grama%20do,em%20R%24%20280%2C60.')

# ouro = nav.find_element_by_xpath('//*[@id="comercial"]').get_attribute('value')
# ouro = ouro.replace(',','.')
# print(ouro)
# nav.quit()


# # ### Agora vamos atualiza a nossa base de preços com as novas cotações

# # - Importando a base de dados

# # In[69]:


# import pandas as pd

# tb = pd.read_excel(r'C:\repoteste_api\Produtos.xlsx')
# tb.head()


# # - Atualizando os preços e o cálculo do Preço Final

# # In[70]:


# tb.loc[tb["Moeda"] == "Dólar", "Cotação"] = float(dolar)
# tb.loc[tb["Moeda"] == "Euro", "Cotação"] = float(euro)
# tb.loc[tb["Moeda"] == "Ouro", "Cotação"] = float(ouro)

# tb["Preço Base Reais"] = tb["Preço Base Original"] * tb["Cotação"]

# tb["Preço Final"] = tb["Preço Base Reais"] * tb["Margem"]

# tb.head()


# # ### Agora vamos exportar a nova base de preços atualizada

# # In[71]:


# tb.to_excel("Produtos Novo1.xlsx", index=False)