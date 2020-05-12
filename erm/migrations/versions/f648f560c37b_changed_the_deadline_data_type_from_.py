"""changed the deadline data type from datetime to date

Revision ID: f648f560c37b
Revises: 8b076f40d500
Create Date: 2020-05-12 23:02:11.696641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f648f560c37b'
down_revision = '8b076f40d500'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('project_ethic_review_send_records',
                    column_name='deadline', type_=sa.Date())


def downgrade():
    op.alter_column('project_ethic_review_send_records',
                    column_name='deadline', type_=sa.DateTime(timezone=True))
