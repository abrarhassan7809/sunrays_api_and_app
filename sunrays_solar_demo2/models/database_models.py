from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Float, Date
from sqlalchemy.orm import relationship
from models.database_config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String, nullable=True)
    joined = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=False)
    fcm_token = Column(String(255), nullable=True)
    user_type = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    otp = Column(String(255), nullable=True)

    user_with_panel = relationship('Panel', back_populates='panel_with_user', cascade="all, delete")
    user_with_inverter = relationship('Inverter', back_populates='inverter_with_user', cascade="all, delete")
    user_with_frame = relationship('Frame', back_populates='frame_with_user', cascade="all, delete")
    user_with_coil = relationship('Coil', back_populates='coil_with_user', cascade="all, delete")
    user_with_battery = relationship('Battery', back_populates='battery_with_user', cascade="all, delete")
    user_with_labor = relationship('LaborInstallation', back_populates='labor_with_user', cascade="all, delete")
    user_with_accessories = relationship('Accessories', back_populates='accessories_with_user', cascade="all, delete")
    user_with_quotation = relationship('Quotation', back_populates='quotation_with_user', cascade="all, delete")


class Panel(Base):
    __tablename__ = "panel"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False)
    capacity = Column(Float, nullable=True)
    efficiency = Column(Float, nullable=True)
    dimensions = Column(String(255), nullable=True)
    weight = Column(Float, nullable=True)

    panel_with_user = relationship('User', back_populates='user_with_panel')


class Inverter(Base):
    __tablename__ = "inverter"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    serial_number = Column(String(255), nullable=False, unique=True)
    power_rating = Column(Float, nullable=False)
    input_voltage = Column(String(50), nullable=False)
    output_voltage = Column(String(50), nullable=False)
    efficiency = Column(Float, nullable=False)
    communication_protocol = Column(String(255), nullable=False)
    warranty = Column(String(255), nullable=False)
    installation_date = Column(Date, nullable=True)

    inverter_with_user = relationship('User', back_populates='user_with_inverter')


class Frame(Base):
    __tablename__ = "frame"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    material = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    thickness = Column(Float, nullable=False)
    manufacturer = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)

    frame_with_user = relationship('User', back_populates='user_with_frame')


class Coil(Base):
    __tablename__ = "coils"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    material = Column(String(255), nullable=False)
    gauge = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    manufacturer = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)

    coil_with_user = relationship('User', back_populates='user_with_coil')


class Battery(Base):
    __tablename__ = "battery"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    brand = Column(String(255), nullable=False)
    capacity = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    chemistry = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)
    price = Column(Float, nullable=True)

    battery_with_user = relationship('User', back_populates='user_with_battery')


class LaborInstallation(Base):
    __tablename__ = "labor_installation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    labor_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    labor_cost = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)

    labor_with_user = relationship('User', back_populates='user_with_labor')
    labor_with_accessories = relationship('Accessories', back_populates='accessories_with_labor')


class Accessories(Base):
    __tablename__ = "accessories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    labor_id = Column(Integer, ForeignKey('labor_installation.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

    accessories_with_user = relationship('User', back_populates='user_with_accessories')
    accessories_with_labor = relationship('LaborInstallation', back_populates='labor_with_accessories')


class Quotation(Base):
    __tablename__ = "quotation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)

    quotation_with_user = relationship('User', back_populates='user_with_quotation')
    quotation_with_item = relationship('QuotationItem', back_populates='itme_with_quotation', cascade="all, delete")


class QuotationItem(Base):
    __tablename__ = "quotation_item"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quotation_id = Column(Integer, ForeignKey('quotation.id', ondelete='CASCADE'), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    itme_with_quotation = relationship('Quotation', back_populates='quotation_with_item')
