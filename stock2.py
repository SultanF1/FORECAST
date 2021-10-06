import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

Start = "2000-01-01"
Today = date.today().strftime("%Y-%m-%d")

st.title("Stock Predictor (i1)")

stocks = {"1180.SR", "2222.SR", "1020.SR", "1211.SR", "2290.SR", "3030.SR", "4050.SR", "4100.SR", "4300.SR", "5110.SR", "7202.SR", "8012.SR", "8040.SR"}
selected_stock = st.selectbox("Select the stock ", stocks)

n_months = st.slider("Months of prediction", 1 , 48)
period = n_months * 30

@st.cache
def load_data(ticker):
    data = yf.download(ticker ,Start ,Today)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done")

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Opening price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Closing price'))
    fig.layout.update(title_text="Actual Data", xaxis_rangeslider_visible= True)
    st.plotly_chart(fig)


plot_raw_data()


df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.write(forecast.tail())

st.write('Predicted data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('Predicted components')
fig2 = m.plot_components(forecast)
st.write(fig2)


