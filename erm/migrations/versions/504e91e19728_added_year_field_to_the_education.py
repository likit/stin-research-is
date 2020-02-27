"""added year field to the education

Revision ID: 504e91e19728
Revises: f384c81e6b0f
Create Date: 2020-02-27 21:42:53.742177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '504e91e19728'
down_revision = 'f384c81e6b0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('educations', sa.Column('year', sa.Integer(), nullable=False))
    #op.execute("UPDATE educations SET year = 2000")
    #op.alter_column('educations', 'year', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('educations', 'year')
    # ### end Alembic commands ###
