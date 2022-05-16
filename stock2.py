from cProfile import label
import email
import streamlit as st
import pandas as pd
import hashlib
import sqlite3 
from email_validator import validate_email, EmailNotValidError
import time
import re   
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import streamlit.components.v1 as components
import json
from fbprophet.serialize import model_to_json, model_from_json

import time
import pyrebase 

from typing import List
import awesome_streamlit as ast
from awesome_streamlit import testing



def return_favorites(user):
    info = db.child("users").child(user['localId']).get()
    dic = info.val()
    res = []
    if not dic:
        return
    for value in dic:
        res.append(dic[value])
    if len(res) >= 1:
        return res
    else:
        return None

def addStock(user,stock):
    favorites = return_favorites(user)

    if not favorites:
        results = db.child("users").child(str(user['localId'])).push(stock,user['idToken'])
    
    if stock not in favorites:
        results = db.child("users").child(str(user['localId'])).push(stock,user['idToken'])

def Main(user):
    Start = "2000-01-01"
    # Today = date.today().strftime("%Y-%m-%d")
    Today = "2022-01-02"
    

    
    
    current = '2222.SR'
    col2.title('Forecast')
    components.html("""
            <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">Ticker Tape</span></a> by TradingView</div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {
    "symbols": [
        {
        "proName": "FOREXCOM:SPXUSD",
        "title": "S&P 500"
        },
        {
        "proName": "FOREXCOM:NSXUSD",
        "title": "Nasdaq 100"
        },
        {
        "proName": "FX_IDC:EURUSD",
        "title": "EUR/USD"
        },
        {
        "proName": "BITSTAMP:BTCUSD",
        "title": "BTC/USD"
        },
        {
        "proName": "BITSTAMP:ETHUSD",
        "title": "ETH/USD"
        }
    ],
    "colorTheme": "dark",
    "isTransparent": false,
    "displayMode": "adaptive",
    "locale": "en"
    }
    </script>
    </div>
    <!-- TradingView Widget END -->
            """)



    favorites = return_favorites(user)
    if favorites:
        selected_stock = st.selectbox("Select one of your stocks ", return_favorites(user))
        current = selected_stock
        if 'exchange' not in yf.Ticker(selected_stock).info:
            st.warning('invalid ticker, Aramco is selected')
            current = '2222.SR'
    i = st.text_input('Or select a stock of your choice',max_chars=8)
    if i:
        start_time = time.time()
        addStock(user,i)
        st.write("--- %s seconds ---" % (time.time() - start_time))

        current = i
    
    if st.checkbox('Financials'):
        st.table(yf.Ticker(current).financials)
    if st.checkbox('Earnings'):
        st.table(yf.Ticker(current).earnings)
    if st.checkbox('Recommendations'):
        st.table(yf.Ticker(current).recommendations)
    n_months = st.slider("Duration of hold(in months)", 1 , 48)
    period = n_months * 30

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker ,Start ,Today)
        data.reset_index(inplace=True)
        return data
 
    
    


    data = load_data(current)
    
    raw_data = data

    st.subheader('Raw data')


    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=raw_data['Date'], y=raw_data['Open'], name='Opening price'))
        fig.add_trace(go.Scatter(x=raw_data['Date'], y=raw_data['Close'], name='Closing price'))
        fig.layout.update(title_text="Actual Data", xaxis_rangeslider_visible= True)
        st.plotly_chart(fig)


    plot_raw_data()



    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    


    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    
    name = str(current) + '_' + str(Today)
    
    with open(name + '.json', 'w') as fout:
        json.dump(model_to_json(m), fout)
    
    st.write('Predicted data')
    st.write(current)
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    





if 'new_username' not in st.session_state:
	    st.session_state.new_username = ''
if 'new_password' not in st.session_state:
	    st.session_state.new_password = ''

if 'check' not in st.session_state:
	    st.session_state.check = ''


firebaseConfig = {
    'apiKey': "AIzaSyBavWVGGBIoueHrRczXiJH0sOPZBR59Brc",
    'authDomain': "forecast2-af3f0.firebaseapp.com",
    'projectId': "forecast2-af3f0",
    'databaseURL':"https://forecast2-af3f0-default-rtdb.europe-west1.firebasedatabase.app/users/-N1uVM4poddbvXKIQm6f/uid",
    'storageBucket': "forecast2-af3f0.appspot.com",
    'messagingSenderId': "821652824054",
    'appId': "1:821652824054:web:754232d56b173802a931d7",
    'measurementId': "G-9PWZWTM0LC"
    }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database() 
storage = firebase.storage()
def writekyc():
    

    new_un = st.session_state.new_username
    new_pw = st.session_state.new_password
    try:
        user = auth.create_user_with_email_and_password(new_un,new_pw)
        
    except:
        st.warning('Email exists or password is less than 6 characters.')
    
    



st.set_page_config(layout='wide')
col1, col2, col3 = st.columns(3)
def main():
    
  
    
    
    st.title("Welcome")
    text_input_container = st.empty()
    username = text_input_container.text_input("E-mail:")
    text_input_container2 = st.empty()
    password = text_input_container2.text_input("Password",type='password')
    signup_button_container = st.empty()
    signup_button = signup_button_container.button(label='Sign Up')
    if st.checkbox("Keep me Logged in"):
        



        user = auth.sign_in_with_email_and_password(username,password)
        if user:
            
            
            
            text_input_container.empty()
            text_input_container2.empty()
            signup_button_container.empty()
            



                        
            
            data = {'uid':'sultan'}
            try:
                
                results = db.child("users").push(data, user['idToken'])
            except:
                st.write('error')
            
            
            
        else:
            st.warning("Incorrect E-mail/Password")




    if signup_button:  
        with st.form("Sign Up"):
            st.write("Inside the form")            
            st.text_input('New E-Mail', key='new_username')
            st.text_input('New Password:', key='new_password', type='password')
            st.write(st.session_state.new_username)
            
            
            st.form_submit_button(label = "Submit",on_click=writekyc)
            


# def test_items_collector() -> List[testing.models.TesTItem]:
#     """The TesTItems to be tested
#     Returns:
#         List[testing.models.TesTItem] -- The TesTItems to be tested
#     """
#     return testing.services.test_item.get_from_resources()


# def write():
#     testing.test_runner_app.write(test_items_collector=test_items_collector)



    
            
            
if __name__ == '__main__':

    main()
    # write()
