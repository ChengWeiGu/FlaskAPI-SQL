import flask
import json
from flask import jsonify, request
import pandas as pd
import numpy as np
import socket
import SQLFunc
import warnings
import datetime
warnings.filterwarnings('ignore')
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")

current_ip = socket.gethostbyname(socket.gethostname())
app = flask.Flask(__name__)


@app.route("/home",methods = ['GET'])
def home():
    return_json = {"basic_resp":"Hellow flask"}
    return jsonify(return_json)

@app.route("/test-get",methods = ['GET'])
def test_get():
    # bytes to json string
    json_str = request.data.decode('utf-8')
    json_data = json.loads(json_str)
    data_list = [{"name":"autooe", "id":'No ID'}]
    data_list.append(json_data)
    return_json = {"results":data_list}
    return jsonify(return_json)

@app.route("/test-post",methods = ['POST'])
def test_post():
    # bytes to string
    json_str = request.data.decode('utf-8')
    json_data = json.loads(json_str)
    request_number = json_data['request_number']
    request_time = json_data['request_time']
    
    response_number = request_number**2
    response_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return_json = {"response_number":response_number,
                    "response_time":response_time}
    return jsonify(return_json)


# use for updating user params (23/6/26)
@app.route("/execute-sql",methods=['POST'])
def execute_sql():
    # init returned json
    return_json = {'status':'fail',
                   "error_msg":""}
    try:
        # bytes to json string
        json_str = request.data.decode('utf-8')
        json_data = json.loads(json_str)
        # get data from VBA
        strSQL = json_data['strSQL']
        aliasName = json_data['aliasName']
        server_name = json_data['server_name']
        database_name = json_data['database_name']
        # print(strSQL)
        # get permission
        flag_read, flag_write, flag_active = SQLFunc.get_permission(aliasName)
        if flag_active and flag_write:
            # execute sql usuall for update or insert
            SQLFunc.execute_sql(strSQL,server_name,database_name)
            return_json['status'] = "success"
        else:
            return_json["error_msg"] = "permission denied"
    except Exception as e:
        print(f"got error: {e}")
        return_json["error_msg"] = e
    return jsonify(return_json)


# query header data by posting a "sql string" from VBA (23/6/26)
@app.route("/query-data",methods=['POST'])
def query_data():
    # init returned json
    return_json = {"results":[],
                    "data_length":0,
                    'column_length':0,
                    "columns":[],
                    "status":'fail',
                    "error_msg":""}
    try:
        # bytes to json string
        json_str = request.data.decode('utf-8')
        json_data = json.loads(json_str)
        # get data from VBA
        # print(json_data)
        strSQL = json_data['strSQL']
        aliasName = json_data['aliasName']
        server_name = json_data['server_name']
        database_name = json_data['database_name']
        # get permission
        flag_read, flag_write, flag_active = SQLFunc.get_permission(aliasName)
        if flag_active and flag_read:
            # get header data
            df_data = SQLFunc.select_sql_tbl(strSQL,server_name,database_name)
            col_list = list(df_data.columns)
            # convert datetime to string format
            for col in col_list:
                if str(df_data[col].dtype).startswith("datetime"):
                    df_data[col] = df_data[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            # convert to json data
            data_list_str = df_data.to_json(orient = 'records') # json str
            data_list = json.loads(data_list_str)
            # define return json
            return_json = {"results":data_list,
                            "data_length":len(data_list),
                            'column_length':len(col_list),
                            "columns":col_list,
                            "status":'success',
                            "error_msg":""}
        else:
            return_json["error_msg"] = "permission denied"
    except Exception as e:
        print(f"got error: {e}")
        return_json["error_msg"] = e
    return jsonify(return_json)


if __name__ == "__main__":
    # app.run(port=5555)
    app.run(host=current_ip,port=5555,debug=True)
    pass