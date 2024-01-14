"""update user table schema name

Revision ID: fe01bc2a158b
Revises: 772f6a521fb5
Create Date: 2024-01-14 14:39:03.002297

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fe01bc2a158b"
down_revision: Union[str, None] = "772f6a521fb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the schema if it doesn't exist
    op.execute("CREATE SCHEMA IF NOT EXISTS account")

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column("role", sa.Integer(), nullable=False),
        sa.Column("gender", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        schema="account",
    )
    op.create_index(
        op.f("ix_account_users_id"), "users", ["id"], unique=False, schema="account"
    )
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop the table first
    op.drop_table("users", schema="account")

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("phone", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column(
            "password", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column("role", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("gender", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "last_login", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "deleted_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.drop_index(op.f("ix_account_users_id"), table_name="users", schema="account")
    op.drop_table("users", schema="account")
    # ### end Alembic commands ###
