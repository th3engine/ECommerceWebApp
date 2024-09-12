from flask import Blueprint, render_template, redirect, url_for, flash, session
from db import db, Fragrances
from forms import ProductInput

bp = Blueprint("Home",__name__)

@bp.route('/')
def index():
    return render_template('home/home.html')

@bp.route('/about')
def about():
    return render_template('home/about.html')

@bp.route('/catalogue')
def catalogue():
    fragrances = db.session.execute(db.select(Fragrances)).scalars()

    return render_template('home/catalogue.html',fragrances=fragrances)

@bp.route('/catalogue/<int:product_id>',methods=["GET","POST"])
def product(product_id):
    fragrance = db.get_or_404(Fragrances,product_id)
    form = ProductInput()
    if form.validate_on_submit():
        if form.buy_now.data:
            return redirect(url_for('Checkout.checkout_item',product_id=product_id,qty=form.quantity.data))
        elif form.add_to_cart.data:
            session['next'] = url_for('Home.product',product_id=product_id)
            return redirect(url_for('Home.add_to_basket',product_id=product_id,qty=form.quantity.data))

    return render_template('home/product.html',fragrance=fragrance,form=form)

@bp.route('/catalogue/<int:product_id>/add/<int:qty>',defaults={"qty":1})
@bp.route('/catalogue/<int:product_id>/add/<int:qty>')
def add_to_basket(product_id,qty):
    fragrance = db.get_or_404(Fragrances,product_id)
    product_id = str(product_id)
    cart = session.get("Cart")
    if cart:
        try:
            cart[product_id]['qty'] += qty
        except KeyError:
            cart[product_id] = dict(name=fragrance.name,img=fragrance.img_url,qty=qty)
    else:
        cart = {
            product_id:dict(name=fragrance.name,img=fragrance.img_url,qty=1)
            }
    session["Cart"] = cart
    flash(f"{fragrance.name} - {qty} added to basket","light")
    return redirect(session.pop('next',None) or f"{url_for('Home.catalogue')}#{fragrance.id}")



