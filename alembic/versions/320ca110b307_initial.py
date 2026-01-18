"""initial

Revision ID: 320ca110b307
Revises: 
Create Date: 2026-01-18 13:03:05.763986

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '320ca110b307'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Путь к sql/seed.sql относительно корня проекта (или текущей папки)
    seed_path = os.path.join(os.path.dirname(__file__), '../../sql/seed.sql')

    with open(seed_path, 'r', encoding='utf-8') as f:
        sql_data = f.read()

    op.execute(sql_data)


def downgrade() -> None:
    op.execute("TRUNCATE organization_activities, organization_phones, organizations, activities, buildings CASCADE")