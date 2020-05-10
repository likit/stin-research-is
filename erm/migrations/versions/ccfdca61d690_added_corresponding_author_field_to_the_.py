"""added corresponding author field to the model

Revision ID: ccfdca61d690
Revises: 498ee2fb2596
Create Date: 2020-04-17 00:58:00.241346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccfdca61d690'
down_revision = '498ee2fb2596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_publication_authors', sa.Column('corresponding', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_publication_authors', 'corresponding')
    # ### end Alembic commands ###