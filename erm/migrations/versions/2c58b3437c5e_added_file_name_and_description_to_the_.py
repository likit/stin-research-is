"""added file name and description to the supplementary model

Revision ID: 2c58b3437c5e
Revises: 2a128460bdcd
Create Date: 2020-09-29 14:15:12.308884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c58b3437c5e'
down_revision = '2a128460bdcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_supplementary_docs', sa.Column('desc', sa.Text(), nullable=True))
    op.add_column('project_supplementary_docs', sa.Column('filename', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_supplementary_docs', 'filename')
    op.drop_column('project_supplementary_docs', 'desc')
    # ### end Alembic commands ###