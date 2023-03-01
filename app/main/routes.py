from flask import flash, json, make_response, render_template, request, url_for, Response, redirect
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.main import bp
from app.main.forms import CookiesForm, DiscoForm
from app.main.get_data import get_summary_data, get_csv_data
from datetime import datetime
import pandas as pd

@bp.route("/", methods=["GET", "POST"])
def index():

    form = DiscoForm()

    if form.validate_on_submit():
        desired_url = form.desired_url.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        df = get_summary_data(start_date, end_date, desired_url)

        top_ten_df = df.head(10)

        csv_link = url_for('main.csv_results', start_date=datetime.strftime(start_date, '%Y%m%d'), end_date=datetime.strftime(end_date, '%Y%m%d'), desired_url=desired_url)

        return render_template("results.html", tables=top_ten_df.values.tolist(), df_header=top_ten_df.columns.values, csv_link=csv_link, form=form)
    return render_template("example_form.html", form=form)

@bp.route("/results", methods=["GET"])
def results():
    form = DiscoForm()
    return render_template("results.html", form=form)

@bp.route("/csv_results", methods=["GET"])
def csv_results():
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    desired_url = request.args['desired_url']

    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')

    df = get_csv_data(start_date, end_date, desired_url)

    response = Response(df.to_csv())
    response.headers["Content-Disposition"] = "attachment"
    response.headers["Content-Type"] = "text/csv"
    return response

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


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    return render_template(f"{error.code}.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
