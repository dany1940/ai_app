"""First-revision

Revision ID: f0b5f544cb7c
Revises: d443e1c8f739
Create Date: 2024-06-27 20:32:25.601840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f0b5f544cb7c'
down_revision: Union[str, None] = 'd443e1c8f739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medication_request_tab')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medication_request_tab',
    sa.Column('medication_request_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('medication_code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('clinician_refrence', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('patient_refrence', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('prescription_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('start_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('end_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('frequency', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('ACTIVE', 'ON_HOLD', 'CANCELLED', 'COMPLETED', name='status'), server_default=sa.text("'ACTIVE'::status"), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['clinician_refrence'], ['clinician_tab.registration_id'], name='medication_request_tab_clinician_refrence_fkey'),
    sa.ForeignKeyConstraint(['patient_refrence'], ['patient_tab.registration_id'], name='medication_request_tab_patient_refrence_fkey'),
    sa.PrimaryKeyConstraint('medication_request_id', name='medication_request_tab_pkey')
    )
    # ### end Alembic commands ###