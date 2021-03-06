"""Create user and entry table

Revision ID: ad4f4ab92584
Revises: 
Create Date: 2022-06-20 12:27:00.977546

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ad4f4ab92584'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password_hashed', sa.String(length=128), nullable=False),
                    sa.Column('auth_token', sa.String(length=64), nullable=True),
                    sa.Column('auth_token_expiration', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_index(op.f('ix_users_auth_token'), 'users', ['auth_token'], unique=False)
    op.create_table('entries',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('entry', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entries')
    op.drop_index(op.f('ix_users_auth_token'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
