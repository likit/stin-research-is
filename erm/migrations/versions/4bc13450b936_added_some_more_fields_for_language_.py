"""added some more fields for language editing request

Revision ID: 4bc13450b936
Revises: 33895c1ce5e3
Create Date: 2020-05-11 01:24:50.271200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bc13450b936'
down_revision = '33895c1ce5e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_language_editing_supports', sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('project_language_editing_supports', sa.Column('criteria', sa.Unicode(), nullable=True))
    op.add_column('project_language_editing_supports', sa.Column('docs', sa.Unicode(), nullable=True))
    op.add_column('project_language_editing_supports', sa.Column('request', sa.Unicode(), nullable=True))
    op.add_column('project_language_editing_supports', sa.Column('status', sa.Unicode(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_language_editing_supports', 'status')
    op.drop_column('project_language_editing_supports', 'request')
    op.drop_column('project_language_editing_supports', 'docs')
    op.drop_column('project_language_editing_supports', 'criteria')
    op.drop_column('project_language_editing_supports', 'approved_at')
    # ### end Alembic commands ###