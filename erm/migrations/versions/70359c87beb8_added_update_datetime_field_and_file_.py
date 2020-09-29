"""added update datetime field and file url field to the ethic record

Revision ID: 70359c87beb8
Revises: a036de5d62e9
Create Date: 2020-09-29 13:06:58.981756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70359c87beb8'
down_revision = 'a036de5d62e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_ethics', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('project_ethics', sa.Column('upload_file_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_ethics', 'upload_file_url')
    op.drop_column('project_ethics', 'updated_at')
    # ### end Alembic commands ###