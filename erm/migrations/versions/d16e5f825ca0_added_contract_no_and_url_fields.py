"""added contract no. and url fields

Revision ID: d16e5f825ca0
Revises: f3f0f2e34b0d
Create Date: 2020-06-04 01:32:31.955739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd16e5f825ca0'
down_revision = 'f3f0f2e34b0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('contract_no', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('contract_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'contract_url')
    op.drop_column('projects', 'contract_no')
    # ### end Alembic commands ###
