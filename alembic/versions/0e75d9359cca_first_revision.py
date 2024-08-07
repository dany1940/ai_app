"""First-revision

Revision ID: 0e75d9359cca
Revises:
Create Date: 2024-07-01 20:09:17.065778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision: str = '0e75d9359cca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("CREATE EXTENSION ltree"))
    op.create_table('organization_tab',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('path', sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_tab',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('pword_hash', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('can_edit', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization_tab.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tab')
    op.drop_table('organization_tab')
    # ### end Alembic commands ###
