import pyodbc
import pandas as pd
import numpy as np
import configparser
import warnings
warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('config.ini')


def get_db_setting(server_name,database_name):
    if server_name == 'Devoadb14' and database_name == 'NTHCDataTech':
        driver = config['autooe']['driver']
        server = config['autooe']['server']
        database = config['autooe']['DB']
        user = config['autooe']['id']
        password = config['autooe']['pass']
        status = True
    elif server_name == 'Devoadb19' and database_name == 'NTHCNuIDB':
        driver = config['nuidb']['driver']
        server = config['nuidb']['server']
        database = config['nuidb']['DB']
        user = config['nuidb']['id']
        password = config['nuidb']['pass']
        status = True
    else:
        driver = ""
        server = ""
        database = ""
        user = ""
        password = ""
        status = False
    return status, driver, server, database, user, password


def get_permission(aliasName):
    flag_read, flag_write, flag_active = False, False,False
    strSQL = f"SELECT * FROM [NTHCDataTech].[dbo].[tblAutoOE_API_Permission] WHERE account_id = '{aliasName}' "
    df_permission = select_sql_tbl(strSQL,'Devoadb14','NTHCDataTech')
    if len(df_permission) > 0:
        flag_read = df_permission.loc[0,'flag_read']
        flag_write = df_permission.loc[0,'flag_write']
        flag_active = df_permission.loc[0,'flag_active']
    return flag_read, flag_write, flag_active


# 執行SQL並撈出資料 return df
def select_sql_tbl(strSQL,server_name,database_name):
    # print("strSQL: ",strSQL)
    status, driver, server, database, user, password = get_db_setting(server_name,database_name)
    connect_str = "Driver={%s};Server=%s;Database=%s;uid=%s;pwd=%s" % (driver,server,database,user,password)
    conn = pyodbc.connect(connect_str)
    cursor = conn.cursor()
    df = pd.read_sql(strSQL, conn)
    cursor.close()
    conn.close()
    return df

# 執行SQL Only
def execute_sql(strSQL,server_name,database_name):
    # print("strSQL: ",strSQL)
    status, driver, server, database, user, password = get_db_setting(server_name,database_name)
    connect_str = "Driver={%s};Server=%s;Database=%s;uid=%s;pwd=%s" % (driver,server,database,user,password)
    conn = pyodbc.connect(connect_str)
    cursor = conn.cursor()
    cursor.execute(strSQL)
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    #datetime64
    flag_read, flag_write, flag_active = get_permission('CWKU3')
    # print(res)