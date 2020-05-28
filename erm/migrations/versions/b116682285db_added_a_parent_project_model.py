"""added a parent project model

Revision ID: b116682285db
Revises: a865485d7a87
Create Date: 2020-05-29 01:43:21.310075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b116682285db'
down_revision = 'a865485d7a87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent_projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title_th', sa.String(), nullable=True),
    sa.Column('subtitle_th', sa.String(), nullable=True),
    sa.Column('title_en', sa.String(), nullable=True),
    sa.Column('subtitle_en', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('projects', sa.Column('parent_project_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'projects', 'parent_projects', ['parent_project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'projects', type_='foreignkey')
    op.drop_column('projects', 'parent_project_id')
    op.drop_table('parent_projects')
    # ### end Alembic commands ###
