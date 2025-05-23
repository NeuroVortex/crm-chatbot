"""create all related tables

Revision ID: 510d835f7190
Revises: 
Create Date: 2025-04-10 13:57:01.394051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '510d835f7190'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_slots',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('period', sa.String(), nullable=False),
    sa.Column('is_booked', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'public_id')
    )
    op.create_index(op.f('ix_time_slots_date'), 'time_slots', ['date'], unique=False)
    op.create_index(op.f('ix_time_slots_id'), 'time_slots', ['id'], unique=True)
    op.create_index(op.f('ix_time_slots_public_id'), 'time_slots', ['public_id'], unique=True)
    op.add_column('reservations', sa.Column('time_slot_id', sa.BigInteger(), nullable=False))
    op.drop_index('ix_reservations_id', table_name='reservations')
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=True)
    op.create_foreign_key(None, 'reservations', 'time_slots', ['time_slot_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reservations', type_='foreignkey')
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.create_index('ix_reservations_id', 'reservations', ['id'], unique=False)
    op.drop_column('reservations', 'time_slot_id')
    op.drop_index(op.f('ix_time_slots_public_id'), table_name='time_slots')
    op.drop_index(op.f('ix_time_slots_id'), table_name='time_slots')
    op.drop_index(op.f('ix_time_slots_date'), table_name='time_slots')
    op.drop_table('time_slots')
    # ### end Alembic commands ###
