import pandas as pd
from datetime import date

# uso = {'nome':['conta04'],'perc_consumo':['60'],'data':['2022-02-21']}
# df_uso = pd.DataFrame(uso)

# # df_uso = pd.DataFrame({'60'})

# df_uso.info()

# print(df_uso)

# print(df_uso.values.tolist())

# data_hoje = date.today()

# print(data_hoje)
uso = '60'

nome = 'conta verificada no banco'
# df_uso = pd.DataFrame({uso})
data_atual = date.today()

dfuso = {'nome':[nome],'uso':[uso],'data':[data_atual]}

df = pd.DataFrame(dfuso)

df.info()
print(df.values.tolist())

