from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required

from sitesurvey import login_manager, db
from sitesurvey.product.models import Charger, Product, Productcategory
from sitesurvey.product.forms import AddChargerForm, AddProductForm, AddProductCategoryForm

from sitesurvey.survey.models import Survey

bp_product = Blueprint('product', __name__)

@bp_product.route('/products/chargers')
@login_required
def chargers():
    chargers = Charger.query.all()
    return render_template('product/chargers.html', title='Chargers', active='chargers', chargers=chargers)

@bp_product.route('/products/charger/<int:charger_id>')
@login_required
def charger(charger_id):
    charger = Charger.query.get_or_404(charger_id)
    return render_template('product/charger.html', charger=charger)

@bp_product.route('/products/add_charger', methods=["GET", "POST"])
@login_required
def add_charger():
    form = AddChargerForm()
    if form.validate_on_submit():

        # Take the form input and create db entry and commit it
        charger = Charger(manufacturer=form.manufacturer.data,
                        model=form.model.data,
                        product_no=form.product_no.data,
                        price=form.price.data,
                        type_of_outlet=form.type_of_outlet.data,
                        no_of_outlets=form.no_of_outlets.data,
                        dc_ac=form.dc_ac.data,
                        communication=form.communication.data,
                        mounting_wall=form.mounting_wall.data,
                        mounting_ground=form.mounting_ground.data,
                        max_power=form.max_power.data,
                        mcb=form.mcb.data,
                        rcd_typea=form.rcd_typea.data,
                        rcd_typeb=form.rcd_typeb.data,
                        automatic_rcd=form.automatic_rcd.data,
                        pwr_outage_eq=form.pwr_outage_eq.data,
                        mid_meter=form.mid_meter.data,
                        mid_readable=form.mid_readable.data,
                        max_cable_d=form.max_cable_d.data,
                        cable_cu_allowed=form.cable_cu_allowed.data,
                        cable_al_allowed=form.cable_al_allowed.data)
        db.session.add(charger)
        db.session.commit()
        flash(f'Charger has been created in the database.', 'success')
        return redirect(url_for('product.charger', charger_id=charger.id))
    return render_template('product/add_charger.html', title='Add charger', form=form, active='add_charger')

@bp_product.route('/products/chargers/view_chargers', methods=["GET"])
@login_required
def view_chargers():
    chargers = Charger.query.all()
    return render_template('product/view_chargers.html', title='View chargers', chargers=chargers)

@bp_product.route('/products/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()

    if form.validate_on_submit() and request.method == 'POST':
        product = Product(product_number = form.product_number.data,
                          product_name = form.product_name.data,
                          unit_of_material = form.unit_of_material.data,
                          price = form.price.data,
                          product_category = form.product_category.data)
        db.session.add(product)
        db.session.commit()
        flash(f'Product has been created in the database.', 'success')
        return redirect(url_for('product.product', product_id=product.id))
    return render_template('product/add_product.html', title='Add product', form=form)

@bp_product.route('/products/product/<int:product_id>')
@login_required
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/product.html', product=product)

@bp_product.route('/products/add_product_category', methods=['GET', 'POST'])
@login_required
def add_product_category():
    form = AddProductCategoryForm()
    
    if form.validate_on_submit() and request.method == 'POST':
        product_category = Productcategory(title = form.title.data,
                                          description = form.description.data)
        db.session.add(product_category)
        db.session.commit()
        flash(f'Product category has been created in the database.', 'success')
        return redirect(url_for('product.product_category', product_category_id = product_category.id))
    return render_template('product/add_product_category.html', title='Add product category', form=form)

@bp_product.route('/products/product_category/<int:product_category_id>')
@login_required
def product_category(product_category_id):
    product_category = Productcategory.query.get_or_404(product_category_id)
    return render_template('product/product_category.html', product_category=product_category)
