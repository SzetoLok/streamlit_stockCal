import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import pandas as pd
import numpy as np
import requests
import mysql.connector
import datetime
import json 
import yfinance as yf
import urllib.error

mydb = mysql.connector.connect(
    host="localhost", 
    user="root",
    passwd="xx135367dra",
    database="justforfun",
    )
mycursor=mydb.cursor(buffered=True) 
mycursor.execute("Select * from stocks order by ticker asc, tradedate asc;")
if 'amount' not in st.session_state:
    st.session_state.amount = 0
if 'date' not in st.session_state:
    st.session_state.date = ''  
if 'price' not in st.session_state:
    st.session_state.price = 0 
if 'side' not in st.session_state: 
    st.session_state.side = ''    
if 'ticker' not in st.session_state:
    st.session_state.ticker = ''      
# if 'total_cost' not in st.session_state:
#     st.session_state.total_cost = 0  
# if 'total_profit' not in st.session_state:
#     st.session_state.total_profit = 0  
# st.write(type(st.session_state.total_cost)) 
total_cost=0
total_profit=0

def insert(): 
    command = "Insert into stocks (tradeDate, amount, price, side, ticker) values (\'{}\',{},{},\'{}\',\'{}\');".format(
         st.session_state.date,
         st.session_state.amount, 
         st.session_state.price,
         st.session_state.side,
         st.session_state.ticker)
    print(command) 
    mycursor.execute(command)
    mydb.commit()
    print(mycursor.rowcount,"Record inserted successfully")

def try1():
    print('hihi')
     
with st.form('adding transaction'):
    date = st.date_input("action date",None ,None ,datetime.datetime.now(),key='date')
    st.text_input("ticker", key='ticker')
    st.number_input("Price", key='price', min_value=1)
    st.number_input("Amount", key='amount',min_value=1)
    side = st.selectbox('Side',('buy','sell'), key='side')
    submit = st.form_submit_button('add',on_click=insert)   
 
 
id = st.number_input("Delete id (if inserted wrong data)", key='id', step=1)
if id:
    command = "Delete from stocks where id = {}".format(id)
    print (command)
    mycursor.execute(command)
    mydb.commit()

mycursor.execute("Select distinct ticker from stocks where ticker is not null order by ticker asc;") 
 
distinct_tickers =[]
for x in mycursor:
        distinct_tickers.append( { 
            "ticker": x[0],
        }) 

transactions =[]

for x in distinct_tickers:
    print(x)
    amount=0
    cost=0
    ticker=''
    details= [] 
    current=0 
    command = "Select * from stocks where ticker = '{}' order by ticker asc, tradedate asc;".format(x['ticker'])
    ticker = x['ticker'].upper() 
  
    try: 
         current=yf.Ticker(ticker).info['currentPrice']
         print('current: '+current)
    except Exception as e: 
            #  print(f'123123123123123A HTTPError was thrown: {err.code} {err.reason}')
         print('something went wrong')    
         print(e)
    else:
            print("nothing went wrong")
    finally:
            print("----end----")
    mycursor.execute(command)    
    for x in mycursor:
        details.append( {
             "date": x[0],
            "amount": x[1],
            "price": x[2],
            "side": x[3],
            "total": x[2]*x[1],
            "id":x[5],
        }) 
        
        amount+=x[1]
        cost += x[2]*x[1]
        # st.session_state.total_cost+=cost
    transactions.append({ 
        "cost": cost, 
        "ticker": ticker,
        "avg" : cost/amount,
        "amount" : amount,
        "current": current,
        "market cap" : current*amount,
        "profit" : current*amount-cost,
        "details": details,
    }) 
    total_cost+=cost
# print(json.dumps(transactions, default=str, indent=2)) 
df2 = pd.DataFrame(transactions)
df2["details"] = df2["details"].apply(lambda x: pd.json_normalize(x))
# print(df2)
st.write('Total : '+ str(total_cost))
 

gridOptions1 = {
    # enable Master / Detail
    "masterDetail": True,
    "rowSelection": "single", 
    # the first Column is configured to use agGroupCellRenderer
    "columnDefs": [
        {
            "field": "ticker",
            "cellRenderer": "agGroupCellRenderer", 
            "checkboxSelection": True,
        },
        {"field": "amount"},
        {"field": "avg", "valueFormatter": "'$' + x.toLocaleString() "},
        # {"field": "current"},
        {"field": "cost", "valueFormatter": "'$' + x.toLocaleString() "},
        # {"field": "market cap", "valueFormatter": "'$' + x.toLocaleString() "},
        # {"field": "profit", "valueFormatter": "'$' + x.toLocaleString() "},
    ],
    "defaultColDef": {
        "flex": 1,
    },  
    # provide Detail Cell Renderer Params
    "detailCellRendererParams": {
        # provide the Grid Options to use on the Detail Grid
        "detailGridOptions": {
            "rowSelection": "multiple",
            "suppressRowClickSelection": True,
            "enableRangeSelection": True,
            "pagination": True,
            "paginationAutoPageSize": True,
            "columnDefs": [
                {"field": "id", "checkboxSelection": True},
                {"field": "date","custom_format_string":"yyyy-MM-dd","type":["dateColumnFilter","customDateTimeFormat"],"pivot":True},
                {"field": "side"},
                {"field": "amount"},
                {"field": "price", "valueFormatter": "'$' + x.toLocaleString() "},
                {"field": "total", "minWidth": 150},
            ],
            "defaultColDef": {
                "sortable": True,
                "flex": 1,
            },
        },
        # get the rows for each Detail Grid
        "getDetailRowData": JsCode(
            """function (params) {
                console.log(params);
                params.successCallback(params.data.details);
    }"""
        ).js_code,
    },
}

r1 = AgGrid(
    df2,
    gridOptions=gridOptions1,
    height=500,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED
)

print("----------------------------------")  