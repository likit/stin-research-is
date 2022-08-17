"""added creator ID to the publication model

Revision ID: 252c5f80b982
Revises: 0c9eb3f66d03
Create Date: 2022-08-18 04:06:09.729666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252c5f80b982'
down_revision = '0c9eb3f66d03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_pub_records', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'project_pub_records', 'users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project_pub_records', type_='foreignkey')
    op.drop_column('project_pub_records', 'creator_id')
    # ### end Alembic commands ###