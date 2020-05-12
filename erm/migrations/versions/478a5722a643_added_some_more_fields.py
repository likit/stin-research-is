"""added some more fields

Revision ID: 478a5722a643
Revises: f648f560c37b
Create Date: 2020-05-13 03:33:33.707227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '478a5722a643'
down_revision = 'f648f560c37b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_review_records', sa.Column('alignment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('alignment_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('alignment_other', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('benefit', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('benefit_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('benefit_detail', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('benefit_detail_other', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('budget', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('budget_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('data_analyze', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('data_analyze_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('data_collection', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('data_collection_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('idea', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('idea_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('importance', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('importance_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('objective', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('objective_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('outcome', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('outcome_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('outcome_detail', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('outcome_detail_other', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('plan', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('plan_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('sampling', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('sampling_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('tool', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('tool_comment', sa.Text(), nullable=True))
    op.add_column('project_review_records', sa.Column('variable', sa.Unicode(), nullable=True))
    op.add_column('project_review_records', sa.Column('variable_comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_review_records', 'variable_comment')
    op.drop_column('project_review_records', 'variable')
    op.drop_column('project_review_records', 'tool_comment')
    op.drop_column('project_review_records', 'tool')
    op.drop_column('project_review_records', 'sampling_comment')
    op.drop_column('project_review_records', 'sampling')
    op.drop_column('project_review_records', 'plan_comment')
    op.drop_column('project_review_records', 'plan')
    op.drop_column('project_review_records', 'outcome_detail_other')
    op.drop_column('project_review_records', 'outcome_detail')
    op.drop_column('project_review_records', 'outcome_comment')
    op.drop_column('project_review_records', 'outcome')
    op.drop_column('project_review_records', 'objective_comment')
    op.drop_column('project_review_records', 'objective')
    op.drop_column('project_review_records', 'importance_comment')
    op.drop_column('project_review_records', 'importance')
    op.drop_column('project_review_records', 'idea_comment')
    op.drop_column('project_review_records', 'idea')
    op.drop_column('project_review_records', 'data_collection_comment')
    op.drop_column('project_review_records', 'data_collection')
    op.drop_column('project_review_records', 'data_analyze_comment')
    op.drop_column('project_review_records', 'data_analyze')
    op.drop_column('project_review_records', 'budget_comment')
    op.drop_column('project_review_records', 'budget')
    op.drop_column('project_review_records', 'benefit_detail_other')
    op.drop_column('project_review_records', 'benefit_detail')
    op.drop_column('project_review_records', 'benefit_comment')
    op.drop_column('project_review_records', 'benefit')
    op.drop_column('project_review_records', 'alignment_other')
    op.drop_column('project_review_records', 'alignment_comment')
    op.drop_column('project_review_records', 'alignment')
    # ### end Alembic commands ###
