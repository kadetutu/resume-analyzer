"""Sample Alembic migration template"""
"""Initial migration

Revision ID: 001_initial
Revises:
Create Date: 2024-05-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tables based on SQLModel models
    pass


def downgrade() -> None:
    pass
