from fastapi import APIRouter, status, Depends, HTTPException
from models.database_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models import database_models

from routes.authentication import authenticate_user
from routes.category_backend import get_all_db_category, get_update_category, get_db_category_by_id, get_create_category
from schemas.category_schema import CreatePanel, UpdatePanel, CreateInverter, UpdateInverter, CreateFrame, UpdateFrame, \
    UpdateCoil, CreateCoil, CreateBattery, UpdateBattery, CreateLabor, UpdateLabor, CreateAccessory, UpdateAccessory, \
    CreateQuotation, UpdateQuotation, CreateQuotationItems, UpdateQuotationItems

category = APIRouter()


# ======panel=======
@category.post('/create_panel/', status_code=status.HTTP_201_CREATED)
async def create_panel(panel_schema: CreatePanel, db: AsyncSession = Depends(get_db)):
    if (panel_schema.weight and panel_schema.efficiency and panel_schema.capacity) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Weight, Efficiency and Capacity must be grater then zero")
    user_id = 1
    db_data = await get_create_category(db, database_models.Panel, panel_schema, user_id)
    return db_data


@category.get('/get_panel/{panel_id}/', status_code=status.HTTP_200_OK)
async def get_panel(panel_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Panel, database_models.Panel.id,
                                          panel_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_panel/', status_code=status.HTTP_200_OK)
async def get_all_panel(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Panel)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_panel/{panel_id}/', status_code=status.HTTP_200_OK)
async def delete_panel(panel_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Panel, database_models.Panel.id, panel_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'panel deleted successfully'}


@category.patch('/update_panel/{panel_id}/', status_code=status.HTTP_200_OK)
async def update_panel(panel_id: int, panel_schema: UpdatePanel, db: AsyncSession = Depends(get_db)):
    if panel_schema.weight is not None:
        if panel_schema.weight <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Weight must be grater then zero")
    if panel_schema.efficiency is not None:
        if panel_schema.efficiency <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Efficiency must be grater then zero")
    if panel_schema.capacity is not None:
        if panel_schema.capacity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Capacity must be grater then zero")

    db_data = await get_update_category(db, database_models.Panel, database_models.Panel.id, panel_id,
                                        panel_schema)
    return db_data


# ======inverter=======
@category.post('/create_inverter/', status_code=status.HTTP_201_CREATED)
async def create_inverter(inverter_schema: CreateInverter, db: AsyncSession = Depends(get_db)):
    get_db_data = await get_db_category_by_id(db, database_models.Inverter, database_models.Inverter.serial_number,
                                              inverter_schema.serial_number)
    if get_db_data is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inverter with same serial number exists",
        )

    if (inverter_schema.power_rating and inverter_schema.efficiency) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Power Rating and Efficiency must be grater then zero")
    user_id = 1
    db_data = await get_create_category(db, database_models.Inverter, inverter_schema, user_id)
    return db_data


@category.get('/get_inverter/{serial_number}/', status_code=status.HTTP_200_OK)
async def get_inverter(serial_number: str, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Inverter, database_models.Inverter.serial_number,
                                          serial_number)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_inverter/', status_code=status.HTTP_200_OK)
async def get_all_inverter(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Inverter)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_inverter/{inverter_id}/', status_code=status.HTTP_200_OK)
async def delete_inverter(inverter_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Inverter, database_models.Inverter.id, inverter_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'inverter deleted successfully'}


@category.patch('/update_inverter/{inverter_id}/', status_code=status.HTTP_200_OK)
async def update_inverter(inverter_id: int, inverter_schema: UpdateInverter, db: AsyncSession = Depends(get_db)):
    if inverter_schema.power_rating is not None:
        if inverter_schema.power_rating <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Power Rating must be grater then zero")
    if inverter_schema.efficiency is not None:
        if inverter_schema.efficiency <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Efficiency must be grater then zero")

    db_data = await get_update_category(db, database_models.Inverter, database_models.Inverter.id, inverter_id,
                                        inverter_schema)
    return db_data


# ======frame=======
@category.post('/create_frame/', status_code=status.HTTP_201_CREATED)
async def create_frame(frame_schema: CreateFrame, db: AsyncSession = Depends(get_db)):
    if (
            frame_schema.weight and frame_schema.width and frame_schema.height and frame_schema.thickness and frame_schema.price) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Weight, Width, Height, Thickness and Price must be grater then zero")
    user_id = 1
    db_data = await get_create_category(db, database_models.Frame, frame_schema, user_id)
    return db_data


@category.get('/get_frame/{frame_id}/', status_code=status.HTTP_200_OK)
async def get_frame(frame_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Frame, database_models.Frame.id,
                                          frame_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_frame/', status_code=status.HTTP_200_OK)
async def get_all_frame(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Frame)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_frame/{frame_id}/', status_code=status.HTTP_200_OK)
async def delete_frame(frame_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Frame, database_models.Frame.id, frame_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'frame deleted successfully'}


@category.patch('/update_frame/{frame_id}/', status_code=status.HTTP_200_OK)
async def update_frame(frame_id: int, frame_schema: UpdateFrame, db: AsyncSession = Depends(get_db)):
    if frame_schema.weight is not None:
        if frame_schema.weight <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Weight must be grater then zero")
    if frame_schema.width is not None:
        if frame_schema.width <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Width must be grater then zero")
    if frame_schema.height is not None:
        if frame_schema.height <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Height must be grater then zero")
    if frame_schema.thickness is not None:
        if frame_schema.thickness <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Thickness must be grater then zero")
    if frame_schema.price is not None:
        if frame_schema.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid price")

    db_data = await get_update_category(db, database_models.Frame, database_models.Frame.id, frame_id,
                                        frame_schema)
    return db_data


# ======coil=======
@category.post('/create_coil/', status_code=status.HTTP_201_CREATED)
async def create_coil(coil_schema: CreateCoil, db: AsyncSession = Depends(get_db)):
    if (coil_schema.gauge and coil_schema.width and coil_schema.height and coil_schema.price) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Gauge, Width, Height and Price must be grater then zero")
    user_id = 1
    db_data = await get_create_category(db, database_models.Coil, coil_schema, user_id)
    return db_data


@category.get('/get_coil/{coil_id}/', status_code=status.HTTP_200_OK)
async def get_coil(coil_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Coil, database_models.Coil.id, coil_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_coil/', status_code=status.HTTP_200_OK)
async def get_all_coil(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Coil)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_coil/{coil_id}/', status_code=status.HTTP_200_OK)
async def delete_coil(coil_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Coil, database_models.Coil.id, coil_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'coil deleted successfully'}


@category.patch('/update_coil/{coil_id}/', status_code=status.HTTP_200_OK)
async def update_coil(coil_id: int, coil_schema: UpdateCoil, db: AsyncSession = Depends(get_db)):
    if coil_schema.width is not None:
        if coil_schema.width <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Width must be grater then zero")
    if coil_schema.height is not None:
        if coil_schema.height <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Height must be grater then zero")
    if coil_schema.price is not None:
        if coil_schema.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid price")

    db_data = await get_update_category(db, database_models.Frame, database_models.Frame.id, coil_id,
                                        coil_schema)
    return db_data


# ======battery=======
@category.post('/create_battery/', status_code=status.HTTP_201_CREATED)
async def create_battery(battery_schema: CreateBattery, db: AsyncSession = Depends(get_db)):
    if (battery_schema.capacity and battery_schema.voltage and battery_schema.weight and battery_schema.price) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Capacity, Voltage, Weight and Price must be grater then zero")
    user_id = 1
    db_data = await get_create_category(db, database_models.Battery, battery_schema, user_id)
    return db_data


@category.get('/get_battery/{battery_id}/', status_code=status.HTTP_200_OK)
async def get_battery(battery_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Battery, database_models.Battery.id, battery_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_battery/', status_code=status.HTTP_200_OK)
async def get_all_battery(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Battery)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_battery/{battery_id}/', status_code=status.HTTP_200_OK)
async def delete_battery(battery_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Battery, database_models.Battery.id, battery_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'battery deleted successfully'}


@category.patch('/update_coil/{battery_id}/', status_code=status.HTTP_200_OK)
async def update_coil(battery_id: int, battery_schema: UpdateBattery, db: AsyncSession = Depends(get_db)):
    if battery_schema.capacity is not None:
        if battery_schema.capacity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Capacity must be grater then zero")
    if battery_schema.voltage is not None:
        if battery_schema.voltage <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Voltage must be grater then zero")
    if battery_schema.weight is not None:
        if battery_schema.weight <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Weight must be grater then zero")
    if battery_schema.price is not None:
        if battery_schema.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid price")

    db_data = await get_update_category(db, database_models.Battery, database_models.Battery.id, battery_id,
                                        battery_schema)
    return db_data


# ======labor_installation=======
@category.post('/create_labor/', status_code=status.HTTP_201_CREATED)
async def create_labor(labor_schema: CreateLabor, db: AsyncSession = Depends(get_db)):
    if labor_schema.labor_cost <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid labor cost")
    user_id = 1
    db_data = await get_create_category(db, database_models.LaborInstallation, labor_schema, user_id)
    return db_data


@category.get('/get_labor/{labor_id}/', status_code=status.HTTP_200_OK)
async def get_labor(labor_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.LaborInstallation,
                                          database_models.LaborInstallation.id, labor_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_labor/', status_code=status.HTTP_200_OK)
async def get_all_labor(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.LaborInstallation)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_labor/{labor_id}/', status_code=status.HTTP_200_OK)
async def delete_labor(labor_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.LaborInstallation,
                                          database_models.LaborInstallation.id, labor_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'labor deleted successfully'}


@category.patch('/update_labor/{labor_id}/', status_code=status.HTTP_200_OK)
async def update_labor(labor_id: int, battery_schema: UpdateLabor, db: AsyncSession = Depends(get_db)):
    if battery_schema.labor_cost is not None:
        if battery_schema.labor_cost <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid labor cost")

    db_data = await get_update_category(db, database_models.LaborInstallation, database_models.LaborInstallation.id,
                                        labor_id, battery_schema)
    return db_data


# ======accessories=======
@category.post('/create_accessory/', status_code=status.HTTP_201_CREATED)
async def create_accessory(accessory_schema: CreateAccessory, db: AsyncSession = Depends(get_db)):
    if accessory_schema.labor_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid labor id")

    get_db_accessory = await get_db_category_by_id(db, database_models.LaborInstallation,
                                                   database_models.LaborInstallation.id, accessory_schema.labor_id)
    if get_db_accessory is None:
        return {'detail': 'Invalid labor id'}
    user_id = 1
    db_data = await get_create_category(db, database_models.Accessories, accessory_schema, user_id)
    return db_data


@category.get('/get_accessory/{accessory_id}/', status_code=status.HTTP_200_OK)
async def get_accessory(accessory_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Accessories, database_models.Accessories.id,
                                          accessory_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_accessory/', status_code=status.HTTP_200_OK)
async def get_all_accessory(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Accessories)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_accessory/{accessory_id}/', status_code=status.HTTP_200_OK)
async def delete_labor(accessory_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Accessories,
                                          database_models.Accessories.id, accessory_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'accessories deleted successfully'}


@category.patch('/update_accessory/{accessory_id}/', status_code=status.HTTP_200_OK)
async def update_accessory(accessory_id: int, accessory_schema: UpdateAccessory, db: AsyncSession = Depends(get_db)):
    if accessory_schema.labor_id is not None:
        if accessory_schema.labor_id <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid labor id")

    db_data = await get_update_category(db, database_models.Accessories, database_models.Accessories.id,
                                        accessory_id, accessory_schema)
    return db_data


# ======quotations=======
@category.post('/create_quotation/', status_code=status.HTTP_201_CREATED)
async def create_quotation(quotation_schema: CreateQuotation, db: AsyncSession = Depends(get_db)):
    if quotation_schema.total_amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid price")
    user_id = 1
    db_data = await get_create_category(db, database_models.Quotation, quotation_schema, user_id)
    return db_data


@category.get('/get_quotation/{quotation_id}/', status_code=status.HTTP_200_OK)
async def get_quotation(quotation_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Quotation,
                                          database_models.Quotation.id, quotation_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_quotation/', status_code=status.HTTP_200_OK)
async def get_all_quotation(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.Quotation)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_quotation/{quotation_id}/', status_code=status.HTTP_200_OK)
async def delete_quotation(quotation_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.Quotation,
                                          database_models.Quotation.id, quotation_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'quotation deleted successfully'}


@category.patch('/update_quotation/{quotation_id}/', status_code=status.HTTP_200_OK)
async def update_quotation(quotation_id: int, quotation_schema: UpdateQuotation, db: AsyncSession = Depends(get_db)):
    if quotation_schema.total_amount is not None:
        if quotation_schema.total_amount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid amount")

    db_data = await get_update_category(db, database_models.Quotation, database_models.Quotation.id,
                                        quotation_id, quotation_schema)
    return db_data


# ======quotations_items=======
@category.post('/create_quotation_item/', status_code=status.HTTP_201_CREATED)
async def create_quotation_item(item_schema: CreateQuotationItems, db: AsyncSession = Depends(get_db)):
    if (item_schema.quantity and item_schema.price) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid amount")
    db_quotation = await get_db_category_by_id(db, database_models.Quotation, database_models.Quotation.id,
                                               item_schema.quotation_id)
    if db_quotation is None:
        return {'detail': 'Empty quotation'}
    user_id = 1
    db_data = await get_create_category(db, database_models.QuotationItem, item_schema, user_id)
    return db_data


@category.get('/get_quotation_item/{item_id}/', status_code=status.HTTP_200_OK)
async def get_quotation_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_data = await get_db_category_by_id(db, database_models.QuotationItem,
                                          database_models.QuotationItem.id, item_id)
    if db_data is None:
        return {'detail': 'Empty'}
    return db_data


@category.get('/get_all_quotation_item/', status_code=status.HTTP_200_OK)
async def get_all_quotation_item(db: AsyncSession = Depends(get_db)):
    db_data = await get_all_db_category(db, database_models.QuotationItem)
    if len(db_data) == 0:
        return {'detail': 'Empty'}
    return db_data


@category.delete('/delete_quotation_item/{item_id}/', status_code=status.HTTP_200_OK)
async def delete_quotation_item(item_id: int, db: AsyncSession = Depends(get_db), _=Depends(authenticate_user)):
    db_data = await get_db_category_by_id(db, database_models.QuotationItem,
                                          database_models.QuotationItem.id, item_id)
    if db_data is None:
        return {'detail': 'Empty'}
    await db.delete(db_data)
    await db.commit()
    return {'detail': 'quotation deleted successfully'}


@category.patch('/update_quotation_item/{item_id}/', status_code=status.HTTP_200_OK)
async def update_quotation_item(item_id: int, item_schema: UpdateQuotationItems, db: AsyncSession = Depends(get_db)):
    if item_schema.quantity is not None:
        if item_schema.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid amount")

    if item_schema.price is not None:
        if item_schema.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid amount")

    db_data = await get_update_category(db, database_models.QuotationItem, database_models.QuotationItem.id,
                                        item_id, item_schema)
    return db_data
