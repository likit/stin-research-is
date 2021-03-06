"""added created datetime and creator fields to the parent project model

Revision ID: c8e9b62f8fcb
Revises: 0236db9e2ef9
Create Date: 2020-05-29 12:20:35.910729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e9b62f8fcb'
down_revision = '0236db9e2ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parent_projects', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('parent_projects', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'parent_projects', 'users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'parent_projects', type_='foreignkey')
    op.drop_column('parent_projects', 'creator_id')
    op.drop_column('parent_projects', 'created_at')
    # ### end Alembic commands ###
