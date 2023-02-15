from flask import flash, json, make_response, redirect, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm, DiscoForm
from app.main.get_data import get_data

import pandas as pd

@bp.route("/", methods=["GET", "POST"])
def index():

    form = DiscoForm()

    if form.validate_on_submit():
        start_date = form.start_date-day.data
        print(f'routes start_date day: {start_date}')
        end_date = form.end_date.data
        print(f'routes end_date day: {end_date}')
        # code to get dataframe from BQ

        return redirect(url_for("example_form.html")) #set to the exampleform page while testing
    return render_template("example_form.html", form=form)

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
