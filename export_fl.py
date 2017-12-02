import pyodbc, datetime, json, decimal
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=FLReports.mdb')
cursor = conn.cursor()
dt = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=18), "%Y-%m-%d")

query_accept = ('''
select StationID,TransactionID,TotalAmount,TimeAccepted from CurrencyAccepted
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_accept)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    stroka[2] = int(stroka[2])
    stroka[3] = str(stroka[3])
    rows.append(dict(zip(columns, stroka)))
accept = {'CurrencyAccepted': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\accept.json', 'w') as file:
    json.dump(accept, file, sort_keys=True)

query_dispens = ('''
select StationID,TransactionID,TotalAmount,TimeDispensed from CurrencyDispensed
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_dispens)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    stroka[2] = int(stroka[2])
    stroka[3] = str(stroka[3])
    rows.append(dict(zip(columns, stroka)))
dispens = {'CurrencyDispensed': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\dispens.json', 'w') as file:
    json.dump(dispens, file, sort_keys=True)

query_manager = ('''
select StationID,TransactionID,DeviceType, Denomination, ChangeInCount,
(Denomination*ChangeInCount) as TotalAmount, BalanceInCount, CashManagementTime
from CurrencyCashManagement
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_manager)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    stroka[3] = int(stroka[3])
    stroka[5] = int(stroka[5])
    stroka[7] = str(stroka[7])
    rows.append(dict(zip(columns, stroka)))
manager = {'CurrencyCashManagement': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\manager.json', 'w') as file:
    json.dump(manager, file, sort_keys=True)


query_deverr = ('''
select StationID,TransactionID,Device,TimeOfError from DeviceErrors
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_deverr)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    stroka[3] = str(stroka[3])
    rows.append(dict(zip(columns, stroka)))
deverr = {'DeviceErrors': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\deverr.json', 'w') as file:
    json.dump(deverr, file, sort_keys=True, ensure_ascii=False)


query_appmode = ('''
select StationID,TransactionID, ModeName, ModeChangeType, OperatorID, InTransaction, ModeChangeTime
from ApplicationMode
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_appmode)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    if stroka[0]:
        stroka[0] = int(stroka[0])
    stroka[6] = str(stroka[6])
    rows.append(dict(zip(columns, stroka)))
appmode = {'ApplicationMode': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\appmode.json', 'w') as file:
    json.dump(appmode, file, sort_keys=True)


query_interven = ('''
select StationID,TransactionID,InterventionClass, InterventionType,
InterventionStartDateTime, InterventionEndDateTime, ItemID, OperatorID, InTransaction, IsApproved
from Interventions
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_interven)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    stroka[4] = str(stroka[4])
    stroka[5] = str(stroka[5])
    if stroka[7]:
        stroka[7] = int(stroka[7])
    rows.append(dict(zip(columns, stroka)))
interven = {'Interventions': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\interven.json', 'w') as file:
    json.dump(interven, file, sort_keys=True, ensure_ascii=False)


query_itemex = ('''
select StationID, TransactionID, ItemSKU, ItemDescription, ExpectedWeight, ObservedWeight, ExceptionType, EntryTime
from ItemExceptions
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_itemex)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    if stroka[4]:
        stroka[4] = float(stroka[4].replace(',','.'))
    if stroka[5]:
        stroka[5] = float(stroka[5].replace(',','.'))
    stroka[7] = str(stroka[7])
    rows.append(dict(zip(columns, stroka)))
itemex = {'ItemExceptions': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\itemex.json', 'w') as file:
    json.dump(itemex, file, sort_keys=True, ensure_ascii=False)


query_tenders = ('''
select
StationID, TransactionID, TenderType, TenderTotal, TenderOperatorID, TenderStartTime, TenderEndTime
from Tenders
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
cursor.execute(query_tenders)
columns = [i[0] for i in cursor.description]
rows = []
for stroka in cursor.fetchall():
    stroka[0] = int(stroka[0])
    if stroka[3]:
        stroka[3] = int(stroka[3])
    if stroka[4]:
        stroka[4] = int(stroka[4])
    stroka[5] = str(stroka[5])
    stroka[6] = str(stroka[6])
    rows.append(dict(zip(columns, stroka)))
tenders = {'Tenders': {'columns': columns, 'rows': rows}}
with open('D:\\FLreports\\json\\tenders.json', 'w') as file:
    json.dump(tenders, file, sort_keys=True, ensure_ascii=False)


conn.close()

