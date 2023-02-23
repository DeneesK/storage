"""01_initial-db

Revision ID: 1992f2d5e099
Revises: 30ff112a44cd
Create Date: 2023-02-23 18:49:01.592611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1992f2d5e099'
down_revision = '30ff112a44cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('file_user_id_fkey', 'file', type_='foreignkey')
    op.create_foreign_key(None, 'file', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.create_foreign_key('file_user_id_fkey', 'file', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###