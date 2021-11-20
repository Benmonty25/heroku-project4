import flask  
import pandas as pd
import yfinance as yf
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

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
        data = yf.Ticker(i).history(period = '1wk')
        df = pd.DataFrame(data)
        df['Date']=df.index
        df['Symbol'] = i
        history = history.append(df)
        print(f"----------{i} complete----------")
    except:
        pass

history.to_csv('Output/1wk_stock_history_test.csv',index=False)

app = flask.Flask(__name__)

@app.route("/api")
def index():
    return "Complete"


if __name__ == "__main__":
    app.run(debug=True)