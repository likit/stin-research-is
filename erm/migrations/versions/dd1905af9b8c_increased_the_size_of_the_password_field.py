"""increased the size of the password field

Revision ID: dd1905af9b8c
Revises: 161fc66f87a9
Create Date: 2020-02-12 22:45:56.318716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1905af9b8c'
down_revision = '161fc66f87a9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'password_hash', nullable=False, type_=sa.String(255))


def downgrade():
    op.alter_column('users', 'password_hash', nullable=False, type_=sa.String(32))
