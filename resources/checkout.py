from flask import Blueprint, render_template, redirect, url_for, session, request, abort
from db import db, Fragrances
import stripe, os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

bp = Blueprint("Checkout",__name__,url_prefix='/basket')

@bp.route('/')
def basket():
    products = []
    for id in session["Cart"]:
        product = db.session.execute(db.select(Fragrances).where(Fragrances.id==int(id))).scalar()
        products.append(product)

    return render_template('checkout/basket.html',fragrances=products)

@bp.route('/update',methods=["POST"])
def update_basket():
    if request.method == "POST":
        cart = session.get("Cart")
        for id in list(cart.keys()):
            qty = request.form.get(id)
            print(qty)
            if qty=='0':
                del cart[id]
            else:
                cart[id]['qty'] = int(qty)

        session['Cart'] = cart

        return redirect(url_for('Checkout.basket'))
    
@bp.route('/checkout')
def checkout_basket():
    line_items = []
    cart = session.get("Cart")
    if not cart:
        abort(400)
    for product_id in cart:
        product = db.get_or_404(Fragrances, int(product_id))
        item = {
            'price_data': {
                'product_data':{
                    'name':product.name
                },
                'unit_amount':int(product.price)*100,
                'currency': 'gbp',
            },
            'quantity':cart[product_id]['qty']
        }
        line_items.append(item)
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        payment_method_types=['card'],
        mode='payment',
        success_url=url_for('Checkout.success',_external=True),
        cancel_url=url_for('Checkout.cancel',_external=True)
    )

    return redirect(checkout_session.url)

@bp.route('/checkout/<int:product_id>/<int:qty>')
def checkout_item(product_id,qty):
    product = db.get_or_404(Fragrances,product_id)
    checkout_session = stripe.checkout.Session.create(
        line_items=[{
            'price_data':{
                'product_data':{
                    'name':product.name,
                },
                'unit_amount':int(product.price)*100,
                'currency':'gbp'
            },
            'quantity':qty,
        }],
        payment_method_types=['card'],
        mode='payment',
        success_url=url_for('Checkout.success',_external=True),
        cancel_url=url_for('Checkout.cancel',_external=True)
    )
    return redirect(checkout_session.url)


@bp.route('/success')
def success():
    del session['Cart']
    return render_template('checkout/success.html')

@bp.route('/cancel')
def cancel():
    return render_template('checkout/cancel.html')
