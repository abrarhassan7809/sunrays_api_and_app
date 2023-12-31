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
    user_type = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)

    user_with_panel = relationship('Panel', back_populates='panel_with_user')
    user_with_inverter = relationship('Inverter', back_populates='inverter_with_user')
    user_with_frame = relationship('Frame', back_populates='frame_with_user')
    user_with_ac_cable = relationship('ACCable', back_populates='ac_cable_with_user')
    user_with_dc_cable = relationship('DCCable', back_populates='dc_cable_with_user')
    user_with_battery = relationship('Battery', back_populates='battery_with_user')
    user_with_labor = relationship('Labor', back_populates='labor_with_user')
    user_with_accessories = relationship('Accessories', back_populates='accessories_with_user')
    user_with_quotation = relationship('Quotation', back_populates='quotation_with_user')
    user_with_item = relationship('QuotationItem', back_populates='item_with_user')
    user_with_customer = relationship('Customer', back_populates='customer_with_user')
    user_with_expanse = relationship('Expanse', back_populates='expanse_with_user')


class Panel(Base):
    __tablename__ = "panel"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    capacity = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    panel_with_user = relationship('User', back_populates='user_with_panel')


class Inverter(Base):
    __tablename__ = "inverter"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    power_rating = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    inverter_with_user = relationship('User', back_populates='user_with_inverter')


class Frame(Base):
    __tablename__ = "frame"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    width = Column(String(255), nullable=True)
    height = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    frame_with_user = relationship('User', back_populates='user_with_frame')


class ACCable(Base):
    __tablename__ = "ac_cable"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    size = Column(String, nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    ac_cable_with_user = relationship('User', back_populates='user_with_ac_cable')


class DCCable(Base):
    __tablename__ = "dc_cable"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    size = Column(String, nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    dc_cable_with_user = relationship('User', back_populates='user_with_dc_cable')


class Battery(Base):
    __tablename__ = "battery"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    warranty = Column(String(255), nullable=True)
    capacity = Column(String(255), nullable=True)
    voltage = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    battery_with_user = relationship('User', back_populates='user_with_battery')


class Labor(Base):
    __tablename__ = "labor"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    labor_name = Column(String(255), nullable=False)
    start_date = Column(String, nullable=True)
    labor_cost = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

    labor_with_user = relationship('User', back_populates='user_with_labor')


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    customer_name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    address = Column(String, nullable=True)

    customer_with_user = relationship('User', back_populates='user_with_customer')


class Accessories(Base):
    __tablename__ = "accessories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=True)
    sell_price = Column(Float, nullable=True)

    accessories_with_user = relationship('User', back_populates='user_with_accessories')


class QuotationItem(Base):
    __tablename__ = "quotation_item"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quotation_id = Column(Integer, ForeignKey('quotation.id'), default=1, nullable=False)
    product_name = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    typ = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False)
    sell_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    item_with_user = relationship('User', back_populates='user_with_item')
    item_with_quotation = relationship('Quotation', back_populates='quotation_with_item')


class Quotation(Base):
    __tablename__ = "quotation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    customer_name = Column(String, nullable=True)
    walk_in_customer = Column(String, nullable=True)
    date = Column(String, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=True)

    quotation_with_user = relationship('User', back_populates='user_with_quotation')
    quotation_with_item = relationship('QuotationItem', back_populates='item_with_quotation', cascade="all, delete")


class Expanse(Base):
    __tablename__ = "expanse"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)

    expanse_with_user = relationship('User', back_populates='user_with_expanse')
