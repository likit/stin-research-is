"""changed Datetime to Date field of the application model

Revision ID: 159d153343b3
Revises: 069f11c922d1
Create Date: 2020-02-27 23:26:10.030151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '159d153343b3'
down_revision = '069f11c922d1'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('applications', 'datetime',
                    new_column_name='date', type_=sa.Date())


def downgrade():
    op.alter_column('applications', 'date',
                    new_column_name='datetime', type_=sa.DateTime(timezone=True))
