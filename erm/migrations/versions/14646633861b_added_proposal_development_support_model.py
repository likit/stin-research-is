"""added proposal development support model

Revision ID: 14646633861b
Revises: 402ced25b936
Create Date: 2020-06-12 02:10:58.272324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14646633861b'
down_revision = '402ced25b936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_proposal_development_supports',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('qualification', sa.String(), nullable=True),
    sa.Column('support', sa.String(), nullable=True),
    sa.Column('docs', sa.Text(), nullable=True),
    sa.Column('other_docs', sa.String(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_proposal_development_supports')
    # ### end Alembic commands ###
