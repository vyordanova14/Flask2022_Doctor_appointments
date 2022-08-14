"""Added appointments

Revision ID: 7097f3bd29e0
Revises: 797f1b1a2a45
Create Date: 2022-08-13 12:56:09.999487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7097f3bd29e0'
down_revision = '797f1b1a2a45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('speciality', sa.String(length=100), nullable=False),
    sa.Column('date_of_appointment', sa.Date(), nullable=False),
    sa.Column('hour_of_appointment', sa.String(length=5), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='appointmentstatus'), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointments')
    # ### end Alembic commands ###