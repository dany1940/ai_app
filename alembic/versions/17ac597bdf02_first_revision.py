"""First-revision

Revision ID: 17ac597bdf02
Revises: 
Create Date: 2024-06-20 21:22:27.114993

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17ac597bdf02"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clinician_tab",
        sa.Column("registration_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("registration_id"),
    )
    op.create_table(
        "medication_tab",
        sa.Column("medication_reference", sa.String(), nullable=False),
        sa.Column("code_name", sa.String(), nullable=False),
        sa.Column("international_code_name", sa.String(), nullable=True),
        sa.Column("strength_value", sa.SmallInteger(), nullable=True),
        sa.Column("strenght_unit", sa.DOUBLE_PRECISION(), nullable=True),
        sa.Column(
            "form",
            sa.Enum("POWDER", "TABLET", "CAPSULE", "SYRUP", name="formtype"),
            server_default="CAPSULE",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("medication_reference"),
    )
    op.create_table(
        "patient_tab",
        sa.Column("registration_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column(
            "gender",
            sa.Enum("MALE", "FEMALE", "PSI", "BAR", "KPA", name="GenderType"),
            server_default="FEMALE",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("registration_id"),
    )
    op.create_table(
        "medication_request_tab",
        sa.Column("medication_request_id", sa.String(), nullable=False),
        sa.Column("clinician_refrence", sa.Integer(), nullable=True),
        sa.Column("patient_refrence", sa.Integer(), nullable=True),
        sa.Column("medication_reference", sa.String(), nullable=True),
        sa.Column("reason", sa.TEXT(), nullable=True),
        sa.Column("prescription_date", sa.DateTime(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("frequency", sa.SmallInteger(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "ON_HOLD", "CANCELLED", "COMPLETED", name="status"),
            server_default="ACTIVE",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["clinician_refrence"],
            ["clinician_tab.registration_id"],
        ),
        sa.ForeignKeyConstraint(
            ["medication_reference"],
            ["medication_tab.medication_reference"],
        ),
        sa.ForeignKeyConstraint(
            ["patient_refrence"],
            ["patient_tab.registration_id"],
        ),
        sa.PrimaryKeyConstraint("medication_request_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("medication_request_tab")
    op.drop_table("patient_tab")
    op.drop_table("medication_tab")
    op.drop_table("clinician_tab")
    # ### end Alembic commands ###
