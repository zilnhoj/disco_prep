from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput, GovDateInput
from wtforms.fields import RadioField, SubmitField, StringField, DateField
from wtforms.validators import InputRequired, Length
import datetime


class CookiesForm(FlaskForm):
    functional = RadioField(
        "Do you want to accept functional cookies?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select yes if you want to accept functional cookies")],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    analytics = RadioField(
        "Do you want to accept analytics cookies?",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Select yes if you want to accept analytics cookies")],
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    save = SubmitField("Save cookie settings", widget=GovSubmitInput())

class DiscoForm(FlaskForm):
    disco_form = StringField(
        "Desired URL",
        widget=GovTextInput(),
        validators=[
            InputRequired(message="Enter a desired url"),
            Length(max=256, message="URL must be 256 characters or fewer")
        ],
        description="Must include the / at the start of the URL",
    )
    start_date = DateField(
                "Please enter the start date for the period you need data for",
                widget=GovDateInput(),
                validators=[
                    InputRequired(message="Select the start date")
                ]
            )
    end_date = DateField(
                "Please enter the end date for the period you need data for",
                widget=GovDateInput(),
                validators=[
                    InputRequired(message="Select the end date")]
            )

    submit = SubmitField("Continue", widget=GovSubmitInput())