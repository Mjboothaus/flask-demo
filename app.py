from datetime import datetime, timedelta

import pandas as pd
import quandl
from bokeh.charts import TimeSeries
from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class StockChoiceForm(FlaskForm):
    # TODO: Improve validation
    stock_ticker = StringField(u'Stock Ticker', validators=[DataRequired()])
    submit = SubmitField('Submit')


def main():
    return


app = Flask(__name__)
app.secret_key = 'mjboothaus_42verylongsecretkey'
Bootstrap(app)  # TODO: Does Bootstrap() do anything useful here?


@app.route('/', methods=['GET', 'POST'])
def index():
    stock_ticker = 'AAPL'  # Default initial value (Apple)
    form = StockChoiceForm()
    return render_template('app_choose_stock.html', form=form)


@app.route('/produce_plot', methods=['POST'])
def produce_plot():
    stock_ticker = request.form.get('stock_ticker')

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Load list of stock codes (currently static CSV version downloaded from Quandl
    # TODO: Probably best to get a list of stock symbols dynamically

    stock_codes = pd.read_csv('WIKI-datasets-codes.csv', header=None)
    stock_code_list = stock_codes[0].tolist()
    stock_code_list = [w.replace('WIKI/', '') for w in stock_code_list]

    if stock_ticker not in stock_code_list:  # TODO - Implement client-side validation of stock symbol - see StockChoiceForm validators
        stock_ticker = 'AAPL'

    quandl_reference = 'WIKI/' + stock_ticker
    nasdaq_url = 'http://www.nasdaq.com/symbol/' + stock_ticker

    # Determine period for last month

    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=31)  # just look at last 30 days for now (not exactly 1 month)

    # Get price data from Quandl

    data = None
    try:
        quandl.ApiConfig.api_key = 'Mror8Ww3qg5e947A7Fhj'
        data = quandl.get(quandl_reference, start_date=start_date, end_date=end_date, returns='pandas')
    except:
        print
        print 'ERROR: Unable to query Quandl data - check internet connection?'
        quit()  # TODO: Need to exit more gracefully

    # Plotting

    p = TimeSeries(data, y='Close', title=stock_ticker, ylabel='Price (USD / share)', xlabel='Date')
    script, div = components(p)

    return render_template('app_plotter.html',
                           name=stock_ticker,
                           plot_script=script,
                           plot_div=div,
                           nasdaq_url=nasdaq_url,
                           js_resources=js_resources,
                           css_resources=css_resources)


if __name__ == '__main__':
    main()
    app.run(port=33507)