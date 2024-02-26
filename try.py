import streamlit as st
import yfinance as finance
import json

def get_ticker(name):
	company = finance.Ticker(name) # google
	return company


# Project Details
st.title("Build and Deploy Stock Market App Using Streamlit")
st.header("A Basic Data Science Web Application")
st.sidebar.header("Geeksforgeeks \n TrueGeeks")

company1 = get_ticker("GOOGL")
company2 = get_ticker("MSFT")
msft = finance.Ticker("MSFT")
print(msft.info['currentPrice'])


# print("here")
# print(json.dumps(google1.info, indent=2))
# fetches the data: Open, Close, High, Low and Volume
google = finance.download("GOOG", start="2023-09-01", end="2023-09-30")
microsoft = finance.download("MSFT", start="2022-09-01", end="2023-09-01")

# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
data1 = company1.history(period="3mo")
data2 = company2.history(period="3mo")

# markdown syntax
st.write("""
### Google 
""")

# detailed summary on Google
print('---------start---------')
print(type(google))
print(type(data1))

st.write(google)

# plots the graph
st.line_chart(data1.values)
print('---------start---------')
# print(google.info)
# print(type(data1))
# print(data1)
st.write("""
### Microsoft
""") 
st.line_chart(data2.values)
