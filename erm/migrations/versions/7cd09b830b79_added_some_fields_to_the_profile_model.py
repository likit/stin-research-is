"""added some fields to the profile model

Revision ID: 7cd09b830b79
Revises: fbbf2c689d8c
Create Date: 2020-10-05 03:58:29.497278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cd09b830b79'
down_revision = 'fbbf2c689d8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('experience', sa.Text(), nullable=True))
    op.add_column('profiles', sa.Column('field_expertise', sa.String(), nullable=True))
    op.add_column('profiles', sa.Column('position', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'position')
    op.drop_column('profiles', 'field_expertise')
    op.drop_column('profiles', 'experience')
    # ### end Alembic commands ###
