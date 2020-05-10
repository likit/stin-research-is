"""added abstract fields to the pub

Revision ID: 33895c1ce5e3
Revises: ccfdca61d690
Create Date: 2020-04-17 14:12:46.719668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33895c1ce5e3'
down_revision = 'ccfdca61d690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_pub_records', sa.Column('en_abstract', sa.Text(), nullable=True))
    op.add_column('project_pub_records', sa.Column('th_abstract', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_pub_records', 'th_abstract')
    op.drop_column('project_pub_records', 'en_abstract')
    # ### end Alembic commands ###