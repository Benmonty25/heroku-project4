import flask  
import pandas as pd
import yfinance as yf
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask_pymongo import PyMongo

app = flask.Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/stock_history"
mongo = PyMongo(app)

@app.route("/all_history")
def all_history():
    all_history= mongo.db.all_history
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://stockanalysis.com/stocks/'
    browser.visit(url)
    element = browser.find_by_name('perpage').first
    element.select('10000')
    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table', {'class' : 'symbol-table index'})

    symbol = []
    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)

    browser.quit()

    history = pd.DataFrame(columns = ['Symbol','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits'])

    for i in symbol:
        try:
            data = yf.Ticker(i).history(period = 'max')
            df = pd.DataFrame(data)
            df['Date']=df.index
            df['Symbol'] = i
            history = history.append(df)
            print(f"----------{i} complete----------")
        except:
            pass

    # history.to_csv('Output/1wk_stock_history_test.csv',index=False)
    
    history.index = ['A'] * len(history)

    all_history.update(
        {},
        history.to_dict(),
        upsert=True
    )
    return "All History Complete"

@app.route("/sap")
def sap():
    sap= mongo.db.sap
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    browser.visit(url)

    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table')

    symbol = []

    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)
    browser.quit()

    cleaned = []
    for i in symbol:
        cleaned.append(i.strip('\n'))

    sp_df = pd.DataFrame(cleaned, columns =['Symbol'])
    sp_df.index = ['A'] * len(sp_df)

    sap.update(
        {},
        sp_df.to_dict(),
        upsert=True
    )
    return "S&P 500 Complete"

@app.route("/stock_list")
def stock_list():
    stock_list= mongo.db.stock_list
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://stockanalysis.com/stocks/'
    browser.visit(url)
    element = browser.find_by_name('perpage').first
    element.select('10000')
    
    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table', {'class' : 'symbol-table index'})

    symbol = []
    company_name = []
    industry = []
    market_cap= []
    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)
        company_name.append(row.find_all('td')[1].text)
        industry.append(row.find_all('td')[2].text)
        market_cap.append(row.find_all('td')[3].text)

    browser.quit()

    stocks_df = pd.DataFrame(list(zip(symbol, company_name,industry,market_cap)),
            columns =['Symbol', 'Company','Industry','Market Cap'])
    stocks_df.index = ['A'] * len(stocks_df)

    stock_list.update(
        {},
        stocks_df.to_dict(),
        upsert=True
    )
    return "Stock List Complete"

@app.route("/week_history")
def week_history():
    week= mongo.db.week
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://stockanalysis.com/stocks/'
    browser.visit(url)
    element = browser.find_by_name('perpage').first
    element.select('10000')
    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table', {'class' : 'symbol-table index'})

    symbol = []
    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)

    browser.quit()

    history = pd.DataFrame(columns = ['Symbol','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits'])
    symbol = ["AAPL","O"]
    for i in symbol:
        try:
            data = yf.Ticker(i).history(period = '1wk')
            df = pd.DataFrame(data)
            df['Date']=df.index
            df['Symbol'] = i
            history = history.append(df)
            print(f"----------{i} complete----------")
        except:
            pass

    # history.to_csv('Output/1wk_stock_history_test.csv',index=False)
    
    history.index = ['A'] * len(history)

    week.update(
        {},
        history.to_dict(),
        upsert=True
    )
    return "Week History Complete"

if __name__ == "__main__":
    app.run(debug=True)