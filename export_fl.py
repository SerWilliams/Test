import pyodbc
from datetime import datetime, timedelta
from json import dumps, dump
from sys import exit
from zlib import compress
from urllib.parse import urlencode
# from urllib2 import Request, urlopen, HTTPError, URLError
from socket import gethostname
Config = {'id_oo': 0, 'code': gethostname()[1:7]}
dt = datetime.strftime(datetime.now() - timedelta(days=18), "%Y-%m-%d")
try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\\FLReports.mdb')
except pyodbc.Error as e:
    print('Ошибка БД', e)
    exit()


def sql_query(query, table, rpath, inti, stri, *floati):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [i[0] for i in cursor.description]
    rows = []
    for stroka in cursor.fetchall():
        for item in inti:
            if stroka[item]:
                stroka[item] = int(stroka[item])
        for item in stri:
            if stroka[item]:
                stroka[item] = str(stroka[item])
        for item in floati:
            if stroka[item]:
                stroka[item] = float(stroka[item].replace(',','.'))
        rows.append(dict(zip(columns, stroka)))
    result = {table: {'columns': columns, 'rows': rows}}
    with open(rpath, 'w') as file:
        dump(result, file, sort_keys=True, ensure_ascii=False)
    send_result({
        'id_oo': Config['id_oo'],
        'code': Config['code'],
        'method': 'gm_kso_flreports',
        'data': compress(dumps(result))
    })




def send_result(data):
    url_in = "http://10.5.4.61:875/api/in_data.php"
    send_data = urlencode(data)
    r = Request(url_in, send_data)
    sendstatus = 0
    while sendstatus == 0:
        try:
            urlopen(r)
        except HTTPError:
            sendstatus = 0
        except URLError:
            sendstatus = 0
        else:
            sendstatus = 1



query_accept = ('''
select StationID,TransactionID,TotalAmount,TimeAccepted from CurrencyAccepted
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_dispens = ('''
select StationID,TransactionID,TotalAmount,TimeDispensed from CurrencyDispensed
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_manager = ('''
select StationID,TransactionID,DeviceType, Denomination, ChangeInCount,
(Denomination*ChangeInCount) as TotalAmount, BalanceInCount, CashManagementTime
from CurrencyCashManagement
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_deverr = ('''
select StationID,TransactionID,Device,TimeOfError from DeviceErrors
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_appmode = ('''
select StationID,TransactionID, ModeName, ModeChangeType, OperatorID, InTransaction, ModeChangeTime
from ApplicationMode
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_interven = ('''
select StationID,TransactionID,InterventionClass, InterventionType,
InterventionStartDateTime, InterventionEndDateTime, ItemID, OperatorID, InTransaction, IsApproved
from Interventions
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_itemex = ('''
select StationID, TransactionID, ItemSKU, ItemDescription, ExpectedWeight, ObservedWeight, ExceptionType, EntryTime
from ItemExceptions
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
query_tenders = ('''
select
StationID, TransactionID, TenderType, TenderTotal, TenderOperatorID, TenderStartTime, TenderEndTime
from Tenders
where TransactionID > '%s' order by  TransactionID desc;
''' % dt)
sql_query(query_accept, 'CurrencyAccepted', 'D:\\FLreports\\json\\accept.json', (0,2,), (3,))
sql_query(query_dispens, 'CurrencyDispensed', 'D:\\FLreports\\json\\dispens.json', (0,2,), (3,))
sql_query(query_manager, 'CurrencyCashManagement', 'D:\\FLreports\\json\\manager.json', (0,3,5,), (7,))
sql_query(query_deverr, 'DeviceErrors', 'D:\\FLreports\\json\\deverr.json', (0,), (3,))
sql_query(query_appmode, 'ApplicationMode', 'D:\\FLreports\\json\\appmode.json', (0,), (6,))
sql_query(query_interven, 'Interventions', 'D:\\FLreports\\json\\interven.json', (0,7,), (4,5,))
sql_query(query_itemex, 'ItemExceptions', 'D:\\FLreports\\json\\itemex.json', (0,), (7,), 4, 5)
sql_query(query_tenders, 'Tenders', 'D:\\FLreports\\json\\tenders.json', (0,3,4,), (5,6,))
