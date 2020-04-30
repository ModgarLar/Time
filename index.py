import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(creds)
wb = client.open('Horario Zurich')
sheet1 = wb.sheet1
sheet2 = wb.worksheet('Time recording')
records = sheet1.get_all_records()
records2 = sheet2.get_all_records()
def getSheetData(records,cols):
    data = []
    for rows in records:
        obj = {}
        for column in rows.keys():
            if column in cols:
                obj[column] = rows[column]
        if len(obj.keys()) > 0:
            data.append(obj)
    return data

def setTime(data):
    form = '%H:%M'
    datos = []
    for row in data:
        obj = row
        day = datetime.strptime(row['Dia'],'%d/%M/%Y')

        init = f"{row['Hora Inicio']}"
        fin = f"{row['Hora Final']}"
        time = 0
        if fin != '':
            t1 = datetime.strptime(fin, form)
            t2 = datetime.strptime(init, form)
            d1 = datetime.combine(day,t1.time())
            d2 = datetime.combine(day,t2.time())
            time = int((d1-d2).total_seconds() /60)
        obj["Time"] = time
        datos.append(obj)
    print(datos)
    return datos

data = getSheetData(records,('Dia', 'Tarea', 'Hora Inicio', 'Hora Final'))
data2 = getSheetData(records2,('Dia','Horas imputadas'))

setTime(data)