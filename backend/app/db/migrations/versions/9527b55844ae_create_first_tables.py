"""create_first_tables

Revision ID: 9527b55844ae
Revises:
Create Date: 2021-07-12 17:21:09.168031

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '9527b55844ae'
down_revision = None
branch_labels = None
depends_on = None


# created_at, updated_atのトリガー
def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

# timestampsのモデル


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_holo_member_table() -> None:
    op.create_table(
        "holo_member",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("twitter", sa.Text, nullable=False),
        sa.Column("age", sa.Numeric(10, 1), nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_holo_member_modtime
            BEFORE UPDATE
            ON holo_member
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_holo_member_table()


def downgrade() -> None:
    op.drop_table("holo_member")
    op.execute("DROP FUNCTION update_updated_at_column")
