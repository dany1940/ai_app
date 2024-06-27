"""First-revision

Revision ID: 78aafab2560b
Revises:
Create Date: 2024-06-26 14:43:45.256473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision: str = '78aafab2560b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("CREATE EXTENSION ltree"))
    op.create_table('image_tab',
    sa.Column('image_id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('image_id')
    )
    op.create_table('organization_tab',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('profile_picture_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('path', sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
    sa.ForeignKeyConstraint(['profile_picture_id'], ['image_tab.image_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('institution_tab',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('contact_number', sa.String(length=255), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization_tab.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('clinician_tab',
    sa.Column('registration_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('gmc_number', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('mobile_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('mc_number', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('about', sa.TEXT(), nullable=True),
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('rating', sa.DOUBLE_PRECISION(), nullable=True),
    sa.Column('online_consultation', sa.Boolean(), nullable=True),
    sa.Column('online_consultation_fee', sa.DOUBLE_PRECISION(), nullable=True),
    sa.Column('online_consultation_duration', sa.SmallInteger(), nullable=True),
    sa.Column('clinician_code', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['institution_id'], ['institution_tab.id'], ),
    sa.PrimaryKeyConstraint('registration_id'),
    sa.UniqueConstraint('clinician_code')
    )
    op.create_table('contact_tab',
    sa.Column('contact', sa.TEXT(), nullable=False),
    sa.Column('contact_name', sa.TEXT(), nullable=False),
    sa.Column('institution_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['institution_id'], ['institution_tab.id'], ),
    sa.PrimaryKeyConstraint('contact', 'institution_id')
    )
    op.create_table('patient_tab',
    sa.Column('registration_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_code', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('is_smoker', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_armed_forces', sa.Boolean(), nullable=False),
    sa.Column('is_from_emergency_services', sa.Boolean(), nullable=False),
    sa.Column('is_from_abroad', sa.Boolean(), nullable=False),
    sa.Column('is_from_nhs', sa.Boolean(), nullable=False),
    sa.Column('emergency_contact_number', sa.String(), nullable=False),
    sa.Column('is_donor', sa.Boolean(), nullable=True),
    sa.Column('donor_organ', sa.String(), nullable=True),
    sa.Column('is_blood_donor', sa.Boolean(), nullable=True),
    sa.Column('patient_medical_history', sa.TEXT(), nullable=True),
    sa.Column('blood_type', sa.Enum('A_POSITIVE', 'A_NEGATIVE', 'B_POSITIVE', 'B_NEGATIVE', 'AB_POSITIVE', 'AB_NEGATIVE', 'O_POSITIVE', 'O_NEGATIVE', name='BloodGroupType'), server_default='A_POSITIVE', nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='GenderType'), server_default='FEMALE', nullable=False),
    sa.Column('title', sa.Enum('MR', 'MRS', 'MISS', 'DR', 'PROF', 'REV', name='TytleType'), server_default='MR', nullable=False),
    sa.Column('is_alcohool_drinker', sa.Boolean(), nullable=False),
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institution_tab.id'], ),
    sa.PrimaryKeyConstraint('registration_id'),
    sa.UniqueConstraint('patient_code')
    )
    op.create_table('user_tab',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('pword_hash', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('can_edit', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institution_tab.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization_tab.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('clinical_trial_tab',
    sa.Column('clinical_trial_id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('clinical_trial_code', sa.String(), nullable=False),
    sa.Column('clinician_refrence', sa.Integer(), nullable=True),
    sa.Column('patient_refrence', sa.Integer(), nullable=True),
    sa.Column('institution_refrence', sa.Integer(), nullable=True),
    sa.Column('reason', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['clinician_refrence'], ['clinician_tab.registration_id'], ),
    sa.ForeignKeyConstraint(['institution_refrence'], ['institution_tab.id'], ),
    sa.ForeignKeyConstraint(['patient_refrence'], ['patient_tab.registration_id'], ),
    sa.PrimaryKeyConstraint('clinical_trial_id'),
    sa.UniqueConstraint('clinical_trial_code')
    )
    op.create_table('medication_request_tab',
    sa.Column('medication_request_id', sa.String(), nullable=False),
    sa.Column('medication_code', sa.String(), nullable=False),
    sa.Column('clinician_refrence', sa.Integer(), nullable=True),
    sa.Column('patient_refrence', sa.Integer(), nullable=True),
    sa.Column('reason', sa.TEXT(), nullable=True),
    sa.Column('prescription_date', sa.DateTime(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('frequency', sa.SmallInteger(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'ON_HOLD', 'CANCELLED', 'COMPLETED', name='status'), server_default='ACTIVE', nullable=False),
    sa.ForeignKeyConstraint(['clinician_refrence'], ['clinician_tab.registration_id'], ),
    sa.ForeignKeyConstraint(['patient_refrence'], ['patient_tab.registration_id'], ),
    sa.PrimaryKeyConstraint('medication_request_id')
    )
    op.create_table('prescription_tab',
    sa.Column('prescription_id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('prescription_code', sa.String(), nullable=False),
    sa.Column('clinician_refrence', sa.Integer(), nullable=True),
    sa.Column('patient_refrence', sa.Integer(), nullable=True),
    sa.Column('reason', sa.TEXT(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('frequency', sa.SmallInteger(), nullable=False),
    sa.Column('prescription_status', sa.Enum('ACTIVE', 'ON_HOLD', 'CANCELLED', name='prescription_status'), server_default='ACTIVE', nullable=False),
    sa.ForeignKeyConstraint(['clinician_refrence'], ['clinician_tab.registration_id'], ),
    sa.ForeignKeyConstraint(['patient_refrence'], ['patient_tab.registration_id'], ),
    sa.PrimaryKeyConstraint('prescription_id'),
    sa.UniqueConstraint('prescription_code')
    )
    op.create_table('apointment_tab',
    sa.Column('apointment_id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('apointment_code', sa.String(), nullable=False),
    sa.Column('clinician_refrence', sa.Integer(), nullable=True),
    sa.Column('patient_refrence', sa.Integer(), nullable=True),
    sa.Column('intitution_refrence', sa.Integer(), nullable=True),
    sa.Column('clincal_trial_id', sa.Integer(), nullable=True),
    sa.Column('reason', sa.TEXT(), nullable=True),
    sa.Column('creted_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('apointment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['clincal_trial_id'], ['clinical_trial_tab.clinical_trial_id'], ),
    sa.ForeignKeyConstraint(['clinician_refrence'], ['clinician_tab.registration_id'], ),
    sa.ForeignKeyConstraint(['intitution_refrence'], ['institution_tab.id'], ),
    sa.ForeignKeyConstraint(['patient_refrence'], ['patient_tab.registration_id'], ),
    sa.PrimaryKeyConstraint('apointment_id'),
    sa.UniqueConstraint('apointment_code'),
    sa.UniqueConstraint('apointment_date')
    )
    op.create_table('medication_tab',
    sa.Column('medication_name', sa.String(), nullable=False),
    sa.Column('medication_reference', sa.String(), nullable=False),
    sa.Column('code_name', sa.String(), nullable=False),
    sa.Column('international_code_name', sa.String(), nullable=True),
    sa.Column('strength_value', sa.SmallInteger(), nullable=True),
    sa.Column('strenght_unit', sa.DOUBLE_PRECISION(), nullable=True),
    sa.Column('form', sa.Enum('POWDER', 'TABLET', 'CAPSULE', 'SYRUP', name='formtype'), server_default='CAPSULE', nullable=False),
    sa.Column('brand_name', sa.String(), nullable=True),
    sa.Column('active_ingredient_name', sa.String(), nullable=True),
    sa.Column('excipient_name', sa.String(), nullable=True),
    sa.Column('other_name_of_active_ingredient', sa.String(), nullable=True),
    sa.Column('abbreviated_name_of_active_ingredient', sa.String(), nullable=True),
    sa.Column('chemical_formula', sa.String(), nullable=True),
    sa.Column('peculiar_part_of_drug', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('smell', sa.String(), nullable=True),
    sa.Column('taste', sa.String(), nullable=True),
    sa.Column('usage_of_excipient', sa.String(), nullable=True),
    sa.Column('indications', sa.String(), nullable=True),
    sa.Column('contraindications', sa.String(), nullable=True),
    sa.Column('is_allowed_for_children', sa.Boolean(), nullable=True),
    sa.Column('medication_category', sa.String(), nullable=True),
    sa.Column('medication_sub_category', sa.String(), nullable=True),
    sa.Column('medication_type', sa.String(), nullable=True),
    sa.Column('frequency', sa.SmallInteger(), nullable=True),
    sa.Column('dosage', sa.String(), nullable=True),
    sa.Column('side_effects', sa.String(), nullable=True),
    sa.Column('storage', sa.String(), nullable=True),
    sa.Column('medication_image', sa.Integer(), nullable=True),
    sa.Column('is_fda_approved', sa.Boolean(), nullable=True),
    sa.Column('is_nhs_approved', sa.Boolean(), nullable=True),
    sa.Column('is_emergency_medicine', sa.Boolean(), nullable=True),
    sa.Column('is_controlled_drug', sa.Boolean(), nullable=True),
    sa.Column('is_generic', sa.Boolean(), nullable=True),
    sa.Column('is_over_the_counter', sa.Boolean(), nullable=True),
    sa.Column('is_herbal', sa.Boolean(), nullable=True),
    sa.Column('is_homeopathic', sa.Boolean(), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.Column('is_restricted', sa.Boolean(), nullable=True),
    sa.Column('is_unlicensed', sa.Boolean(), nullable=True),
    sa.Column('is_orphan_drug', sa.Boolean(), nullable=True),
    sa.Column('is_biological', sa.Boolean(), nullable=True),
    sa.Column('is_trial_drug', sa.Boolean(), nullable=True),
    sa.Column('is_medical_gas', sa.Boolean(), nullable=True),
    sa.Column('is_medical_radioisotope', sa.Boolean(), nullable=True),
    sa.Column('is_medical_radioactive', sa.Boolean(), nullable=True),
    sa.Column('prescription_refrence', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medication_image'], ['image_tab.image_id'], ),
    sa.ForeignKeyConstraint(['prescription_refrence'], ['prescription_tab.prescription_id'], ),
    sa.PrimaryKeyConstraint('medication_reference'),
    sa.UniqueConstraint('code_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medication_tab')
    op.drop_table('apointment_tab')
    op.drop_table('prescription_tab')
    op.drop_table('medication_request_tab')
    op.drop_table('clinical_trial_tab')
    op.drop_table('user_tab')
    op.drop_table('patient_tab')
    op.drop_table('contact_tab')
    op.drop_table('clinician_tab')
    op.drop_table('institution_tab')
    op.drop_table('organization_tab')
    op.drop_table('image_tab')
    # ### end Alembic commands ###
