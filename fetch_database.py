from typing import Any
import pandas as pd
import pyodbc
from configparser import ConfigParser
import os

class config:
    def __init__(self, DSN='', server='', client='', user='', pwd='', port='8080', odbc_driver='SQL') -> None:
        self.DSN = DSN
        self.server = server
        self.client = client
        self.user = user
        self.pwd = pwd
        self.port = port
        self.odbc_driver = odbc_driver
        
    def init(self):
        config = ConfigParser()
        config.read('config.ini')
        #DbValues
        config.add_section('db')
        config.set('db', 'DSN', self.DSN)
        config.set('db', 'server', self.server)
        config.set('db', 'client', self.client)
        config.set('db', 'port', self.port)
        #UserValues
        config.add_section('user_info')
        config.set('user_info', 'user', self.user)
        config.set('user_info', 'pwd', self.pwd)
        #SysValues
        config.add_section('sys')
        config.set('sys', 'odbc', self.odbc_driver)

        with open('config.ini', 'w') as f:
            config.write(f)
            f.close()

    def update(self, section, variable_target, new_value):
        edit = ConfigParser()
        edit.read('config.ini')
        change = edit[section]
        change[variable_target] = new_value
        with open('config.ini', 'w') as configfile:
            edit.write(configfile)
            configfile.close()

class getData():
    def __init__(self) -> None:
        config = ConfigParser()
        if os.path.exists("config.ini"):
            config.read('config.ini')
            self.DSN = config.get('db', 'DSN')
            self.server = config.get('db', 'server')
            self.client = config.get('db', 'client')
            self.port = config.get('db', 'port')
            self.user = config.get('user_info', 'user')
            self.pwd = config.get('user_info', 'pwd')
            self.odbc_driver = config.get('sys', 'odbc')
        else:
            print("init credentials")

    def fetchData(self, tables:list):
        cnxn = pyodbc.connect(f'DRIVER={self.odbc_driver};Server={self.server};Database={self.DSN};Port={self.port};User ID={self.user};Password={self.pwd}')        
        for t in tables:
            sql = f"select * from {t}"
            data = pd.read_sql(sql, cnxn) 
            data.to_csv(f'/data/{t}.csv')


#firebird = config(DSN='test', client='bryan', user='bryan', pwd='123')
#firebird.init()

# firebird = config(DSN='test', client='bryan', user='bryan', pwd='345')
# firebird.init()
# def fetch_database(SERVER, DATABASE, UID, PW):
#     

#config().update('user_info', 'pwd', '123123')
# data = getData()
# data.fetchData()
#https://github.com/hrabe/odbc-on-macos/blob/master/docs/postgresql.md