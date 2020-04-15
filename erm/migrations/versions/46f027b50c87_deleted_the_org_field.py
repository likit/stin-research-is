"""deleted the org field

Revision ID: 46f027b50c87
Revises: 906ab2a93d4a
Create Date: 2020-03-30 12:45:54.282202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46f027b50c87'
down_revision = '906ab2a93d4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('applications', 'organization')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('organization', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###