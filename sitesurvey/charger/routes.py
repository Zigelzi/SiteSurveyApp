from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required

from sitesurvey import login_manager
from sitesurvey.charger.models import Charger
from sitesurvey.charger.forms import AddChargerForm

from sitesurvey.survey.models import Survey

bp_charger = Blueprint('charger', __name__)

@bp_charger.route('/chargers')
@login_required
def chargers():
    chargers = Charger.query.all()
    return render_template('chargers/chargers.html', title='Chargers', active='chargers', chargers=chargers)

@bp_charger.route('/chargers/charger/<int:charger_id>')
def charger(charger_id):
    charger = Charger.query.get_or_404(charger_id)
    return render_template('chargers/charger.html', charger=charger)

@bp_charger.route('/chargers/add_charger', methods=["GET", "POST"])
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
        return redirect(url_for('add_charger'))
    return render_template('chargers/add_charger.html', title='Add charger', form=form, active='add_charger')

@bp_charger.route('/chargers/view_chargers', methods=["GET"])
@login_required
def view_chargers():
    chargers = Charger.query.all()
    return render_template('chargers/view_chargers.html', title='View chargers', chargers=chargers)