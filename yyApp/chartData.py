import pandas as pd, os

tables = pd.read_excel(os.getcwd() + '/yyApp/shelter_dog.xlsx', sheet_name=[0, 1], engine='openpyxl')
state = tables[0]
city = tables[1]

index = state['상태']
value = state['견 수']

ls_index = list(index)
ls_value = list(value)