"""empty message

Revision ID: 01fc813986e3
Revises: 
Create Date: 2019-08-30 09:32:41.030840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01fc813986e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charger',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=30), nullable=False),
    sa.Column('model', sa.String(length=30), nullable=False),
    sa.Column('product_no', sa.String(length=30), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('type_of_outlet', sa.String(length=10), nullable=False),
    sa.Column('no_of_outlets', sa.Integer(), nullable=True),
    sa.Column('dc_ac', sa.String(length=2), nullable=False),
    sa.Column('communication', sa.String(length=20), nullable=False),
    sa.Column('mounting_wall', sa.Boolean(), nullable=False),
    sa.Column('mounting_ground', sa.Boolean(), nullable=False),
    sa.Column('max_power', sa.Float(), nullable=False),
    sa.Column('mcb', sa.Boolean(), nullable=False),
    sa.Column('rcd_typea', sa.Boolean(), nullable=False),
    sa.Column('rcd_typeb', sa.Boolean(), nullable=False),
    sa.Column('automatic_rcd', sa.Boolean(), nullable=False),
    sa.Column('pwr_outage_eq', sa.Boolean(), nullable=False),
    sa.Column('mid_meter', sa.Boolean(), nullable=False),
    sa.Column('mid_readable', sa.Boolean(), nullable=False),
    sa.Column('max_cable_d', sa.Integer(), nullable=False),
    sa.Column('cable_cu_allowed', sa.Boolean(), nullable=False),
    sa.Column('cable_al_allowed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_no')
    )
    op.create_table('orgtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('productcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('workorder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('requested_date', sa.DateTime(), nullable=True),
    sa.Column('ready_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('public_chargers', sa.Integer(), nullable=False),
    sa.Column('public_installation_location', sa.Text(), nullable=False),
    sa.Column('public_charging_power', sa.Float(), nullable=False),
    sa.Column('private_chargers', sa.Integer(), nullable=False),
    sa.Column('private_installation_location', sa.Text(), nullable=False),
    sa.Column('private_charging_power', sa.Float(), nullable=False),
    sa.Column('installation_type', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_name', sa.String(length=100), nullable=False),
    sa.Column('org_number', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=10), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('org_number')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_number', sa.String(length=8), nullable=False),
    sa.Column('product_name', sa.String(length=30), nullable=False),
    sa.Column('unit_of_material', sa.String(length=8), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('product_category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_category'], ['productcategory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_number')
    )
    op.create_table('workorderattachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('attachment_filename', sa.String(length=15), nullable=False),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contactperson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('parent_org', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_org'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lineitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discount', sa.DECIMAL(precision=3, scale=2), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org_type',
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['orgtype.id'], )
    )
    op.create_table('product_category',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('product_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_category_id'], ['productcategory.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], )
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('installation_method', sa.String(length=30), nullable=False),
    sa.Column('concrete_foundation', sa.Boolean(), nullable=True),
    sa.Column('grid_connection', sa.Integer(), nullable=True),
    sa.Column('grid_cable', sa.String(length=15), nullable=True),
    sa.Column('max_power', sa.Float(), nullable=True),
    sa.Column('consumption_fuse', sa.Integer(), nullable=True),
    sa.Column('maincabinet_rating', sa.Integer(), nullable=True),
    sa.Column('empty_fuses', sa.Boolean(), nullable=True),
    sa.Column('number_of_slots', sa.Integer(), nullable=True),
    sa.Column('signal_strength', sa.Float(), nullable=True),
    sa.Column('installation_location', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=10), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.Column('coordinate_lat', sa.Float(), nullable=True),
    sa.Column('coordinate_long', sa.Float(), nullable=True),
    sa.Column('workorder_id', sa.Integer(), nullable=True),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.ForeignKeyConstraint(['workorder_id'], ['workorder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('survey_contact_person',
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contactperson.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], )
    )
    op.create_table('surveypicture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('picture_filename', sa.String(length=15), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('surveypicture')
    op.drop_table('survey_contact_person')
    op.drop_table('location')
    op.drop_table('survey')
    op.drop_table('user')
    op.drop_table('product_category')
    op.drop_table('org_type')
    op.drop_table('lineitem')
    op.drop_table('contactperson')
    op.drop_table('workorderattachment')
    op.drop_table('product')
    op.drop_table('organization')
    op.drop_table('comment')
    op.drop_table('workorder')
    op.drop_table('productcategory')
    op.drop_table('orgtype')
    op.drop_table('charger')
    # ### end Alembic commands ###