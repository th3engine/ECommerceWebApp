from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class ProductInput(FlaskForm):
    size = SelectField("Size",validators=[InputRequired()],choices=["Small","Medium","Large"])
    quantity = IntegerField("Quantity",default=1,render_kw={"min":1,"max":5},validators=[InputRequired(),NumberRange(1,5)])
    buy_now = SubmitField("Buy Now")
    add_to_cart = SubmitField("Add to Cart")