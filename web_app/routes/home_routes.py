from flask import Blueprint, render_template, Response, request, redirect, flash
from datetime import date
import matplotlib.pyplot as plt

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
                return render_template("pricefind.html", results2=results2)