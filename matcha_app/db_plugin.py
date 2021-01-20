import db1
import db2

db_manager:

    def exec_sql_fr_db(sql_cmd, db=''):

        db = {'sqlite' : db1.execsqlFUN , 'fakedb ' : db2.execsqlFUN}

        if db == 'sqlite':
