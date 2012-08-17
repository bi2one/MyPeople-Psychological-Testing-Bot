#ALTER DATABASE MyDb CHARACTER SET utf8;
#ALTER TABLE MyTable CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
from MySQLdb import *
from cmdtools import *
import os, sys
pwd =  os.environ["PWD"]
host = 'localhost'

user='root'
password='dkdnsmrep2'
database='mypeople'

ret = get_yes_or_no('Are you sure convert all tables in %s database charset to utf-8 ? (yes/no) [**CRITICAL**] :' % database)
if not ret :
    sys.exit(0)

db = connect(host, user, password, database)
cursor = db.cursor()

cursor.execute('ALTER DATABASE ' + database + ' CHARACTER SET utf8')
sql = 'show tables'
cursor.execute(sql)
tables = cursor.fetchall()

for table in tables :
    cursor.execute('ALTER TABLE ' + table[0] + ' CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')

db.close()

