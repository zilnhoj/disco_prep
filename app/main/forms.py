from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput, GovDateInput
from wtforms.fields import RadioField, SubmitField, StringField, DateField
from wtforms.validators import InputRequired, Length, Optional, DataRequired
from datetime import date


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
    # def __validate(form, field):
    #     #print(valueLisst)
    #     print(f'field data {field.errors}')
    #     print(f'form data {form.end_date.data}')

    def __validate(form, field):
        print(f'field ---> {field}')
        # if valuelist:
        #     date_str = ' '.join(valuelist).strip()
        #     print(date_str)
        print(f'field data {field.data}')
        print(f'form data {form.data}')

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
                format='%d/%m/%Y',
                validators=[
                    InputRequired(message="Select the start date"),
                    __validate
                ]
            )

    end_date = DateField(
                "Please enter the end date for the period you need data for",
                widget=GovDateInput(),
                format='%d/%m/%Y',
                validators=[
                    InputRequired(message="Select the end date"),
                    __validate
                ]
            )


        # date_str = (f'{field.end_date-day}, {field.end_date-month}, {field.end_date-year}')
        # datetime.datetime.strptime(date_str, '%d%m%Ys').date()

    submit = SubmitField("Continue", widget=GovSubmitInput())

