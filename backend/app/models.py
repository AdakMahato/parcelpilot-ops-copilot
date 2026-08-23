from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True)
    account_name = Column(String)
    plan = Column(String)
    status = Column(String)
    csm = Column(String)
    contract_file = Column(String)
    premium_support = Column(Boolean)
    notes = Column(String)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String, primary_key=True)
    account_id = Column(String)
    carrier = Column(String)
    status = Column(String)
    booked_at = Column(String)
    pickup_window_start = Column(String)
    pickup_window_end = Column(String)
    pickup_actual_at = Column(String)
    shipment_fee_inr = Column(Float)
    carrier_fault = Column(Boolean)
    customer_fault = Column(Boolean)
    cancellation_requested_at = Column(String)
    notes = Column(String)

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(String, primary_key=True)
    account_id = Column(String)
    created_at = Column(String)
    status = Column(String)
    subject = Column(String)
    description = Column(String)
    channel = Column(String)
    assigned_to = Column(String)
    last_customer_message_at = Column(String)
    historical_resolution = Column(String)

class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(String)
    event_type = Column(String)
    description = Column(String)
    actor = Column(String)
