from PySide2.QtCore import QDate
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidgetItem, QDateEdit, \
    QTableWidget, QMessageBox, QComboBox, QHBoxLayout, QFormLayout, QWidget
from models.database_models import Panel, Frame, Inverter, Accessories, Labor, Battery, Quotation, \
    QuotationItem, ACCable, DCCable, Customer


class AddInvoiceDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Invoice")
        self.setModal(True)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_input = QComboBox()
        self.customer_name_input.currentIndexChanged.connect(self.populate_items)
        self.layout.addRow(self.customer_name_label, self.customer_name_input)

        self.walking_customer_label = QLabel("Walking Customer:")
        self.walking_customer_input = QLineEdit()
        self.layout.addRow(self.walking_customer_label, self.walking_customer_input)

        self.item_label = QLabel("Item:")
        self.item_input = QComboBox()
        self.layout.addRow(self.item_label, self.item_input)

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addRow(self.description_label, self.description_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addRow(self.quantity_label, self.quantity_input)

        self.price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.layout.addRow(self.price_label, self.price_input)

        self.total_label = QLabel("Total:")
        self.total_input = QLineEdit()
        self.layout.addRow(self.total_label, self.total_input)

        self.date_label = QLabel("Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addRow(self.date_label, self.date_edit)

        self.grand_total_label = QLabel("Grand Total:")
        self.grand_total_input = QLineEdit()
        self.layout.addRow(self.grand_total_label, self.grand_total_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_invoice)
        self.layout.addRow(self.add_button)

        # Populate the input fields
        self.populate_customers()

    def populate_customers(self):
        customers = self.db.query(Customer).all()
        self.customer_name_input.clear()
        self.customer_name_input.addItems([customer.customer_name for customer in customers])

    def populate_items(self):
        customer_name = self.customer_name_input.currentText()
        customer = self.db.query(Customer).filter_by(customer_name=customer_name).first()
        if customer:
            items = []
            panel = self.db.query(Panel).all()
            inverter = self.db.query(Inverter).all()
            frame = self.db.query(Frame).all()
            ac_cable = self.db.query(ACCable).all()
            dc_cable = self.db.query(DCCable).all()

            if len(panel) != 0:
                items.append(panel)
            if len(inverter) != 0:
                items.append(inverter)
            if len(frame) != 0:
                items.append(frame)
            if len(ac_cable) != 0:
                items.append(ac_cable)
            if len(dc_cable) != 0:
                items.append(dc_cable)

            for item in items:
                self.item_input.clear()
                self.item_input.addItems(item)
                self.fetch_item_details()

    def fetch_item_details(self):
        item_name = self.item_input.currentText()
        customer_name = self.customer_name_input.currentText()
        self.customer = self.db.query(Customer).filter_by(customer_name=customer_name).first()
        if self.customer:
            item = self.db.query(item_name).first()
            if item:
                self.quantity_input.setText(str(item.quantity))
                self.price_input.setText(str(item.price))
                self.total_input.setText(str(item.total))

    def add_invoice(self):
        user_id = self.user_id
        customer_name = self.customer_name_input.currentText()
        walking_customer = self.walking_customer_input.text()
        item = self.item_input.currentText()
        description = self.description_input.text()
        quantity = self.quantity_input.text()
        price = float(self.price_input.text()) if self.price_input.text() else None
        total = float(self.total_input.text()) if self.total_input.text() else None
        date = self.date_edit.date().toString("dd-MM-yyyy")
        grand_total = float(self.grand_total_input.text()) if self.grand_total_input.text() else None

        quotation = Quotation(
            user_id=user_id,
            customer_name=customer_name,
            walking_customer=walking_customer,
            item=item,
            description=description,
            quantity=quantity,
            price=price,
            total=total,
            date=date,
            grand_total=grand_total
        )

        self.db.add(quotation)
        self.db.commit()

        quotation_item = QuotationItem(
            user_id=user_id,
            customer_id=self.customer.id,
            item=item,
            description=description,
            quantity=quantity,
            price=price,
            total=total,
            date=date
        )

        self.db.add(quotation_item)
        self.db.commit()

        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(customer_name)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(walking_customer)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(item)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(description)))
        self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(quantity)))
        self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(price)))
        self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(total)))
        self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(date)))
        self.table_widget.setItem(row_count, 9, QTableWidgetItem(str(grand_total)))

        self.close()


class AddPanelDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Panel")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Product Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.capacity_label = QLabel("Capacity:")
        self.capacity_input = QLineEdit()
        self.layout.addWidget(self.capacity_label)
        self.layout.addWidget(self.capacity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_panel)
        self.layout.addWidget(self.add_button)

    def add_panel(self):
        if not (self.name_input.text() and self.brand_input.text() and self.type_input.text() and self.capacity_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.name_input.text() and self.brand_input.text() and self.type_input.text() and self.capacity_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            capacity = self.capacity_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Panel(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                capacity=capacity,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(capacity)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(sell_price)))

            self.close()


class AddInverterDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Inverter")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.power_rating_label = QLabel("Power Rating:")
        self.power_rating_input = QLineEdit()
        self.layout.addWidget(self.power_rating_label)
        self.layout.addWidget(self.power_rating_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_inverter)
        self.layout.addWidget(self.add_button)

    def add_inverter(self):
        if not (self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.power_rating_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.power_rating_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            power_rating = self.power_rating_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Inverter(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                power_rating=power_rating,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(power_rating)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(sell_price)))

            self.close()


class AddFrameDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Frame")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.width_label = QLabel("Width:")
        self.width_input = QLineEdit()
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)

        self.height_label = QLabel("Height:")
        self.height_input = QLineEdit()
        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_frame)
        self.layout.addWidget(self.add_button)

    def add_frame(self):
        if not (self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.width_input.text() and self.height_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.width_input.text() and self.height_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            width = self.width_input.text()
            height = self.height_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Frame(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                width=width,
                height=height,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(width)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(height)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(sell_price)))

            self.close()


class AddACCableDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add AC-Cable")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.size_label = QLabel("Size:")
        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_cable)
        self.layout.addWidget(self.add_button)

    def add_cable(self):
        if not (self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            size = self.size_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = ACCable(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                size=size,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(size)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(sell_price)))

            self.close()


class AddDCCableDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add DC-Cable")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.size_label = QLabel("Size:")
        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_cable)
        self.layout.addWidget(self.add_button)

    def add_cable(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            size = self.size_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = DCCable(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                size=size,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(size)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(sell_price)))

            self.close()


class AddBatteryDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Battery")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.warranty_label = QLabel("Warranty:")
        self.warranty_input = QLineEdit()
        self.layout.addWidget(self.warranty_label)
        self.layout.addWidget(self.warranty_input)

        self.capacity_label = QLabel("Capacity:")
        self.capacity_input = QLineEdit()
        self.layout.addWidget(self.capacity_label)
        self.layout.addWidget(self.capacity_input)

        self.voltage_label = QLabel("Voltage:")
        self.voltage_input = QLineEdit()
        self.layout.addWidget(self.voltage_label)
        self.layout.addWidget(self.voltage_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_battery)
        self.layout.addWidget(self.add_button)

    def add_battery(self):
        if not (self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.warranty_input.text() and self.capacity_input.text() and self.voltage_input.text() and self.price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.warranty_input.text() and self.capacity_input.text() and self.voltage_input.text() and self.price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            warranty = self.warranty_input.text()
            capacity = self.capacity_input.text()
            voltage = self.voltage_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Battery(
                user_id=user_id,
                product_name=product_name,
                brand=brand,
                typ=typ,
                warranty=warranty,
                capacity=capacity,
                voltage=voltage,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(warranty)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(capacity)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(voltage)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(sell_price)))

            self.close()


class AddAccessoriesDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Accessories")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.model_label = QLabel("Model:")
        self.model_input = QLineEdit()
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_customer)
        self.layout.addWidget(self.add_button)

    def add_customer(self):
        if not (self.product_name_input.text() and self.type_input.text() and self.model_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.type_input.text() and self.model_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_name = self.product_name_input.text()
            model = self.model_input.text()
            typ = self.type_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_label.text() else ''

            panel = Accessories(
                user_id=user_id,
                product_name=product_name,
                model=model,
                typ=typ,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(model)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(sell_price)))

            self.close()


class AddLaborDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Labor")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.labor_name_label = QLabel("Labor Name:")
        self.labor_name_input = QLineEdit()
        self.layout.addWidget(self.labor_name_label)
        self.layout.addWidget(self.labor_name_input)

        self.date_label = QLabel("Start Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.end_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.end_date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_edit)

        self.labor_cost_label = QLabel("Labor Cost:")
        self.labor_cost_input = QLineEdit()
        self.layout.addWidget(self.labor_cost_label)
        self.layout.addWidget(self.labor_cost_input)

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_labor)
        self.layout.addWidget(self.add_button)

    def add_labor(self):
        if not (self.labor_name_input.text() and self.date_edit.text() and self.labor_cost_input.text() and self.description_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.labor_name_input.text() and self.date_edit.text() and self.labor_cost_input.text() and self.description_input.text():
            user_id = self.user_id
            labor_name = self.labor_name_input.text()
            start_date = self.start_date_edit.date().toString("dd-MM-yyyy")
            labor_cost = int(self.labor_cost_input.text()) if self.labor_cost_input.text() else None
            description = self.description_input.text()

            panel = Labor(
                user_id=user_id,
                labor_name=labor_name,
                start_date=start_date,
                labor_cost=labor_cost,
                description=description
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            # self.table_widget.setItem(row_count, 1, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(labor_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(start_date)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(labor_cost)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(description)))

            self.close()


class AddCustomerDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Customer")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_input = QLineEdit()
        self.layout.addWidget(self.customer_name_label)
        self.layout.addWidget(self.customer_name_input)

        self.company_label = QLabel("Company:")
        self.company_input = QLineEdit()
        self.layout.addWidget(self.company_label)
        self.layout.addWidget(self.company_input)

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()
        self.layout.addWidget(self.phone_number_label)
        self.layout.addWidget(self.phone_number_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()
        self.layout.addWidget(self.city_label)
        self.layout.addWidget(self.city_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_labor)
        self.layout.addWidget(self.add_button)

    def add_labor(self):
        if not (self.customer_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.city_input.text() and self.address_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.customer_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.city_input.text() and self.address_input.text():
            user_id = self.user_id
            customer_name = self.customer_name_input.text()
            company = self.company_input.text()
            phone_number = self.phone_number_input.text()
            email = self.email_input.text()
            city = self.city_input.text()
            address = self.address_input.text()

            panel = Customer(
                user_id=user_id,
                customer_name=customer_name,
                company=company,
                phone_number=phone_number,
                email=email,
                city=city,
                address=address
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            # self.table_widget.setItem(row_count, 1, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(customer_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(company)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(phone_number)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(email)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(city)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(address)))

            self.close()


class AddQuotationItemDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Quotation Item")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.quotation_id_label = QLabel("Quotation Id:")
        self.quotation_id_input = QLineEdit()
        self.layout.addWidget(self.quotation_id_label)
        self.layout.addWidget(self.quotation_id_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QComboBox()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.total_price_label = QLabel("Total Price:")
        self.total_price_input = QLineEdit()
        self.layout.addWidget(self.total_price_label)
        self.layout.addWidget(self.total_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_quotation_item)
        self.layout.addWidget(self.add_button)

        # Populate the item input with data from the database
        self.populate_item_input()

    def populate_item_input(self):
        items_list = [
            (Panel, 'product_name'),
            (Inverter, 'product_name'),
            (Frame, 'product_name'),
            (ACCable, 'product_name'),
            (DCCable, 'product_name'),
            (Battery, 'product_name'),
            (Accessories, 'product_name')
        ]

        # Clear the current items in the combobox
        self.item_input.clear()

        # Add the items to the combobox
        for item_type, attribute_name in items_list:
            items = self.db.query(item_type).all()
            for item in items:
                item_name = getattr(item, attribute_name)
                self.item_input.addItem(item_name)

    def add_quotation_item(self):
        user_id = self.user_id
        quotation_id = self.quotation_id_input.text()
        product_name = self.product_name_input.currentText()
        brand = self.brand_input.text()
        typ = self.type_input.text()
        quantity = int(self.quantity_input.text()) if self.quantity_input.text() else ''
        sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''
        total_price = float(self.total_price_input.text()) if self.total_price_input.text() else ''

        quotation_item = QuotationItem(
            user_id=user_id,
            quotation_id=quotation_id,
            product_name=product_name,
            brand=brand,
            typ=typ,
            quantity=quantity,
            sell_price=sell_price,
            total_price=total_price
        )
        self.db.add(quotation_item)
        self.db.commit()

        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(quantity)))
        self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(sell_price)))
        self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(total_price)))

        self.close()


class AddQuotationDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Quotation")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_input = QComboBox()
        self.customer_name_input.currentIndexChanged.connect(self.populate_items)
        self.layout.addWidget(self.customer_name_label)
        self.layout.addWidget(self.customer_name_input)

        self.walking_customer_label = QLabel("Walk in Customer:")
        self.walking_customer_input = QLineEdit()
        self.layout.addWidget(self.walking_customer_label)
        self.layout.addWidget(self.walking_customer_input)

        self.date_label = QLabel("Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_edit)

        self.grand_total_label = QLabel("Grand Total:")
        self.grand_total_input = QLineEdit()
        self.layout.addWidget(self.grand_total_label)
        self.layout.addWidget(self.grand_total_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_quotation)
        self.layout.addWidget(self.add_button)

        # Populate the input fields
        self.populate_customers()
        self.fetch_item_details()

    def populate_customers(self):
        customers = self.db.query(Customer).all()
        self.customer_name_input.clear()
        self.customer_name_input.addItems([customer.customer_name for customer in customers])

    def populate_items(self):
        customer_name = self.customer_name_input.currentText()
        customer = self.db.query(Customer).filter_by(customer_name=customer_name).first()
        if customer:
            items = self.db.query(Panel).all()
            self.item_input.clear()
            self.item_input.addItems([item.name for item in items])

    # def fetch_item_details(self):
    #     item_name = self.item_input.currentText()
    #     print(item_name)
    #     item = self.db.query(QuotationItem).filter_by(item=item_name).first()
    #     if item:
    #         self.description_input.setText(str(item.description))
    #         self.quantity_input.setText(str(item.quantity))
    #         self.price_input.setText(str(item.price))
    #         self.total_input.setText(str(item.total))

    def add_quotation(self):
        user_id = self.user_id
        customer_name = self.customer_name_input.currentText()
        walk_in_customer = self.walking_customer_input.text()
        date = self.date_edit.date().toString("dd-MM-yyyy")
        grand_total = float(self.grand_total_input.text()) if self.grand_total_input.text() else ''

        panel = Quotation(
            user_id=user_id,
            customer_name=customer_name,
            walk_in_customer=walk_in_customer,
            date=date,
            grand_total=grand_total
        )
        self.db.add(panel)
        self.db.commit()

        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(customer_name)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(walk_in_customer)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(date)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(grand_total)))

        self.close()


class UpdateItemDialog(QDialog):
    def __init__(self, db, todo_stack):
        super().__init__()
        self.db = db
        self.todo_stack = todo_stack
        self.update_item()

    def update_item(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        # Get the selected item
        selected_items = table_widget.selectedItems()

        # Check if an item is selected
        if not selected_items:
            QMessageBox.warning(self, "Error", "No item selected.")
            return

        # Get the row index of the selected item
        selected_row = selected_items[0].row()

        # Get the item ID from the first column of the selected row
        item = table_widget.item(selected_row, 0)
        item_id = item.text() if item is not None else ""

        # Open an update dialog or window for the selected item and update the data
        if current_index == 1:
            # Update Panel item
            panel = self.db.query(Panel).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if panel:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                capacity = table_widget.item(selected_row, 4).text()
                purchase_price = table_widget.item(selected_row, 5).text()
                sell_price = table_widget.item(selected_row, 6).text()

                # Update the panel data
                panel.product_name = product_name
                panel.brand = brand
                panel.typ = typ
                panel.capacity = capacity
                panel.purchase_price = purchase_price
                panel.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 2:
            # Update Inverter item
            inverter = self.db.query(Inverter).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if inverter:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                power_rating = table_widget.item(selected_row, 4).text()
                purchase_price = table_widget.item(selected_row, 5).text()
                sell_price = table_widget.item(selected_row, 6).text()

                # Update the inverter data
                inverter.product_name = product_name
                inverter.brand = brand
                inverter.typ = typ
                inverter.power_rating = power_rating
                inverter.purchase_price = purchase_price
                inverter.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 3:
            # Update Frame item
            frame = self.db.query(Frame).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if frame:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 0).text()
                brand = table_widget.item(selected_row, 1).text()
                typ = table_widget.item(selected_row, 2).text()
                width = table_widget.item(selected_row, 3).text()
                height = table_widget.item(selected_row, 4).text()
                purchase_price = table_widget.item(selected_row, 5).text()
                sell_price = table_widget.item(selected_row, 6).text()

                # Update the inverter data
                frame.product_name = product_name
                frame.brand = brand
                frame.typ = typ
                frame.width = width
                frame.height = height
                frame.purchase_price = purchase_price
                frame.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 4:
            # Update AC-Cable item
            coil = self.db.query(ACCable).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if coil:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                size = table_widget.item(selected_row, 4).text()
                purchase_price = table_widget.item(selected_row, 5).text()
                sell_price = table_widget.item(selected_row, 6).text()

                # Update the inverter data
                coil.product_name = product_name
                coil.brand = brand
                coil.typ = typ
                coil.size = size
                coil.purchase_price = purchase_price
                coil.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 5:
            # Update DC-Cable item
            coil = self.db.query(DCCable).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if coil:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                size = table_widget.item(selected_row, 4).text()
                purchase_price = table_widget.item(selected_row, 5).text()
                sell_price = table_widget.item(selected_row, 6).text()

                # Update the inverter data
                coil.product_name = product_name
                coil.brand = brand
                coil.typ = typ
                coil.size = size
                coil.purchase_price = purchase_price
                coil.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 6:
            # Update Battery item
            battery = self.db.query(Battery).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if battery:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                warranty = table_widget.item(selected_row, 4).text()
                capacity = table_widget.item(selected_row, 5).text()
                voltage = table_widget.item(selected_row, 6).text()
                purchase_price = table_widget.item(selected_row, 7).text()
                sell_price = table_widget.item(selected_row, 8).text()

                # Update the inverter data
                battery.product_name = product_name
                battery.brand = brand
                battery.typ = typ
                battery.warranty = warranty
                battery.capacity = capacity
                battery.voltage = voltage
                battery.purchase_price = purchase_price
                battery.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()

        elif current_index == 7:
            # Update Accessories item
            accessory = self.db.query(Accessories).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if accessory:
                # Get the updated data from the user
                product_name = table_widget.item(selected_row, 1).text()
                brand = table_widget.item(selected_row, 2).text()
                typ = table_widget.item(selected_row, 3).text()
                purchase_price = table_widget.item(selected_row, 4).text()
                sell_price = table_widget.item(selected_row, 5).text()

                # Update the inverter data
                accessory.product_name = product_name
                accessory.brand = brand
                accessory.typ = typ
                accessory.purchase_price = purchase_price
                accessory.sell_price = sell_price

                # Commit the changes to the database
                self.db.commit()


# ================invoices forme===================
class InvoiceForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Invoice")
        self.setFixedSize(400, 300)

        # Create the main layout
        main_layout = QHBoxLayout()

        # Create a layout for the first column of input fields
        first_column_layout = QVBoxLayout()

        # Create the first input field
        first_input = QLineEdit()
        first_column_layout.addWidget(QLabel("Customer:"))
        first_column_layout.addWidget(first_input)

        # Create the third input field
        third_input = QLineEdit()
        first_column_layout.addWidget(QLabel("Product:"))
        first_column_layout.addWidget(third_input)

        # Create a layout for the second column of input fields
        second_column_layout = QVBoxLayout()

        # Create the second input field
        second_input = QLineEdit()
        second_column_layout.addWidget(QLabel("Address:"))
        second_column_layout.addWidget(second_input)

        # Create the fourth input field
        fourth_input = QLineEdit()
        second_column_layout.addWidget(QLabel("Quantity:"))
        second_column_layout.addWidget(fourth_input)

        # Add the columns to the main layout
        main_layout.addLayout(first_column_layout)
        main_layout.addLayout(second_column_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        # Add a button to create the invoice
        create_button = QPushButton("Create Invoice")
        main_layout.addWidget(create_button)

        # Connect the button click to a function
        create_button.clicked.connect(self.create_invoice)

    def create_invoice(self):
        # Retrieve the values from the input fields
        customer = self.findChild(QLineEdit).text()
        address = self.findChild(QLineEdit, "", 1).text()
        product = self.findChild(QLineEdit, "", 2).text()
        quantity = self.findChild(QLineEdit, "", 3).text()

        # Perform the invoice creation logic
        # ...
        # Print the values for demonstration purposes
        print(f"Customer: {customer}")
        print(f"Address: {address}")
        print(f"Product: {product}")
        print(f"Quantity: {quantity}")
