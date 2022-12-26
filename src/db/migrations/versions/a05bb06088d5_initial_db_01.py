"""initial_db_01

Revision ID: a05bb06088d5
Revises: 
Create Date: 2022-12-15 15:45:25.940960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a05bb06088d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('urls',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('original_url', sa.String(), nullable=False),
    sa.Column('short_url', sa.String(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('visibility', sa.Boolean(), nullable=True),
    sa.Column('counter', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    op.drop_table('users')
    # ### end Alembic commands ###
