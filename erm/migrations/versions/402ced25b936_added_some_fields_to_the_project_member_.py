"""added some fields to the project member model

Revision ID: 402ced25b936
Revises: a3f63a187641
Create Date: 2020-06-04 16:20:21.788217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '402ced25b936'
down_revision = 'a3f63a187641'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_members', sa.Column('affiliation', sa.String(), nullable=True))
    op.add_column('project_members', sa.Column('firstname', sa.String(), nullable=True))
    op.add_column('project_members', sa.Column('lastname', sa.String(), nullable=True))
    op.add_column('project_members', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_members', 'title')
    op.drop_column('project_members', 'lastname')
    op.drop_column('project_members', 'firstname')
    op.drop_column('project_members', 'affiliation')
    # ### end Alembic commands ###
