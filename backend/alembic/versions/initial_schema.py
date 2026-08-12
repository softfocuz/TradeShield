from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e6b085c6cf7c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('EXPORTER', 'IMPORTER', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('exporter_profiles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('business_registration', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('importer_profiles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('import_license', sa.String(length=255), nullable=False),
    sa.Column('destination_country', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('importer_profiles')
    op.drop_table('exporter_profiles')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
