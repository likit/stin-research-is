"""added Profile model

Revision ID: 293bdff2b9e3
Revises: dd1905af9b8c
Create Date: 2020-02-13 01:19:21.486726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '293bdff2b9e3'
down_revision = 'dd1905af9b8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title_th', sa.String(), nullable=True),
    sa.Column('title_en', sa.String(), nullable=True),
    sa.Column('firstname_th', sa.String(), nullable=True),
    sa.Column('lastname_th', sa.String(), nullable=True),
    sa.Column('firstname_en', sa.String(), nullable=True),
    sa.Column('lastname_en', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###
