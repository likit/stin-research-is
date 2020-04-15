"""replaced reviewer_id with review_id field

Revision ID: 064c47765ae5
Revises: 05635c0bd3cf
Create Date: 2020-03-18 06:38:37.871808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '064c47765ae5'
down_revision = '05635c0bd3cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_review_send_records', sa.Column('review_id', sa.Integer(), nullable=True))
    op.drop_constraint('project_review_send_records_reviewer_id_fkey', 'project_review_send_records', type_='foreignkey')
    op.create_foreign_key(None, 'project_review_send_records', 'project_review_records', ['review_id'], ['id'])
    op.drop_column('project_review_send_records', 'reviewer_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_review_send_records', sa.Column('reviewer_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'project_review_send_records', type_='foreignkey')
    op.create_foreign_key('project_review_send_records_reviewer_id_fkey', 'project_review_send_records', 'project_reviewers', ['reviewer_id'], ['id'])
    op.drop_column('project_review_send_records', 'review_id')
    # ### end Alembic commands ###