# -*- coding: cp1251 -*-

import kinterbasdb as kdb, simplejson as json, re
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError, URLError
from zlib import compress


def GetConfig():
	data = ReadDataFromFile('/usr/local/tander/etc/local_db.conf')
	kwargs = {}

	try:
		kwargs['code'] = re.findall('^code\s+(.*)', data, re.M)[0]
	except:
		kwargs['code'] = ''

	try:
		kwargs['dsn'] = re.findall('^connection\s+(.*)', data, re.M)[0]
	except:
		kwargs['dsn'] = ''

	try:
		kwargs['password'] = re.findall('^password\s+(.*)', data, re.M)[0]
	except:
		kwargs['password'] = ''
	kwargs['user'] = 'sadmin'
	kwargs['charset'] = 'WIN1251'
	kwargs['id_oo'] = ReadDataFromFile('/base/sql/scripts/confs/main.conf').split("\n")[1]
	return kwargs

def CreateConnection(kwargs):
	try:
		connection = kdb.connect(**kwargs)
		return connection
	except Exception, e:
		print e
		return None

def ReadDataFromFile(path):
	f = open(path, 'r')
	data = f.read()
	f.close()
	return data

def ExecQuery(cursor, state, cash):
	try:
		cursor.execute(state, (cash, cash, cash))
		table = cursor.fetchallmap()
		result = [string for string in table]
		return result[0]
	except NoneType:
		return None

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

try:
	Config = GetConfig()
	Connection = CreateConnection(Config)
	if Connection is not None:
		data = ReadDataFromFile('/work/whs/spcash/local_starter.xml')
		cash_list = [string.split('name="')[1].split('"')[0] for string in data.split("\n") if string.find('cash_kso') > 0]
		if len(cash_list) > 0:
			cursor = Connection.cursor()
			state = cursor.prep('''
				select first 1
					trim(c(datetostr(current_timestamp, '%d.%m.%Y'))) check_date,
					trim(c(datetostr(max(op.lastdate), '%d.%m.%Y %H:%M:%S'))) last_sale,
					(select count(*) from operation where id_session = (select max(id_session) from sp_session where hostname = ?) 
						and opdate = extractdate(current_timestamp) and id_top = '3') count_sale,
					(select case when ((sum(opsum)) is null) then cast (0 as INTEGER) else cast(sum(opsum) as INTEGER) end from operation
						where id_session = (select max(id_session) from sp_session where hostname = ?)
						and opdate = extractdate(current_timestamp) and id_top = '3') sum_sale,
					sp.cash_number,
					sp.kkm_num
				from  sp_session sp
				left join operation op ON op.id_session = sp.id_session
				where op.id_top = 3 and op.opdate > extractdate(current_timestamp)-15 and sp.hostname = ?
				group by 1,5,6 
				order by max(op.lastdate) desc
				''')
			result_obj = [ExecQuery(cursor, state, cash) for cash in cash_list]
			result = [{
				'check_date': string['CHECK_DATE'].strip(),
				'last_sale': string['LAST_SALE'].strip(),
				'count_sale': string['COUNT_SALE'],
				'sum_sale': string['SUM_SALE'],
				'cash_number': string['CASH_NUMBER'],
				'kkm_num': string['KKM_NUM'].strip()
			} for string in result_obj]
			send_result({
				'id_oo': Config['id_oo'],
				'code': Config['code'],
				'method': 'gm_kso_sales',
				'data': compress(json.dumps(result))
			})

except Exception, e:
	print e
