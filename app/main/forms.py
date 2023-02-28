from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput, GovDateInput
from wtforms.fields import RadioField, SubmitField, StringField, DateField
from wtforms.validators import InputRequired, Length, Optional, DataRequired
from datetime import date, datetime




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
    def __validate_dt(form, field):
        print(f'data in field: {field}')
        print(f'data in form.start_date.data: {form.start_date.data}')
        dt_ls = field.raw_data
        dt_str = "".join(dt_ls).strip()
        date_dt = datetime.strptime(dt_str, "%d%m%Y").date()
        data = date_dt
        print(f'date_dt - {date_dt}')
        print(f'data - {data}')
        if not date_dt:
            raise ValidationError('not a valid date buddy')
        else:
            print(f'in else statement {data}')
            # assert date_dt
            return data

    desired_url = StringField(
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
                format = "%d %m %Y",
                validators=[
                    InputRequired()
                ]
            )
    print(f'start_date_date:- {start_date}')

    end_date = DateField(
                "Please enter the end date for the period you need data for",
                widget=GovDateInput(),
                format="%d %m %Y",
                validators=[
                    InputRequired()
                ]
            )


    submit = SubmitField("Continue", widget=GovSubmitInput())

