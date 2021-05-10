from flask import Blueprint, render_template, Response, request, redirect, flash, session
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
import pandas as pd
import base64


from app.pricefind import pricefind
from app.sqlupload2 import sqlupload
from app.pricefind import tickercheck
from app.pricefind import datecheck
from app.pricefind import stockinfo

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/pricefind",methods=['GET','POST'])
def pfind():
    if request.method == 'GET':
        return render_template("pricefind.html")
    else:
        symbol = dict(request.form)
        sdate = symbol['sdate']
        edate = symbol['edate']
        symbol = symbol['ticker'].upper()
        if tickercheck(symbol) == False:
            flash("Invalid Ticker", "danger")
            return render_template("pricefind.html")
        elif sdate>edate:
            flash("End Date Greater Than Start Date", "danger")
            return render_template("pricefind.html")
        elif sdate>str(date.today()):
            flash("Start Date In The Future", "danger")
            return render_template("pricefind.html")
        elif edate>str(date.today()):
            flash("End Date In The Future", "danger")
            return render_template("pricefind.html")
        else:
            try:
                stockinfo(symbol)
            except KeyError:
                flash("Invalid Ticker", "danger")
                return render_template("pricefind.html")
            else:
                results2 = sqlupload(symbol,sdate,edate)
                stkinfo = stockinfo(symbol)
                fig = Figure()
                axis = fig.add_subplot(1, 1, 1)
                axis.set_xlabel("Date")
                axis.set_ylabel("Price")
                axis.grid()
                axis.plot(results2['Date'], results2['Close'], linestyle="--")
                # Convert plot to PNG image
                pngImage = io.BytesIO()
                FigureCanvas(fig).print_png(pngImage)
    
                # Encode PNG image to base64 string
                pngImageB64String = "data:image/png;base64,"
                pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

                results2 = results2.to_dict('records')
                return render_template("pricefind.html", results2=results2, stkinfo=stkinfo, image=pngImageB64String)

@home_routes.route("/pricefind2",methods=['GET','POST'])
def pfind2():
    if request.method == 'GET':
        return render_template("pricefind2.html")
    else:
        symbol = dict(request.form)
        sdate = symbol['sdate']
        edate = symbol['edate']
        symbol1 = symbol['ticker'].upper()
        symbol2 = symbol['ticker2'].upper()
        if tickercheck(symbol1) == False:
            flash("Invalid Ticker", "danger")
            return render_template("pricefind2.html")
        elif sdate>edate:
            flash("End Date Greater Than Start Date", "danger")
            return render_template("pricefind2.html")
        elif sdate>str(date.today()):
            flash("Start Date In The Future", "danger")
            return render_template("pricefind2.html")
        elif edate>str(date.today()):
            flash("End Date In The Future", "danger")
            return render_template("pricefind2.html")
        else:
            try:
                stockinfo(symbol1)
            except KeyError:
                flash("Invalid Ticker", "danger")
                return render_template("pricefind2.html")
            else:
                results2 = sqlupload(symbol1,sdate,edate)
                results3 = sqlupload(symbol2,sdate,edate)
                stkinfo = stockinfo(symbol1)
                stkinfo2 = stockinfo(symbol2)
                fig = Figure()
                axis = fig.add_subplot(1, 1, 1)
                axis.set_xlabel("Date")
                axis.set_ylabel("Price")
                axis.grid()
                axis2 = axis.twinx()
                axis.plot(results2['Date'], results2['Close'], label=symbol1, linestyle="--", color="b")
                axis2.plot(results3['Date'], results3['Close'], label=symbol2, linestyle="--", color="orange")
                axis.legend(bbox_to_anchor=(0.2, 1.0))
                axis2.legend(bbox_to_anchor=(0.2, 0.9))
                # Convert plot to PNG image
                pngImage = io.BytesIO()
                FigureCanvas(fig).print_png(pngImage)
    
                # Encode PNG image to base64 string
                pngImageB64String = "data:image/png;base64,"
                pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

                results2 = results2.to_dict('records')
                results3 = results3.to_dict('records')
                return render_template("pricefind2.html", results2=results2, results3=results3, stkinfo=stkinfo, stkinfo2=stkinfo2, image=pngImageB64String)