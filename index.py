import gspread
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def startSession():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    wb = client.open('Horario Zurich')
    sheet1 = wb.sheet1
    return wb

def getJsonData(name):
    with open(name, 'r') as json_file:
        datos = json.loads(json_file.read())
        return datos

def getSheetsData(records,cols,data):
    start = len(data)
    for i in range(start, len(records)):
        rows = records[i]
        obj = {}
        for column in rows.keys():
            if column in list(cols.keys()):
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




def main(wb,data):
    datos1 = data["Horario"]["data"]
    datos2 = data['Tracking']['data']

    sheet1 = wb.sheet1
    sheet2 = wb.worksheet('Time recording')
    records = sheet1.get_all_records()
    records2 = sheet2.get_all_records()
    last1 = len(records)
    last2 = len(records2)
    dif1 = last1 - len(datos1)
    dif2 = last2 -len(datos2)
    if dif1 and dif2 > 0:

        cols1 = {"Dia":5,"Tarea":6,"Hora Inicio":7,"Hora Final":8}
        cols2 = {'Dia':1,'Horas imputadas':2}

        print(datos1)
        data1 = getSheetsData(records,cols1,datos1)
        data2 = getSheetsData(records2, cols2, datos2)
        datos = setTime(data1)
        print(datos)
        data = {"Horario": {
            "data": datos
        },
            "Tracking": {
                "data": data2
            }}
        savedRecords(data, 'saved_records.json')
    return data