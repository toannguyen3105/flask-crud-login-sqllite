from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp


class CustomLength(Length):
    def __call__(self, form, field):
        length = field.data and len(field.data) or 0
        if length >= self.min and (self.max == -1 or length <= self.max):
            return

        if self.message is not None:
            message = self.message

        elif self.max == -1:
            message = field.ngettext(
                "The field must have at least %(min)d character.",
                "The field must have at least %(min)d characteres.",
                self.min,
            )
        elif self.min == -1:
            message = field.ngettext(
                "The field cannot contain more than %(max)d character.",
                "The field cannot contain more than %(max)d characteres.",
                self.max,
            )
        elif self.min == self.max:
            message = field.ngettext(
                "The field must contain exactly %(max)d character.",
                "The field must contain exactly %(max)d characteres.",
                self.max,
            )
        else:
            message = field.gettext(
                "The field must contain between %(min)d and %(max)d characters."
            )

        raise ValidationError(message % dict(min=self.min, max=self.max, length=length))


passPattern = '[0-9]{6,12}'
badPassword = 'The password can only contain numbers, it must have a length of at least 6 digits.'


class RegistrationForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(message="You must enter a name."), CustomLength(min=5, max=25)],
                           description="user name")
    email = StringField('Full Name',
                        validators=[DataRequired(message="You must enter a full name."), CustomLength(min=6, max=25)],
                        description="email")
    password = PasswordField('Password', validators=[DataRequired(), Length(max=12),
                                                     Regexp(regex=passPattern, message=badPassword)])
    submit = SubmitField('Register')
