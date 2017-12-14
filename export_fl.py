import pyodbc
from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties
from decimal import Decimal
import logging.config
from datetime import datetime, timedelta
from json import dumps, dump
from sys import exit
from zlib import compress
from urllib.parse import urlencode
from urllib.request import Request, urlopen, HTTPError, URLError
from socket import gethostname
from os import makedirs
jsdir = 'C:\\scot\\export\\FLreports'
makedirs(jsdir, exist_ok=True)
logging.config.fileConfig('..\\log_conf.cfg')
logger = logging.getLogger("export_fl")
logger.info('='*60)
logger.info('Запуск экспорта данных из БД FLReports.mdb')
Config = {'id_oo': 0, 'code': gethostname()[1:7]}
dt = datetime.strftime(datetime.now() - timedelta(days=7), "%Y-%m-%d")
logger.info('ИД ГМ - %d, код ГМ - %s, дата начала %s', Config['id_oo'], Config['code'], dt)
try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=C:\\scot\\Report\\Database\\FLReports.mdb')
    logger.debug('Успешное подключение к БД')
except pyodbc.Error as e:
    logger.error('Ошибка БД \n%s \nExit', e)
    exit()


def sql_query(*args):
    logger.info('Выгрузка таблицы %s', args[1])
    cursor = conn.cursor()
    cursor.execute(args[0])
    columns = [i[0] for i in cursor.description]
    rows = []
    for stroka in cursor.fetchall():
        for item in args[3]:
            if stroka[item]:
                stroka[item] = int(stroka[item])
        for item in args[4]:
            if stroka[item]:
                stroka[item] = str(stroka[item])
        try:
            for item in args[5]:
                if stroka[item]:
                    stroka[item] = float(stroka[item].replace(',','.'))
        except:
            pass
        rows.append(dict(zip(columns, stroka)))
    result = {args[1]: {'columns': columns, 'rows': rows}}
    with open(args[2], 'w') as file:
        logger.info('Запись в файл %s', args[2])
        dump(result, file, indent=4, sort_keys=True, ensure_ascii=False)
    try:
     send_messege(compress(dumps(result, sort_keys=True, ensure_ascii=False).encode('utf-8')))
    except Exception as e:
        logger.error('Ошибка отправки данных на сервер %s', e)


def send_messege(message):
    logger.info('Отправка данных на сервер')
    secure = PlainCredentials('sadmin', 'akuma')
    connect = BlockingConnection(
        ConnectionParameters(
         host='10.5.4.15',
         port=5672,
         virtual_host='/',
         credentials=secure
        )
    )
    channel = connect.channel()
    channel.basic_publish(
        exchange='gm_kso_report',
        routing_key='',
        body=message,
        properties=BasicProperties(
         delivery_mode=2,
        )
    )


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
queryes = [
    [query_accept, 'CurrencyAccepted', jsdir + '\\accept.json', (0,2,), (3,)],
    [query_dispens, 'CurrencyDispensed', jsdir + '\\dispens.json', (0,2,), (3,)],
    [query_manager, 'CurrencyCashManagement', jsdir + '\\manager.json', (0,3,5,), (7,)],
    [query_deverr, 'DeviceErrors', jsdir + '\\deverr.json', (0,), (3,)],
    [query_appmode, 'ApplicationMode', jsdir + '\\appmode.json', (0,), (6,)],
    [query_interven, 'Interventions', jsdir + '\\interven.json', (0,7,), (4,5,)],
    [query_itemex, 'ItemExceptions', jsdir + '\\itemex.json', (0,), (7,), (4, 5,)],
    [query_tenders, 'Tenders', jsdir + '\\tenders.json', (0,3,4,), (5,6,)]
]
for i in range(len(queryes)):
    try:
        sql_query(*queryes[i])
    except BaseException as e:
        logger.error('Ошибка выполнения запроса \n%s \n', e)
logger.info('Выгрузка завершена.')
logging.shutdown()
exit(1)
