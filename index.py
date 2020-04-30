import gspread
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)


def getJsonData(name):
    with open(name, 'r') as json_file:
        datos = json.loads(json_file.read())
        return datos


def getSheetData(records, cols, start):
    data = []
    for i in range(start, len(records)):
        rows = records[i]
        obj = {}
        for column in rows.keys():
            if column in cols:
                obj[column] = rows[column]
        if len(obj.keys()) > 0:
            data.append(obj)

    return data


def savedRecords(data,name):
    with open(name,'w') as json_file:
        json.dump(data,json_file)


def setTime(data):
    form = '%H:%M'
    datos = []
    for row in data:
        obj = row
        day = datetime.strptime(row['Dia'], '%d/%M/%Y')

        init = f"{row['Hora Inicio']}"
        fin = f"{row['Hora Final']}"
        time = 0
        if fin != '':
            t1 = datetime.strptime(fin, form)
            t2 = datetime.strptime(init, form)
            d1 = datetime.combine(day, t1.time())
            d2 = datetime.combine(day, t2.time())
            time = int((d1 - d2).total_seconds() / 60)
        obj["Time"] = time
        datos.append(obj)
    return datos


data = getJsonData('saved_records.json')
start1 = data['Horario']['last']
start2 = data['Tracking']['last']

client = gspread.authorize(creds)
wb = client.open('Horario Zurich')
sheet1 = wb.sheet1
sheet2 = wb.worksheet('Time recording')
last1 = len(sheet1.get_all_records()) - 1
last2 = len(sheet2.get_all_records()) - 1
records = sheet1.get_all_records()
records2 = sheet2.get_all_records()
data1 = getSheetData(records, ('Dia', 'Tarea', 'Hora Inicio', 'Hora Final'), start1)
data2 = getSheetData(records2, ('Dia', 'Horas imputadas'), start2)

datos = setTime(data1)

data = {"Horario": {
    "data": datos,
    "last": last1
},
    "Tracking": {
        "data": data2,
        "last": last2
    }}

savedRecords(data,'saved_records.json')

