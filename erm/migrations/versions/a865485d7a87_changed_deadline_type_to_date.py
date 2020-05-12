"""changed deadline type to date

Revision ID: a865485d7a87
Revises: 80b5c6db869b
Create Date: 2020-05-13 05:04:50.386804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a865485d7a87'
down_revision = '80b5c6db869b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('project_review_send_records', column_name='deadline',
                    type_=sa.Date())


def downgrade():
    op.alter_column('project_review_send_records', column_name='deadline',
                    type_=sa.DateTime(timezone=True))
