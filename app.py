import datetime

import pandas as pd
import quandl
from bokeh.charts import TimeSeries
from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    stock_ticker = StringField(u'Stock Ticker', validators=[DataRequired()])
    submit = SubmitField('Submit')


# # Validate stock ticker (initially from user input)  TODO: Move to web form
#
# stock_ticker = 'AAPL'        # need to request from user and validate TODO: Put back to null string
#
# while stock_ticker not in stock_code_list:
#     stock_ticker = raw_input('Enter stock ticker: ')
#     stock_ticker = 'AAPL' # TODO: For testing
#     # TODO: get stock ticker from web interface

# TODO: Put dynamic link on page to look up stock info after producing chart



# TODO: Simple webpage requirements
# INPUT: User choice of stock ticker
# OUTPUT: Plots closing price data for the last month

# TODO: Also put link to stock e.g. http://www.nasdaq.com/symbol/aapl


def main():
    return

app = Flask(__name__)
app.secret_key = 'mjb_verylongsecretkey'
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    stock_ticker = None
    form = MyForm()

    if not form.validate_on_submit():  # TODO: Need to remove not here - don't understand this
        stock_ticker = form.stock_ticker.data

        # Load list of stock codes (currently static CSV version downloaded from Quandl

        stock_codes = pd.read_csv('WIKI-datasets-codes.csv', header=None)
        stock_code_list = stock_codes[0].tolist()
        stock_code_list = [w.replace('WIKI/', '') for w in stock_code_list]

        if stock_ticker not in stock_code_list:
            stock_ticker = 'AAPL'

        quandl_reference = 'WIKI/' + stock_ticker
        nasdaq_url = 'http://www.nasdaq.com/symbol/' + stock_ticker

        # Determine period for last month

        end_date = datetime.date.today().replace(day=datetime.date.today().day - 1)
        start_date = end_date.replace(month=end_date.month - 1)

        # Get price data from Quandl
        try:
            quandl.ApiConfig.api_key = 'Mror8Ww3qg5e947A7Fhj'
            data = quandl.get(quandl_reference, start_date=start_date, end_date=end_date, returns='pandas')
        except:
            print
            print 'ERROR: Unable to query Quandl data - check internet connection?'
            quit()

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        # Plotting
        p = TimeSeries(data, y='Close', title=stock_ticker, ylabel='Price (USD / share)', xlabel='Date')
        script, div = components(p)

    form.stock_ticker.data = stock_ticker

    return render_template('app_plotter.html',
                           form=form,
                           name=stock_ticker,
                           plot_script=script,
                           plot_div=div,
                           js_resources=js_resources,
                           css_resources=css_resources)


if __name__ == '__main__':
    main()
    app.run(port=33507)