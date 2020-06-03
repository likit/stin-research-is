"""added a photo url field to the profile model

Revision ID: f3f0f2e34b0d
Revises: b5eccd86d4e3
Create Date: 2020-06-04 00:38:03.805666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3f0f2e34b0d'
down_revision = 'b5eccd86d4e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('photo_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'photo_url')
    # ### end Alembic commands ###