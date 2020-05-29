"""removed comment field

Revision ID: 80b5c6db869b
Revises: 478a5722a643
Create Date: 2020-05-13 04:34:08.324309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80b5c6db869b'
down_revision = '478a5722a643'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_ethic_review_records', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_ethic_review_records', sa.Column('comment', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###