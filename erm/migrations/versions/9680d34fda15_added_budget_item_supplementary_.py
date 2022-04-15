"""added budget item supplementary document model

Revision ID: 9680d34fda15
Revises: 456208d477bb
Create Date: 2022-04-11 09:49:29.364443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9680d34fda15'
down_revision = '456208d477bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_budget_item_docs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('budget_item_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['budget_item_id'], ['project_budget_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_budget_item_docs')
    # ### end Alembic commands ###