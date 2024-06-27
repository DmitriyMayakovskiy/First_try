import json
import pprint
from openpyexcel import load_workbook
filename = 'pnevmat.xlsx'
wb = load_workbook(filename)
ws = wb['Sheet1']
with open('data.json', encoding='utf-8') as file:
    data = json.load(file)
for i in data:
    ws.append([i['name'],i['price']+'₽', i['full_har']])
wb.save(filename)
wb.close()
