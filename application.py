from flask import Flask, flash, jsonify, redirect, render_template, request, session
from helpers import fair_value_function
#from helpers import apology, #ticker(used for determining if the ticker is even available or not), fair_value


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/methodology')
def methodology():
    return render_template("methodology.html")


@app.route('/calculator', methods = ["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template("calculator.html")
    else:
        list_specifics = []
        list_specifics.append(float(request.form.get("term")))
        list_specifics.append(float(request.form.get("strike_price")))
        list_specifics.append(float(request.form.get("stock_price")))
        list_specifics.append(float(request.form.get("risk_free_rate")))
        list_specifics.append(float(request.form.get("number_of_options")))
        list_specifics.append(float(request.form.get("dividend_yield_percentage")))
        list_specifics.append(request.form.get("Ticker"))
        list_specifics.append(int(request.form.get("Start_date_day")))
        list_specifics.append(int(request.form.get("Start_date_month")))
        list_specifics.append(int(request.form.get("Start_date_year")))
        list_specifics.append(int(request.form.get("end_date_day")))
        list_specifics.append(int(request.form.get("end_date_month")))
        list_specifics.append(int(request.form.get("end_date_year")))

        fair_value = fair_value_function(list_specifics)

        if fair_value == "error":
            return render_template("error.html")
        else:
            return render_template("results.html", fair_value = fair_value)
            
