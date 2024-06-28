"""First-revision

Revision ID: e08ccdf31abc
Revises: d2e5e956e3a0
Create Date: 2024-06-26 20:29:50.893604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e08ccdf31abc'
down_revision: Union[str, None] = 'd2e5e956e3a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prescription_tab', sa.Column('medication_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prescription_tab', 'medication_json')
    # ### end Alembic commands ###