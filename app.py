from flask import Flask, render_template, request, redirect, flash
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
#
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file, output_notebook
import numpy as np
from datetime import datetime

app = Flask(__name__)
author = 'Created by Ashkan Farahani'

# get last three months for a drop down form variable
month = datetime.now().month
year  = datetime.now().year
months = np.arange(month,month-3,-1)
monthstr = ['January','February','March','April','May','June','July','August','September','October','November','December']
months_to_display = list(map(lambda x: monthstr[x-1], months))

@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html',months_to_display = months_to_display, year = year)

'''@app.route('/show',methods = ['POST','GET'])
def show():
    if request.method == 'GET':
        return f"Try going to '/form' to Submit the form"
    if request.method == 'POST':
        form_data = request.form
        # initializing alpha_vantage API
        alpha_vantage_api_key = "6ZXYDMYP08NQJ2XV"
        month_to_digit = {'Januray':1, 'Februray':2, 'March':3, 'April':4, 'May':5, 'June':6,
                        'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

        which_month = form_data.get('months')
        input_month = month_to_digit.get(which_month)
        ticker_name = form_data.get('stock')
        return render_template('show.html',form_data = form_data,which_month=which_month,input_month=input_month,ticker_name=ticker_name)'''

@app.route('/display',methods = ['POST','GET'])
def display():
    if request.method == 'GET':
        return f"Try going to '/form' to Submit the form"
    if request.method == 'POST':
        form_data = request.form
        # initializing alpha_vantage API
        alpha_vantage_api_key = "6ZXYDMYP08NQJ2XV"
        month_to_digit = {'Januray':1, 'Februray':2, 'March':3, 'April':4, 'May':5, 'June':6,
                        'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

        which_month = form_data.get('months')
        input_month = month_to_digit.get(which_month)
        ticker_name = form_data.get('stock')

        #Generate Alpha Vantage time series object
        ts = TimeSeries(key = alpha_vantage_api_key, output_format = 'pandas')
        data, meta_data = ts.get_daily_adjusted(ticker_name, outputsize = "compact")
        data['date_time'] = data.index
        cols = ['1. open', '2. high', '3. low', '4. close', '5. adjusted close', 'date_time']
        df = data[cols]
        df.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'date_time']
        dfc = df.copy()
        dfc.loc[:,'month'] = df.apply(lambda x: x['date_time'].month,axis=1)
        dfc.loc[:,'day']   = df.apply(lambda x: x['date_time'].day,axis=1)
        df_final = dfc[dfc['month']== input_month]
        df_final = df_final.sort_values(by='date_time',ascending=True)
        y = df_final['close'].values
        x = df_final['day'].values
        title = 'Close price of ' + ticker_name +' in month of '+ which_month
        fig = figure(plot_width= 600, plot_height=600)
        fig.line(x,y,legend=title)

        # grab the static resources
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        # render template
        script, div = components(fig)
        return render_template('display.html', form_data= form_data,
                                plot_script=script, plot_div=div,
                                js_resources=js_resources, css_resources=css_resources,
                                author = author)
if __name__ == '__main__':
    app.run(debug=True)
