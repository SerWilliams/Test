import pyodbc
import logging
import logging.config
from datetime import datetime, timedelta
from json import dumps, dump
from sys import exit
from zlib import compress
from urllib.parse import urlencode
from urllib.request import Request, urlopen, HTTPError, URLError
from socket import gethostname
logging.config.fileConfig('log_conf.cfg')
logger = logging.getLogger("export_fl")
logger.info('='*60)
logger.info('Запуск экспорта данных из БД FLReports.mdb')
Config = {'id_oo': 0, 'code': gethostname()[1:7]}
dt = datetime.strftime(datetime.now() - timedelta(days=20), "%Y-%m-%d")
logger.info('ИД ГМ - %d, код ГМ - %s, дата начала %s', Config['id_oo'], Config['code'], dt)
try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\\FLReports.mdb')
    logger.debug('Успешное подключение к БД')
except pyodbc.Error as e:
    logger.error('Ошибка БД \n%s \nExit', e)
    exit()


def sql_query(query, table, rpath, inti, stri, *floati):
    logger.info('Выгрузка таблицы %s', table)
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
        logger.info('Запись в файл %s', rpath)
        dump(result, file, indent=4, sort_keys=True, ensure_ascii=False)
    send_result({
        'id_oo': Config['id_oo'],
        'code': Config['code'],
        'method': 'gm_kso_flreports',
        'data': compress(dumps(result, sort_keys=True, ensure_ascii=False).encode('utf-8'))
    })


def send_result(data):
    url_in = "http://10.5.4.61:875/api/in_data.php"
    url_in = 'https://httpbin.org'
    logger.info('Отправка данных на сервер %s', url_in)
    send_data = urlencode(data).encode('utf-8')
    r = Request(url_in, send_data)
    sendstatus = 1
    while sendstatus <=3:
        try:
            urlopen(r)
            logger.info('Отправка выполнена успешно')
        except HTTPError as e:
            logger.error('Ошибка подключения к серверу %s, попытка %d ~HTTPError~ %s', e.code, sendstatus, e.reason)
            sendstatus += 1
        except URLError as e:
            logger.error('Ошибка подключения к серверу, попытка %d ~URLError~ %s', sendstatus, e.reason)
            sendstatus += 1
        else:
            sendstatus = 4


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
try:
    sql_query(query_accept, 'CurrencyAccepted', 'D:\\FLreports\\json\\accept.json', (0,2,), (3,))
    sql_query(query_dispens, 'CurrencyDispensed', 'D:\\FLreports\\json\\dispens.json', (0,2,), (3,))
    sql_query(query_manager, 'CurrencyCashManagement', 'D:\\FLreports\\json\\manager.json', (0,3,5,), (7,))
    sql_query(query_deverr, 'DeviceErrors', 'D:\\FLreports\\json\\deverr.json', (0,), (3,))
    sql_query(query_appmode, 'ApplicationMode', 'D:\\FLreports\\json\\appmode.json', (0,), (6,))
    sql_query(query_interven, 'Interventions', 'D:\\FLreports\\json\\interven.json', (0,7,), (4,5,))
    sql_query(query_itemex, 'ItemExceptions', 'D:\\FLreports\\json\\itemex.json', (0,), (7,), 4, 5)
    sql_query(query_tenders, 'Tenders', 'D:\\FLreports\\json\\tenders.json', (0,3,4,), (5,6,))
except BaseException as e:
    logger.error('Ошибка выполнения запроса \n%s \n', e)
logger.info('Выгрузка завершена.')
logging.shutdown()
exit(1)