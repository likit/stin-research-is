"""added mentor field to the project record

Revision ID: a3f63a187641
Revises: fa0614c1afe4
Create Date: 2020-06-04 16:06:36.972212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3f63a187641'
down_revision = 'fa0614c1afe4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('mentor', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'mentor')
    # ### end Alembic commands ###