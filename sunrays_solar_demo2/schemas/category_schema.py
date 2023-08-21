import datetime
from pydantic import BaseModel, Field, validator


class BaseMod(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        schema_extra: dict = {}


# ==========panel============
class CreatePanel(BaseMod):
    name: str
    brand: str
    capacity: float
    efficiency: float
    dimensions: str
    weight: float


class GetPanel(CreatePanel):
    id: int


class UpdatePanel(BaseMod):
    name: str | None = None
    brand: str | None = None
    capacity: float | None = None
    efficiency: float | None = None
    dimensions: str | None = None
    weight: float | None = None


# ==========inverter============
class CreateInverter(BaseMod):
    manufacturer: str
    model: str
    serial_number: str
    power_rating: float
    input_voltage: str
    output_voltage: str
    efficiency: float
    communication_protocol: str
    warranty: str
    installation_date: datetime.date

    @validator("serial_number")
    def validate_email(cls, value):
        if len(value) <= 4:
            raise ValueError("Serial number must be of 5 character")
        return value.lower()


class GetInverter(CreatePanel):
    id: int


class UpdateInverter(BaseMod):
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    power_rating: float | None = None
    input_voltage: str | None = None
    output_voltage: str | None = None
    efficiency: float | None = None
    communication_protocol: str | None = None
    warranty: str | None = None


# ==========frame============
class CreateFrame(BaseMod):
    material: str
    weight: float
    width: float
    height: float
    thickness: float
    manufacturer: str
    price: float


class GetFrame(CreateFrame):
    id: int


class UpdateFrame(BaseMod):
    material: str | None = None
    weight: float | None = None
    width: float | None = None
    height: float | None = None
    thickness: float | None = None
    manufacturer: str | None = None
    price: float | None = None


# ==========coil============
class CreateCoil(BaseMod):
    material: str
    gauge: float
    width: float
    height: float
    manufacturer: str
    price: float


class GetCoil(CreateCoil):
    id: int


class UpdateCoil(BaseMod):
    material: str | None = None
    gauge: float | None = None
    width: float | None = None
    height: float | None = None
    manufacturer: str | None = None
    price: float | None = None


# ==========battery============
class CreateBattery(BaseMod):
    brand: str
    capacity: float
    voltage: float
    chemistry: str
    weight: float
    price: float


class GetBattery(CreateBattery):
    id: int


class UpdateBattery(BaseMod):
    brand: str | None = None
    capacity: float | None = None
    voltage: float | None = None
    chemistry: str | None = None
    weight: float | None = None
    price: float | None = None


# ==========labor_installation============
class CreateLabor(BaseMod):
    labor_name: str
    start_date: datetime.date
    end_date: datetime.date
    labor_cost: int
    description: str


class GetLabor(CreateLabor):
    id: int


class UpdateLabor(BaseMod):
    labor_name: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    labor_cost: int | None = None
    description: str | None = None


# ==========accessories============
class CreateAccessory(BaseMod):
    name: str
    labor_id: int
    description: str


class GetAccessory(CreateAccessory):
    id: int


class UpdateAccessory(BaseMod):
    name: str | None = None
    labor_id: int | None = None
    description: str | None = None


# ==========quotations============
class CreateQuotation(BaseMod):
    date: datetime.date
    total_amount: int


class GetQuotation(CreateAccessory):
    id: int


class UpdateQuotation(BaseMod):
    date: datetime.date | None = None
    total_amount: int | None = None


# ==========quotations_items============
class CreateQuotationItems(BaseMod):
    quotation_id: int
    product_name: str
    quantity: int
    price: float


class GetQuotationItems(CreateAccessory):
    id: int


class UpdateQuotationItems(BaseMod):
    quotation_id: int | None = None
    product_name: str | None = None
    quantity: int | None = None
    price: float | None = None
