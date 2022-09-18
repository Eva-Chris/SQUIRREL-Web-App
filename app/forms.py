from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField,validators, ValidationError
 
class ContactForm(Form):
  name = StringField("Name" )
  email = StringField("Email")
  subject = StringField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")
