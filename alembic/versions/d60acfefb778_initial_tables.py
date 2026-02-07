"""initial tables

Revision ID: d60acfefb778
Revises: 
Create Date: 2026-02-07 17:08:16.846750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd60acfefb778'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'gates',
        sa.Column('gate_id', sa.String(10), primary_key=True),
        sa.Column('gate_name', sa.String(50), nullable=False),
    )

    op.create_table(
        'connections',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('from_gate_id', sa.String(10), sa.ForeignKey('gates.gate_id'), nullable=False),
        sa.Column('to_gate_id', sa.String(10), sa.ForeignKey('gates.gate_id'), nullable=False),
        sa.Column('distance_hu', sa.Float, nullable=False),
    )

    op.bulk_insert(
        sa.table('gates',
            sa.column('gate_id', sa.String),
            sa.column('gate_name', sa.String),
        ),
        [
            {'gate_id': 'SOL', 'gate_name': 'Sol'},
            {'gate_id': 'PRX', 'gate_name': 'Proxima'},
            {'gate_id': 'SIR', 'gate_name': 'Sirius'},
            {'gate_id': 'CAS', 'gate_name': 'Castor'},
            {'gate_id': 'PRO', 'gate_name': 'Procyon'},
            {'gate_id': 'DEN', 'gate_name': 'Denebula'},
            {'gate_id': 'RAN', 'gate_name': 'Ran'},
            {'gate_id': 'ARC', 'gate_name': 'Arcturus'},
            {'gate_id': 'FOM', 'gate_name': 'Fomalhaut'},
            {'gate_id': 'ALT', 'gate_name': 'Altair'},
            {'gate_id': 'VEG', 'gate_name': 'Vega'},
            {'gate_id': 'ALD', 'gate_name': 'Aldermain'},
            {'gate_id': 'ALS', 'gate_name': 'Alshain'},
        ]
    )

    op.bulk_insert(
        sa.table('connections',
            sa.column('from_gate_id', sa.String),
            sa.column('to_gate_id', sa.String),
            sa.column('distance_hu', sa.Float),
        ),
        [
            {'from_gate_id': 'SOL', 'to_gate_id': 'RAN', 'distance_hu': 100},
            {'from_gate_id': 'SOL', 'to_gate_id': 'PRX', 'distance_hu': 90},
            {'from_gate_id': 'SOL', 'to_gate_id': 'SIR', 'distance_hu': 100},
            {'from_gate_id': 'SOL', 'to_gate_id': 'ARC', 'distance_hu': 200},
            {'from_gate_id': 'SOL', 'to_gate_id': 'ALD', 'distance_hu': 250},
            {'from_gate_id': 'PRX', 'to_gate_id': 'SOL', 'distance_hu': 90},
            {'from_gate_id': 'PRX', 'to_gate_id': 'SIR', 'distance_hu': 100},
            {'from_gate_id': 'PRX', 'to_gate_id': 'ALT', 'distance_hu': 150},
            {'from_gate_id': 'SIR', 'to_gate_id': 'SOL', 'distance_hu': 80},
            {'from_gate_id': 'SIR', 'to_gate_id': 'PRX', 'distance_hu': 10},
            {'from_gate_id': 'SIR', 'to_gate_id': 'CAS', 'distance_hu': 200},
            {'from_gate_id': 'CAS', 'to_gate_id': 'SIR', 'distance_hu': 200},
            {'from_gate_id': 'CAS', 'to_gate_id': 'PRO', 'distance_hu': 120},
            {'from_gate_id': 'PRO', 'to_gate_id': 'CAS', 'distance_hu': 80},
            {'from_gate_id': 'DEN', 'to_gate_id': 'PRO', 'distance_hu': 5},
            {'from_gate_id': 'DEN', 'to_gate_id': 'ARC', 'distance_hu': 2},
            {'from_gate_id': 'DEN', 'to_gate_id': 'FOM', 'distance_hu': 8},
            {'from_gate_id': 'DEN', 'to_gate_id': 'RAN', 'distance_hu': 100},
            {'from_gate_id': 'DEN', 'to_gate_id': 'ALD', 'distance_hu': 3},
            {'from_gate_id': 'RAN', 'to_gate_id': 'SOL', 'distance_hu': 100},
            {'from_gate_id': 'ARC', 'to_gate_id': 'SOL', 'distance_hu': 500},
            {'from_gate_id': 'ARC', 'to_gate_id': 'DEN', 'distance_hu': 120},
            {'from_gate_id': 'FOM', 'to_gate_id': 'PRX', 'distance_hu': 10},
            {'from_gate_id': 'FOM', 'to_gate_id': 'DEN', 'distance_hu': 20},
            {'from_gate_id': 'FOM', 'to_gate_id': 'ALS', 'distance_hu': 9},
            {'from_gate_id': 'ALT', 'to_gate_id': 'FOM', 'distance_hu': 140},
            {'from_gate_id': 'ALT', 'to_gate_id': 'VEG', 'distance_hu': 220},
            {'from_gate_id': 'VEG', 'to_gate_id': 'ARC', 'distance_hu': 220},
            {'from_gate_id': 'VEG', 'to_gate_id': 'ALD', 'distance_hu': 580},
            {'from_gate_id': 'ALD', 'to_gate_id': 'SOL', 'distance_hu': 200},
            {'from_gate_id': 'ALD', 'to_gate_id': 'ALS', 'distance_hu': 160},
            {'from_gate_id': 'ALD', 'to_gate_id': 'VEG', 'distance_hu': 320},
            {'from_gate_id': 'ALS', 'to_gate_id': 'ALT', 'distance_hu': 1},
            {'from_gate_id': 'ALS', 'to_gate_id': 'ALD', 'distance_hu': 1},
        ]
    )


def downgrade() -> None:
    op.drop_table('connections')
    op.drop_table('gates')
