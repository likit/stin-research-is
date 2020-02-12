"""added project and project members models

Revision ID: c7d938ae64aa
Revises: 0da350474d0c
Create Date: 2020-02-13 02:03:20.260775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d938ae64aa'
down_revision = '0da350474d0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title_th', sa.String(), nullable=True),
    sa.Column('subtitle_th', sa.String(), nullable=True),
    sa.Column('title_en', sa.String(), nullable=True),
    sa.Column('subtitle_en', sa.String(), nullable=True),
    sa.Column('objective', sa.Text(), nullable=True),
    sa.Column('abstract', sa.Text(), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('method', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_members')
    op.drop_table('projects')
    # ### end Alembic commands ###
