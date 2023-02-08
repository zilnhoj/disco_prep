from flask import flash, json, make_response, redirect, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm, DiscoForm
from app.main.get_data import get_data

import pandas as pd


@bp.route("/", methods=["GET", "POST"])
def index():

    disco_data_form = DiscoForm()
    if disco_data_form.validate_on_submit():
        # if request.method == "POST":
        # start_date = request.form.values()
        # end_date = request.form.values()
        print(f'request.form.values - {request.form.values()}')

        # cir_date_ls = [x for x in cir_date]
        # g.cir_date = f'{cir_date_ls[0]}-{cir_date_ls[1]}-{cir_date_ls[2]}'
        # print(f'value for date {g.cir_date}')
            # return render_template("choose-circuit.html", cir_date=g.cir_date)
            # return render_template("choose-circuit.html")


        # df = get_data(start_date, end_date, desiredPage)
        return redirect(url_for("example_form.html"))
    return render_template("example_form.html", form=disco_data_form)

def results():
    return render_template("results.html", form=disco_data_form)
@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


@bp.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no", "analytics": "no"}

    if form.validate_on_submit():
        # Update cookies policy consent from form data
        cookies_policy["functional"] = form.functional.data
        cookies_policy["analytics"] = form.analytics.data

        # Create flash message confirmation before rendering template
        flash("You’ve set your cookie preferences.", "success")

        # Create the response so we can set the cookie before returning
        response = make_response(render_template("cookies.html", form=form))

        # Set cookies policy for one year
        response.set_cookie("cookies_policy", json.dumps(cookies_policy), max_age=31557600)
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios to current consent
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
        else:
            # If conset not previously set, use default "no" policy
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
    return render_template("cookies.html", form=form)


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")
#
#
# @bp.app_errorhandler(HTTPException)
# def http_exception(error):
#     return render_template(f"{error.code}.html"), error.code
#
#
# @bp.app_errorhandler(CSRFError)
# def csrf_error(error):
#     flash("The form you were submitting has expired. Please try again.")
#     return redirect(request.full_path)
