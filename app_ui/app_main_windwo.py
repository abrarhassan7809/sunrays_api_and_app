from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QComboBox, QLineEdit, QTextEdit, QAction, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QStackedWidget, \
    QAbstractItemView
import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

from app_ui.cetagories import AddPanelDialog, AddInverterDialog, AddFrameDialog, AddACCableDialog, AddDCCableDialog, \
    AddBatteryDialog, AddAccessoriesDialog, UpdateItemDialog
from models.database_config import get_db
from models.database_models import User, Panel, Inverter, ACCable, DCCable, Frame, Labor, Quotation, \
    Battery, \
    Accessories, QuotationItem, Expanse, Customer

from models.database_models import Panel


class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.db = next(get_db())
        self.user = self.db.query(User).filter(User.token == self.token).first()

        # Store table_widget as an instance variable
        self.table_widget = None

        self.setWindowTitle("System Inventory")
        self.setFixedSize(self.screen().size())
        self.setMinimumSize(900, 600)

        # Create the main layout
        main_layout = QVBoxLayout()
        self.set_app_icon()

        # Create menu bar
        menu_bar = self.menuBar()
        file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
        file_save.setShortcut('Ctrl+S')
        file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
        file_exit.setShortcut('Ctrl+Q')
        file_exit.triggered.connect(self.close)

        action_edit = QAction(QIcon('app_icons/save.svg'), "Edit", self)
        action_edit.setShortcut('Ctrl+E')
        action_help = QAction(QIcon('app_icons/save.svg'), "Help", self)
        action_help.setShortcut('Ctrl+H')

        # Add File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(file_save)
        file_menu.addAction(file_exit)

        view_menu = menu_bar.addMenu("View")
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

        # Create the header part
        header_layout = QHBoxLayout()
        self.body_label = QLabel('')
        self.body_combo = QComboBox()
        self.body_combo.addItem('')
        self.body_combo.addItem('Panel')
        self.body_combo.addItem('Inverter')
        self.body_combo.addItem('Frame')
        self.body_combo.addItem('AC Cable')
        self.body_combo.addItem('DC Cable')
        self.body_combo.addItem('Battery')
        self.body_combo.addItem('Accessories')

        customer_button = QPushButton('Customer')
        invoices_button = QPushButton('Invoices')
        user_button = QPushButton('User')
        header_layout.addWidget(self.body_combo)
        header_layout.addWidget(customer_button)
        header_layout.addWidget(invoices_button)
        header_layout.addStretch()
        header_layout.addWidget(user_button)

        # Create the bottom part
        bottom_layout = QHBoxLayout()
        create_invoice_button = QPushButton('Create Invoice')
        create_button = QPushButton('Create')
        update_button = QPushButton('Update')
        delete_button = QPushButton('Delete')

        bottom_layout.addWidget(create_button)
        bottom_layout.addWidget(update_button)
        bottom_layout.addWidget(delete_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(create_invoice_button)

        # Add the header, body, and bottom layouts to the main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.body_label)
        main_layout.addLayout(bottom_layout)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect signals to slots
        self.body_combo.currentIndexChanged.connect(self.show_data)
        customer_button.clicked.connect(self.show_customers)
        invoices_button.clicked.connect(self.show_invoices)
        create_invoice_button.clicked.connect(self.create_invoice)
        create_button.clicked.connect(self.create_action)
        update_button.clicked.connect(self.update_action)
        delete_button.clicked.connect(self.delete_action)

        # Initialize the todo_stack
        self.todo_stack = QStackedWidget()

    def show_data(self, index):
        item = self.body_combo.currentText()

        if index == 0:
            pass

        elif item == 'Panel':
            headers = ["Product Name", "Brand", "Type", "Capacity", "Purchase Price", "Sell Price"]
            db_data = self.db.query(Panel).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.capacity)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'Inverter':
            headers = ["Product Name", "Brand", "Type", "Power Rating", "Purchase Price", "Sell Price"]
            db_data = self.db.query(Inverter).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.power_rating)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'Frame':
            headers = ["Product Name", "Brand", "Type", "Width", "Height", "Purchase Price", "Sell Price"]
            db_data = self.db.query(Frame).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.width)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.height)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'AC Cable':
            headers = ["Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
            db_data = self.db.query(ACCable).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.size)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'DC Cable':
            headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
            db_data = self.db.query(DCCable).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.size)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'Battery':
            headers = ["#", "Product Name", "Brand", "Type", "Warranty", "Capacity", "Voltage", "Purchase Price",
                       "Sell Price"]
            db_data = self.db.query(Battery).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.warranty)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.capacity)))
                table_widget.setItem(row, 5, QTableWidgetItem(item.voltage))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif item == 'Accessories':
            headers = ["#", "Product Name", "Model", "Type", "Purchase Price", "Sell Price"]
            db_data = self.db.query(Accessories).all()

            # Create the table widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Add items to the table widget
            table_widget.setRowCount(len(db_data))

            for row, item in enumerate(db_data):
                # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.model)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.sell_price)))

                # Store the item ID as a custom data role
                table_widget.item(row, 0).setData(Qt.UserRole, item.id)

            # Set the header section resize mode to Stretch
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Replace the body_label with the table_widget
            main_layout = self.centralWidget().layout()
            main_layout.replaceWidget(self.body_label, table_widget)
            self.body_label = table_widget

            # Set the selection behavior to select entire rows
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        else:
            return

    def set_app_icon(self):
        app_icon = QIcon("app_icons/401262_archlinux_icon.png")
        self.setWindowIcon(app_icon)

    def show_customers(self):
        pass

    def show_invoices(self):
        pass

    def create_invoice(self):
        # Perform the create_ action based on the current window
        pass

    def create_action(self):
        if self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

        current_index = self.body_combo.currentIndex()
        # todo_widget = self.todo_stack.widget(current_index)

        if current_index == 1:  # Panel
            table_widget = QTableWidget()
            add_panel_dialog = AddPanelDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 2:  # Inverter
            table_widget = QTableWidget()
            add_panel_dialog = AddInverterDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 3:  # Frame
            table_widget = QTableWidget()
            add_panel_dialog = AddFrameDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 4:  # AC Cable
            table_widget = QTableWidget()
            add_panel_dialog = AddACCableDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 5:  # DC Cable
            table_widget = QTableWidget()
            add_panel_dialog = AddDCCableDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 6:  # Battery
            table_widget = QTableWidget()
            add_panel_dialog = AddBatteryDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        elif current_index == 7:  # Accessories
            table_widget = QTableWidget()
            add_panel_dialog = AddAccessoriesDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

            # Update the main window after adding the panel
            self.show_data(current_index)

        # Assign the table_widget to self.body_label
        # self.table_widget = table_widget
        self.body_label = self.table_widget

        # Replace the body_label with the table_widget on the UI
        main_layout = self.centralWidget().layout()
        main_layout.replaceWidget(self.body_label, self.table_widget)

        # Set the selection behavior to select entire rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def update_action(self):
        if self.user is not None:
            update_item_dialog = UpdateItemDialog(self.db, self.todo_stack)
            update_item_dialog.exec_()
        else:
            QMessageBox.warning(self, "Error", "Please login first.")

    def delete_action(self):
        if self.user is not None:
            # Get the selected item from the table widget
            selected_items = self.body_label.selectedItems()

            if len(selected_items) > 0:
                # Get the row index of the selected item
                row = selected_items[0].row()

                # Retrieve the item ID from the custom data role
                item_id = self.body_label.item(row, 0).data(Qt.UserRole)

                # Determine the current selected item in the combo box
                current_index = self.body_combo.currentIndex()

                if current_index == 1:  # Panel
                    item = self.db.query(Panel).get(item_id)
                elif current_index == 2:  # Inverter
                    item = self.db.query(Inverter).get(item_id)
                elif current_index == 3:  # Frame
                    item = self.db.query(Frame).get(item_id)
                elif current_index == 4:  # AC Cable
                    item = self.db.query(ACCable).get(item_id)
                elif current_index == 5:  # DC Cable
                    item = self.db.query(DCCable).get(item_id)
                elif current_index == 6:  # Battery
                    item = self.db.query(Battery).get(item_id)
                elif current_index == 7:  # Accessories
                    item = self.db.query(Accessories).get(item_id)
                else:
                    return

                # Confirm the deletion with a QMessageBox
                reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this item?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    # Remove the item from the database
                    self.db.delete(item)
                    self.db.commit()

                    # Remove the selected row from the table widget
                    self.body_label.removeRow(row)

                    QMessageBox.information(self, "Success", "Item deleted successfully.")
            else:
                QMessageBox.warning(self, "Error", "Please select an item to delete.")
        else:
            QMessageBox.warning(self, "Error", "Please login first.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow('token')
    window.show()
    sys.exit(app.exec_())

