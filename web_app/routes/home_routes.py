from flask import Blueprint, render_template, Response, request, redirect
import matplotlib.pyplot as plt

from app.pricefind import pricefind

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
        results2 = pricefind(symbol,sdate,edate)
        # plt.plot[results2['Date'], results2['Close']]
        # plt.show()
        return render_template("pricefind.html", results2=results2)