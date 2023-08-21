# from PySide2 import QtWidgets
# from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
#     QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox, QSizePolicy, QInputDialog, \
#     QDialogButtonBox, QFormLayout, QToolButton, QComboBox
# from PySide2.QtCore import Qt, Signal, QSize
# from functools import partial
# from PySide2.QtGui import QIcon
#
# from app_ui import cetagories
# from app_ui.cetagories import AddPanelDialog, AddQuotationDialog, AddAccessoriesDialog, AddLaborDialog, \
#     AddBatteryDialog, AddFrameDialog, AddInverterDialog, AddQuotationItemDialog, AddCustomerDialog, AddDCCableDialog, \
#     AddACCableDialog, AddInvoiceDialog
# from models.database_config import get_db
# from models.database_models import User, Panel, Inverter, ACCable, DCCable, Frame, Labor, Quotation, \
#     Battery, \
#     Accessories, QuotationItem, Expanse, Customer
# import sys
#
# HORIZONTAL_HEADERS = ["Header", "Header", "Header", "Header", "Header", "Header", "Header"]
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, token):
#         super().__init__()
#         self.token = token
#         self.db = next(get_db())
#         self.user = self.db.query(User).filter(User.token == self.token).first()
#         self.init_ui()
#
#         # Add the table_widget attribute
#         self.table_widget = None
#
#     def init_ui(self):
#         self.setWindowTitle("System Inventory")
#         self.setFixedSize(self.screen().size())
#         self.setMinimumSize(900, 600)
#
#         # Create menu bar
#         menu_bar = self.menuBar()
#         self.set_app_icon()
#
#         file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
#         file_save.setShortcut('Ctrl+S')
#         file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
#         file_exit.setShortcut('Ctrl+Q')
#         file_exit.triggered.connect(self.close)
#
#         action_edit = QAction(QIcon('app_icons/save.svg'), "Edit", self)
#         action_edit.setShortcut('Ctrl+E')
#         action_help = QAction(QIcon('app_icons/save.svg'), "Help", self)
#         action_help.setShortcut('Ctrl+H')
#
#         # Add File menu
#         file_menu = menu_bar.addMenu("File")
#         file_menu.addAction(file_save)
#         file_menu.addAction(file_exit)
#
#         view_menu = menu_bar.addMenu("View")
#         edit_menu = menu_bar.addMenu("Edit")
#         help_menu = menu_bar.addMenu("Help")
#
#         # Create the central widget
#         central_widget = QWidget()
#
#         # Create main layout for the central widget
#         main_layout = QHBoxLayout()
#         central_widget.setLayout(main_layout)
#
#         # Create layout for the left menu
#         menu_layout = QVBoxLayout()
#         menu_widget = QWidget()
#         menu_widget.setLayout(menu_layout)
#
#         # Move the left menu button to the top position
#         menu_layout.setAlignment(Qt.AlignTop)
#
#         # Create a dropdown list for menu items
#         menu_combo = QComboBox()
#         menu_layout.addWidget(menu_combo)
#
#         customer_button = QPushButton("Customers")
#         menu_layout.addWidget(customer_button)
#         customer_button.clicked.connect(self.add_customer)
#
#         invoices_button = QPushButton("Invoices")
#         menu_layout.addWidget(invoices_button)
#         invoices_button.clicked.connect(self.show_invoices)
#
#         # Add menu items to the left menu
#         menu_items = [
#             ("", ""),
#             ("Panel", "app_icons/icons8-solar-panel-40.png"),
#             ("Inverter", "app_icons/icons8-inverter-65.png"),
#             ("Frame", "app_icons/icons8-frame-67.png"),
#             ("AC-Cable", "app_icons/icons8-coil-48.png"),
#             ("DC-Cable", "app_icons/icons8-coil-48.png"),
#             ("Batteries", "app_icons/icons8-battery-64.png"),
#             ("Accessories", "app_icons/icons8-cart-48.png"),
#         ]
#
#         # Create a stacked widget for todo windows
#         self.todo_stack = QStackedWidget()
#
#         for item_text, icon_path in menu_items:
#             menu_combo.addItem(QIcon(icon_path), item_text)
#             index = menu_combo.currentIndex()
#             menu_combo.activated.connect(partial(self.on_menu_item_clicked))
#
#             # Create a todo window widget for each menu item
#             todo_widget = QWidget()
#             todo_layout = QVBoxLayout()
#             todo_widget.setLayout(todo_layout)
#
#             # Add table widget to the todo window widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(HORIZONTAL_HEADERS))
#             table_widget.setHorizontalHeaderLabels(HORIZONTAL_HEADERS)
#             table_widget.verticalHeader().setVisible(False)
#             table_widget.horizontalHeader().setStretchLastSection(True)
#             todo_layout.addWidget(table_widget)
#
#             # Create button layout
#             button_layout = QHBoxLayout()
#             button_layout.setMargin(10)
#
#             # Add spacer item to push buttons to the right side
#             spacer_item = QWidget()
#             spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#             button_layout.addWidget(spacer_item)
#
#             # Create the buttons
#             invoice_button = QPushButton("Invoice")
#             create_button = QPushButton("Add")
#             update_button = QPushButton("Update")
#             delete_button = QPushButton("Delete")
#
#             button_layout.addWidget(invoice_button)
#             button_layout.addWidget(create_button)
#             button_layout.addWidget(update_button)
#             button_layout.addWidget(delete_button)
#
#             todo_layout.addLayout(button_layout)
#
#             invoice_button.clicked.connect(self.add_invoice)
#             create_button.clicked.connect(self.open_add_window)
#             update_button.clicked.connect(self.update_data)
#             delete_button.clicked.connect(self.delete_item)
#
#             self.todo_stack.addWidget(todo_widget)
#
#         # Add left menu and right todos to the main layout
#         main_layout.addWidget(menu_widget)
#         main_layout.addWidget(self.todo_stack)
#
#         # Set the central widget
#         self.setCentralWidget(central_widget)
#
#         # Show the main window
#         self.show()
#
#     def set_app_icon(self):
#         app_icon = QIcon("app_icons/401262_archlinux_icon.png")
#         self.setWindowIcon(app_icon)
#
#     def update_data(self):
#         if self.user is not None:
#             cetagories.UpdateItemDialog(self.db, self.todo_stack)
#         else:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def delete_item(self):
#         if self.user is not None:
#             # Get the current todo window index
#             current_index = self.todo_stack.currentIndex()
#
#             # Get the corresponding todo window widget
#             todo_widget = self.todo_stack.widget(current_index)
#
#             # Get the table widget from the todo window widget
#             table_widget = todo_widget.findChild(QTableWidget)
#
#             # Get the selected item
#             selected_items = table_widget.selectedItems()
#
#             # Check if an item is selected
#             if not selected_items:
#                 QMessageBox.warning(self, "Error", "No item selected.")
#                 return
#
#             # Get the row indexes of the selected items
#             selected_rows = set()
#             for item in selected_items:
#                 selected_rows.add(item.row())
#
#             # Display a confirmation dialog
#             confirmation = QMessageBox.question(
#                 self,
#                 "Confirmation",
#                 "Are you sure you want to delete the selected item(s)?",
#                 QMessageBox.Yes | QMessageBox.No,
#                 QMessageBox.No
#             )
#
#             if confirmation == QMessageBox.Yes:
#                 # Remove the selected item(s) from the table widget
#                 for row in sorted(selected_rows, reverse=True):
#                     item_id = table_widget.item(row, 0).text()
#                     self.delete_item_from_database(current_index, int(item_id))
#                     table_widget.removeRow(row)
#
#                 # Commit the changes to the database
#                 self.db.commit()
#
#         else:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def delete_item_from_database(self, index, item_id):
#         YourModel = None
#         if index == 0:
#             YourModel = Panel
#         if index == 1:
#             YourModel = Inverter
#         if index == 2:
#             YourModel = Frame
#         if index == 3:
#             YourModel = ACCable
#         if index == 4:
#             YourModel = DCCable
#         if index == 5:
#             YourModel = Battery
#         if index == 6:
#             YourModel = Accessories
#         try:
#             # Retrieve the item from the database using the item_id
#             item = self.db.query(YourModel).get(item_id)
#
#             if item is not None:
#                 # Delete the item from the database
#                 self.db.delete(item)
#                 self.db.commit()
#
#                 # Remove the item from the UI or update the UI accordingly
#
#                 QMessageBox.information(self, 'Success', 'Item deleted successfully.')
#             else:
#                 QMessageBox.warning(self, 'Error', 'Item not found.')
#
#         except Exception as e:
#             QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
#
#     def on_menu_item_clicked(self, index):
#         # Check if the clicked menu item is already selected
#         if index == self.todo_stack.currentIndex():
#             return
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(index)
#
#         # Find the existing table widget in the todo widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if table_widget is None:
#             # Create a new table widget if it doesn't exist
#             table_widget = QTableWidget(todo_widget)
#             todo_widget.layout().addWidget(table_widget)
#         else:
#             table_widget.clear()
#
#         if index == 0:
#             pass
#
#         if index == 1:
#             headers = ["#", "Product Name", "Brand", "Type", "Capacity", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Panel).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 2:
#             headers = ["#", "Product Name", "Brand", "Type", "Power Rating", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Inverter).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.power_rating)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 3:
#             headers = ["#", "Product Name", "Brand", "Type", "Width", "Height", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Frame).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.width)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.height)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 7, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 4:
#             headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(ACCable).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 5:
#             headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(DCCable).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 6:
#             headers = ["#", "Product Name", "Brand", "Type", "Warranty", "Capacity", "Voltage", "Purchase Price",
#                        "Sell Price"]
#             db_data = self.db.query(Battery).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.warranty)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(item.voltage))
#                 table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 7:
#             headers = ["#", "Product Name", "Brand", "Type", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Accessories).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#         else:
#             return
#
#         # Resize the columns to fit the content
#         table_widget.resizeColumnsToContents()
#
#         # Set the current todo window index to match the clicked menu item
#         self.todo_stack.setCurrentIndex(index)
#
#     def add_customer(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         headers = ["Customer Name", "Company", "Phone Number", "Email", "City", "Address"]
#         db_data = self.db.query(Customer).all()
#
#         # Set the new headers
#         table_widget.setColumnCount(len(headers))
#         table_widget.setHorizontalHeaderLabels(headers)
#
#         # Add items to the table widget
#         table_widget.setRowCount(len(db_data))
#
#         for row, item in enumerate(db_data):
#             # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#             table_widget.setItem(row, 0, QTableWidgetItem(str(item.customer_name)))
#             table_widget.setItem(row, 1, QTableWidgetItem(str(item.company)))
#             table_widget.setItem(row, 2, QTableWidgetItem(str(item.phone_number)))
#             table_widget.setItem(row, 3, QTableWidgetItem(str(item.email)))
#             table_widget.setItem(row, 4, QTableWidgetItem(str(item.city)))
#             table_widget.setItem(row, 5, QTableWidgetItem(str(item.address)))
#
#     def show_invoices(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         headers = ["Invoice Code", "Product Name", "Brand", "Type", "Quantity", "Price", "Total"]
#         db_data = self.db.query(QuotationItem).all()
#
#         # Set the new headers
#         table_widget.setColumnCount(len(headers))
#         table_widget.setHorizontalHeaderLabels(headers)
#
#         # Add items to the table widget
#         table_widget.setRowCount(len(db_data))
#
#         for row, item in enumerate(db_data):
#             # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#             table_widget.setItem(row, 0, QTableWidgetItem(str(item.item)))
#             table_widget.setItem(row, 1, QTableWidgetItem(str(item.description)))
#             table_widget.setItem(row, 2, QTableWidgetItem(str(item.quantity)))
#             table_widget.setItem(row, 3, QTableWidgetItem(str(item.price)))
#             table_widget.setItem(row, 4, QTableWidgetItem(str(item.total)))
#
#     def add_invoice(self):
#         print('invoice')
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if self.user:
#             add_invoice_dialog = AddInvoiceDialog(self.db, self.user.id, table_widget)
#             add_invoice_dialog.exec_()
#
#         elif self.user is None:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def open_add_window(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if self.user is None:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#         elif current_index == 1:  # Panel
#             add_panel_dialog = AddPanelDialog(self.db, self.user.id, table_widget)
#             add_panel_dialog.exec_()
#
#         elif current_index == 2:  # Inverter
#             add_inverter_dialog = AddInverterDialog(self.db, self.user.id, table_widget)
#             add_inverter_dialog.exec_()
#
#         elif current_index == 3:  # Frame
#             add_frame_dialog = AddFrameDialog(self.db, self.user.id, table_widget)
#             add_frame_dialog.exec_()
#
#         elif current_index == 4:  # AC-Cable
#             add_ac_cable_dialog = AddACCableDialog(self.db, self.user.id, table_widget)
#             add_ac_cable_dialog.exec_()
#
#         elif current_index == 5:  # DC-Cable
#             add_dc_cable_dialog = AddDCCableDialog(self.db, self.user.id, table_widget)
#             add_dc_cable_dialog.exec_()
#
#         elif current_index == 6:  # Battery
#             add_battery_dialog = AddBatteryDialog(self.db, self.user.id, table_widget)
#             add_battery_dialog.exec_()
#
#         elif current_index == 7:  # Accessories
#             add_accessories_dialog = AddAccessoriesDialog(self.db, self.user.id, table_widget)
#             add_accessories_dialog.exec_()
#
#     def handle_added_item(self, item_data):
#         # Get the current todo window index
#         current_index = self.todo_stack.currentIndex()
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(current_index)
#
#         # Get the table widget from the todo window widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         # Validate the item data
#         if all(item_data.values()):
#             # Add the item to the table widget
#             row_count = table_widget.rowCount()
#             table_widget.insertRow(row_count)
#
#             for column, data in enumerate(item_data.values()):
#                 item = QTableWidgetItem(data)
#                 item.setTextAlignment(Qt.AlignCenter)
#                 table_widget.setItem(row_count, column, item)
#         else:
#             # Show an error message if any field is empty
#             QMessageBox.warning(self, "Error", "All fields are required.")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow('token')
#     sys.exit(app.exec_())

# ==============2=================
# from PySide2 import QtWidgets
# from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
#     QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox, QSizePolicy, QInputDialog, \
#     QDialogButtonBox, QFormLayout, QToolButton, QComboBox
# from PySide2.QtCore import Qt, Signal, QSize
# from functools import partial
# from PySide2.QtGui import QIcon
#
# from app_ui import cetagories
# from app_ui.cetagories import AddPanelDialog, AddQuotationDialog, AddAccessoriesDialog, AddLaborDialog, \
#     AddBatteryDialog, AddFrameDialog, AddInverterDialog, AddQuotationItemDialog, AddCustomerDialog, AddDCCableDialog, \
#     AddACCableDialog, AddInvoiceDialog
# from models.database_config import get_db
# from models.database_models import User, Panel, Inverter, ACCable, DCCable, Frame, Labor, Quotation, \
#     Battery, \
#     Accessories, QuotationItem, Expanse, Customer
# import sys
#
# HORIZONTAL_HEADERS = ["Header", "Header", "Header", "Header", "Header", "Header", "Header"]
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, token):
#         super().__init__()
#         self.token = token
#         self.db = next(get_db())
#         self.user = self.db.query(User).filter(User.token == self.token).first()
#         self.init_ui()
#
#         # Add the table_widget attribute
#         self.table_widget = None
#
#     def init_ui(self):
#         self.setWindowTitle("System Inventory")
#         self.setFixedSize(self.screen().size())
#         self.setMinimumSize(900, 600)
#
#         # Create menu bar
#         menu_bar = self.menuBar()
#         self.set_app_icon()
#
#         file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
#         file_save.setShortcut('Ctrl+S')
#         file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
#         file_exit.setShortcut('Ctrl+Q')
#         file_exit.triggered.connect(self.close)
#
#         action_edit = QAction(QIcon('app_icons/save.svg'), "Edit", self)
#         action_edit.setShortcut('Ctrl+E')
#         action_help = QAction(QIcon('app_icons/save.svg'), "Help", self)
#         action_help.setShortcut('Ctrl+H')
#
#         # Add File menu
#         file_menu = menu_bar.addMenu("File")
#         file_menu.addAction(file_save)
#         file_menu.addAction(file_exit)
#
#         view_menu = menu_bar.addMenu("View")
#         edit_menu = menu_bar.addMenu("Edit")
#         help_menu = menu_bar.addMenu("Help")
#
#         # Create the central widget
#         central_widget = QWidget()
#
#         # Create main layout for the central widget
#         main_layout = QHBoxLayout()
#         central_widget.setLayout(main_layout)
#
#         # Create layout for the left menu
#         menu_layout = QVBoxLayout()
#         menu_widget = QWidget()
#         menu_widget.setLayout(menu_layout)
#
#         # Move the left menu button to the top position
#         menu_layout.setAlignment(Qt.AlignTop)
#
#         # Create a dropdown list for menu items
#         menu_combo = QComboBox()
#         menu_layout.addWidget(menu_combo)
#
#         customer_button = QPushButton("Customers")
#         menu_layout.addWidget(customer_button)
#         customer_button.clicked.connect(self.add_customer)
#
#         invoices_button = QPushButton("Invoices")
#         menu_layout.addWidget(invoices_button)
#         invoices_button.clicked.connect(self.show_invoices)
#
#         # Add menu items to the left menu
#         menu_items = [
#             ("Panel", "app_icons/icons8-solar-panel-40.png"),
#             ("Inverter", "app_icons/icons8-inverter-65.png"),
#             ("Frame", "app_icons/icons8-frame-67.png"),
#             ("AC-Cable", "app_icons/icons8-coil-48.png"),
#             ("DC-Cable", "app_icons/icons8-coil-48.png"),
#             # ("Labor", "app_icons/icons8-labor-64.png"),
#             # ("Customer", "app_icons/icons8-labor-64.png"),
#             ("Batteries", "app_icons/icons8-battery-64.png"),
#             ("Accessories", "app_icons/icons8-cart-48.png"),
#             # ("Q-Item", "app_icons/icons8-open-box-64.png"),
#             # ("Quotation", "app_icons/icons8-quotation-64.png"),
#         ]
#
#         # Create a stacked widget for todo windows
#         self.todo_stack = QStackedWidget()
#
#         for item_text, icon_path in menu_items:
#             menu_combo.addItem(QIcon(icon_path), item_text)
#             index = menu_combo.currentIndex()
#             menu_combo.activated.connect(partial(self.on_menu_item_clicked))
#
#             # Create a todo window widget for each menu item
#             todo_widget = QWidget()
#             todo_layout = QVBoxLayout()
#             todo_widget.setLayout(todo_layout)
#
#             # Add table widget to the todo window widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(HORIZONTAL_HEADERS))
#             table_widget.setHorizontalHeaderLabels(HORIZONTAL_HEADERS)
#             table_widget.verticalHeader().setVisible(False)
#             table_widget.horizontalHeader().setStretchLastSection(True)
#             todo_layout.addWidget(table_widget)
#
#             # Create button layout
#             button_layout = QHBoxLayout()
#             button_layout.setMargin(10)
#
#             # Add spacer item to push buttons to the right side
#             spacer_item = QWidget()
#             spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#             button_layout.addWidget(spacer_item)
#
#             # Create the buttons
#             invoice_button = QPushButton("Invoice")
#             create_button = QPushButton("Add")
#             update_button = QPushButton("Update")
#             delete_button = QPushButton("Delete")
#
#             button_layout.addWidget(invoice_button)
#             button_layout.addWidget(create_button)
#             button_layout.addWidget(update_button)
#             button_layout.addWidget(delete_button)
#
#             todo_layout.addLayout(button_layout)
#
#             invoice_button.clicked.connect(self.add_invoice)
#             create_button.clicked.connect(self.open_add_window)
#             update_button.clicked.connect(self.update_data)
#             delete_button.clicked.connect(self.delete_item)
#
#             self.todo_stack.addWidget(todo_widget)
#
#         # Add left menu and right todos to the main layout
#         main_layout.addWidget(menu_widget)
#         main_layout.addWidget(self.todo_stack)
#
#         # Set the central widget
#         self.setCentralWidget(central_widget)
#
#         # Show the main window
#         self.show()
#
#     def set_app_icon(self):
#         app_icon = QIcon("app_icons/401262_archlinux_icon.png")
#         self.setWindowIcon(app_icon)
#
#     def update_data(self):
#         if self.user is not None:
#             cetagories.UpdateItemDialog(self.db, self.todo_stack)
#         else:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def delete_item(self):
#         if self.user is not None:
#             # Get the current todo window index
#             current_index = self.todo_stack.currentIndex()
#
#             # Get the corresponding todo window widget
#             todo_widget = self.todo_stack.widget(current_index)
#
#             # Get the table widget from the todo window widget
#             table_widget = todo_widget.findChild(QTableWidget)
#
#             # Get the selected item
#             selected_items = table_widget.selectedItems()
#
#             # Check if an item is selected
#             if not selected_items:
#                 QMessageBox.warning(self, "Error", "No item selected.")
#                 return
#
#             # Get the row indexes of the selected items
#             selected_rows = set()
#             for item in selected_items:
#                 selected_rows.add(item.row())
#
#             # Display a confirmation dialog
#             confirmation = QMessageBox.question(
#                 self,
#                 "Confirmation",
#                 "Are you sure you want to delete the selected item(s)?",
#                 QMessageBox.Yes | QMessageBox.No,
#                 QMessageBox.No
#             )
#
#             if confirmation == QMessageBox.Yes:
#                 # Remove the selected item(s) from the table widget
#                 for row in sorted(selected_rows, reverse=True):
#                     item_id = table_widget.item(row, 0).text()
#                     self.delete_item_from_database(current_index, int(item_id))
#                     table_widget.removeRow(row)
#
#                 # Commit the changes to the database
#                 self.db.commit()
#
#         else:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def delete_item_from_database(self, index, item_id):
#         YourModel = None
#         if index == 0:
#             YourModel = Panel
#         if index == 1:
#             YourModel = Inverter
#         if index == 2:
#             YourModel = Frame
#         if index == 3:
#             YourModel = ACCable
#         if index == 4:
#             YourModel = DCCable
#         if index == 5:
#             YourModel = Customer
#         if index == 6:
#             YourModel = Battery
#         if index == 7:
#             YourModel = Accessories
#         if index == 8:
#             YourModel = QuotationItem
#         if index == 9:
#             YourModel = Quotation
#         try:
#             # Retrieve the item from the database using the item_id
#             item = self.db.query(YourModel).get(item_id)
#
#             if item is not None:
#                 # Delete the item from the database
#                 self.db.delete(item)
#                 self.db.commit()
#
#                 # Remove the item from the UI or update the UI accordingly
#
#                 QMessageBox.information(self, 'Success', 'Item deleted successfully.')
#             else:
#                 QMessageBox.warning(self, 'Error', 'Item not found.')
#
#         except Exception as e:
#             QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
#
#     def on_menu_item_clicked(self, index):
#         # Check if the clicked menu item is already selected
#         if index == self.todo_stack.currentIndex():
#             return
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(index)
#
#         # Find the existing table widget in the todo widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if table_widget is None:
#             # Create a new table widget if it doesn't exist
#             table_widget = QTableWidget(todo_widget)
#             todo_widget.layout().addWidget(table_widget)
#         else:
#             table_widget.clear()
#
#         if index == 0:
#             headers = ["#", "Product Name", "Brand", "Type", "Capacity", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Panel).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 1:
#             headers = ["#", "Product Name", "Brand", "Type", "Power Rating", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Inverter).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(item.product_name))
#                 table_widget.setItem(row, 2, QTableWidgetItem(item.brand))
#                 table_widget.setItem(row, 3, QTableWidgetItem(item.typ))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.power_rating)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(item.purchase_price))
#                 table_widget.setItem(row, 6, QTableWidgetItem(item.sell_price))
#
#         elif index == 2:
#             headers = ["#", "Product Name", "Brand", "Type", "Width", "Height", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Frame).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.width)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.height)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 7, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 3:
#             headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(ACCable).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 4:
#             headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(DCCable).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#         # elif index == 5:
#         #     headers = ["#", "Customer Name", "Company", "Phone Number", "Email", "City", "Address"]
#         #     db_data = self.db.query(Customer).all()
#         #
#         #     # Set the new headers
#         #     table_widget.setColumnCount(len(headers))
#         #     table_widget.setHorizontalHeaderLabels(headers)
#         #
#         #     # Add items to the table widget
#         #     table_widget.setRowCount(len(db_data))
#         #
#         #     for row, item in enumerate(db_data):
#         #         table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#         #         table_widget.setItem(row, 1, QTableWidgetItem(str(item.customer_name)))
#         #         table_widget.setItem(row, 2, QTableWidgetItem(str(item.company)))
#         #         table_widget.setItem(row, 3, QTableWidgetItem(str(item.phone_number)))
#         #         table_widget.setItem(row, 4, QTableWidgetItem(str(item.email)))
#         #         table_widget.setItem(row, 5, QTableWidgetItem(str(item.city)))
#         #         table_widget.setItem(row, 6, QTableWidgetItem(str(item.address)))
#
#         elif index == 5:
#             headers = ["#", "Product Name", "Brand", "Type", "Warranty", "Capacity", "Voltage", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Battery).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.warranty)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(item.voltage))
#                 table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))
#
#         elif index == 6:
#             headers = ["#", "Product Name", "Model", "Type", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Accessories).all()
#
#             # Set the new headers
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.model)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#         # elif index == 8:
#         #     headers = ["#", "Product Name", "Brand", "Type", "Quantity", "Sell Price", "Total Price"]
#         #     db_data = self.db.query(QuotationItem).all()
#         #
#         #     # Set the new headers
#         #     table_widget.setColumnCount(len(headers))
#         #     table_widget.setHorizontalHeaderLabels(headers)
#         #
#         #     # Add items to the table widget
#         #     table_widget.setRowCount(len(db_data))
#         #
#         #     for row, item in enumerate(db_data):
#         #         table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#         #         table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_name)))
#         #         table_widget.setItem(row, 2, QTableWidgetItem(str(item.brand)))
#         #         table_widget.setItem(row, 3, QTableWidgetItem(str(item.typ)))
#         #         table_widget.setItem(row, 4, QTableWidgetItem(str(item.quantity)))
#         #         table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#         #         table_widget.setItem(row, 6, QTableWidgetItem(str(item.total_price)))
#         #
#         # elif index == 9:
#         #     headers = ["#", "Customer Name", "Walk in Customer", "Date", "Grand Total"]
#         #     db_data = self.db.query(Quotation).all()
#         #
#         #     # Set the new headers
#         #     table_widget.setColumnCount(len(headers))
#         #     table_widget.setHorizontalHeaderLabels(headers)
#         #
#         #     # Add items to the table widget
#         #     table_widget.setRowCount(len(db_data))
#         #
#         #     for row, ite in enumerate(db_data):
#         #         table_widget.setItem(row, 0, QTableWidgetItem(str(ite.id)))
#         #         table_widget.setItem(row, 1, QTableWidgetItem(str(ite.customer_name)))
#         #         table_widget.setItem(row, 2, QTableWidgetItem(str(ite.walk_in_customer)))
#         #         table_widget.setItem(row, 3, QTableWidgetItem(str(ite.date)))
#         #         table_widget.setItem(row, 4, QTableWidgetItem(str(ite.grand_total)))
#
#         else:
#             return
#
#         # Resize the columns to fit the content
#         table_widget.resizeColumnsToContents()
#
#         # Set the current todo window index to match the clicked menu item
#         self.todo_stack.setCurrentIndex(index)
#
#     def add_customer(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         headers = ["#", "Customer Name", "Company", "Phone Number", "Email", "City", "Address"]
#         db_data = self.db.query(Customer).all()
#
#         # Set the new headers
#         table_widget.setColumnCount(len(headers))
#         table_widget.setHorizontalHeaderLabels(headers)
#
#         # Add items to the table widget
#         table_widget.setRowCount(len(db_data))
#
#         for row, item in enumerate(db_data):
#             table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#             table_widget.setItem(row, 1, QTableWidgetItem(str(item.customer_name)))
#             table_widget.setItem(row, 2, QTableWidgetItem(str(item.company)))
#             table_widget.setItem(row, 3, QTableWidgetItem(str(item.phone_number)))
#             table_widget.setItem(row, 4, QTableWidgetItem(str(item.email)))
#             table_widget.setItem(row, 5, QTableWidgetItem(str(item.city)))
#             table_widget.setItem(row, 6, QTableWidgetItem(str(item.address)))
#
#     def show_invoices(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         headers = ["#", "Invoice Code", "Product Name", "Brand", "Type", "Quantity", "Price", "Total"]
#         db_data = self.db.query(QuotationItem).all()
#
#         # Set the new headers
#         table_widget.setColumnCount(len(headers))
#         table_widget.setHorizontalHeaderLabels(headers)
#
#         # Add items to the table widget
#         table_widget.setRowCount(len(db_data))
#
#         for row, item in enumerate(db_data):
#             table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#             table_widget.setItem(row, 1, QTableWidgetItem(str(item.item)))
#             table_widget.setItem(row, 2, QTableWidgetItem(str(item.description)))
#             table_widget.setItem(row, 3, QTableWidgetItem(str(item.quantity)))
#             table_widget.setItem(row, 4, QTableWidgetItem(str(item.price)))
#             table_widget.setItem(row, 5, QTableWidgetItem(str(item.total)))
#
#     def add_invoice(self):
#         print('invoice')
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if self.user:
#             add_invoice_dialog = AddInvoiceDialog(self.db, self.user.id, table_widget)
#             add_invoice_dialog.exec_()
#
#         elif self.user is None:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#     def open_add_window(self):
#         current_index = self.todo_stack.currentIndex()
#         todo_widget = self.todo_stack.widget(current_index)
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         if self.user is None:
#             QMessageBox.warning(self, "Error", "Please login first.")
#
#         elif current_index == 0:  # Panel
#             add_panel_dialog = AddPanelDialog(self.db, self.user.id, table_widget)
#             add_panel_dialog.exec_()
#
#         elif current_index == 1:  # Inverter
#             add_inverter_dialog = AddInverterDialog(self.db, self.user.id, table_widget)
#             add_inverter_dialog.exec_()
#
#         elif current_index == 2:  # Frame
#             add_frame_dialog = AddFrameDialog(self.db, self.user.id, table_widget)
#             add_frame_dialog.exec_()
#
#         elif current_index == 3:  # AC-Cable
#             add_ac_cable_dialog = AddACCableDialog(self.db, self.user.id, table_widget)
#             add_ac_cable_dialog.exec_()
#
#         elif current_index == 4:  # DC-Cable
#             add_dc_cable_dialog = AddDCCableDialog(self.db, self.user.id, table_widget)
#             add_dc_cable_dialog.exec_()
#
#         # elif current_index == 5:  # Labor
#         #     add_labor_dialog = AddLaborDialog(self.db, self.user.id, table_widget)
#         #     add_labor_dialog.exec_()
#
#         elif current_index == 5:  # Customer
#             add_customer_dialog = AddCustomerDialog(self.db, self.user.id, table_widget)
#             add_customer_dialog.exec_()
#
#         elif current_index == 6:  # Battery
#             add_battery_dialog = AddBatteryDialog(self.db, self.user.id, table_widget)
#             add_battery_dialog.exec_()
#
#         elif current_index == 7:  # Accessories
#             add_accessories_dialog = AddAccessoriesDialog(self.db, self.user.id, table_widget)
#             add_accessories_dialog.exec_()
#
#         elif current_index == 8:  # QuotationItem
#             add_quotation_item_dialog = AddQuotationItemDialog(self.db, self.user.id, table_widget)
#             add_quotation_item_dialog.exec_()
#
#         elif current_index == 9:  # Quotation
#             add_quotation_dialog = AddQuotationDialog(self.db, self.user.id, table_widget)
#             add_quotation_dialog.exec_()
#
#     def handle_added_item(self, item_data):
#         # Get the current todo window index
#         current_index = self.todo_stack.currentIndex()
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(current_index)
#
#         # Get the table widget from the todo window widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         # Validate the item data
#         if all(item_data.values()):
#             # Add the item to the table widget
#             row_count = table_widget.rowCount()
#             table_widget.insertRow(row_count)
#
#             for column, data in enumerate(item_data.values()):
#                 item = QTableWidgetItem(data)
#                 item.setTextAlignment(Qt.AlignCenter)
#                 table_widget.setItem(row_count, column, item)
#         else:
#             # Show an error message if any field is empty
#             QMessageBox.warning(self, "Error", "All fields are required.")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow('token')
#     sys.exit(app.exec_())

# ==========3=============
# from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
#     QComboBox, QLineEdit, QTextEdit, QAction, QTableWidget, QTableWidgetItem, QHeaderView
# import sys
# from PySide2.QtCore import Qt
# from PySide2.QtGui import QIcon
# from models.database_config import get_db
# from models.database_models import User, Panel, Inverter, ACCable, DCCable, Frame, Labor, Quotation, \
#     Battery, \
#     Accessories, QuotationItem, Expanse, Customer
#
# from models.database_models import Panel
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, token):
#         super().__init__()
#         self.token = token
#         self.db = next(get_db())
#         self.user = self.db.query(User).filter(User.token == self.token).first()
#
#         self.setWindowTitle("System Inventory")
#         self.setFixedSize(self.screen().size())
#         self.setMinimumSize(900, 600)
#
#         # Create the main layout
#         main_layout = QVBoxLayout()
#
#         # Create menu bar
#         menu_bar = self.menuBar()
#         file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
#         file_save.setShortcut('Ctrl+S')
#         file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
#         file_exit.setShortcut('Ctrl+Q')
#         file_exit.triggered.connect(self.close)
#
#         action_edit = QAction(QIcon('app_icons/save.svg'), "Edit", self)
#         action_edit.setShortcut('Ctrl+E')
#         action_help = QAction(QIcon('app_icons/save.svg'), "Help", self)
#         action_help.setShortcut('Ctrl+H')
#
#         # Add File menu
#         file_menu = menu_bar.addMenu("File")
#         file_menu.addAction(file_save)
#         file_menu.addAction(file_exit)
#
#         view_menu = menu_bar.addMenu("View")
#         edit_menu = menu_bar.addMenu("Edit")
#         help_menu = menu_bar.addMenu("Help")
#
#         # Create the header part
#         header_layout = QHBoxLayout()
#         self.body_label = QLabel('')
#         self.body_combo = QComboBox()
#         self.body_combo.addItem('')
#         self.body_combo.addItem('Inverter')
#         self.body_combo.addItem('Panel')
#         self.body_combo.addItem('Frame')
#         self.body_combo.addItem('AC Cable')
#         self.body_combo.addItem('DC Cable')
#         self.body_combo.addItem('Battery')
#         self.body_combo.addItem('Accessories')
#
#         customer_button = QPushButton('Customer')
#         invoices_button = QPushButton('Invoices')
#         user_button = QPushButton('User')
#         header_layout.addWidget(self.body_combo)
#         header_layout.addWidget(customer_button)
#         header_layout.addWidget(invoices_button)
#         header_layout.addStretch()
#         header_layout.addWidget(user_button)
#
#         # Create the bottom part
#         bottom_layout = QHBoxLayout()
#         create_invoice_button = QPushButton('Create Invoice')
#         create_button = QPushButton('Create')
#         update_button = QPushButton('Update')
#         delete_button = QPushButton('Delete')
#
#         bottom_layout.addWidget(create_button)
#         bottom_layout.addWidget(update_button)
#         bottom_layout.addWidget(delete_button)
#         bottom_layout.addStretch()
#         bottom_layout.addWidget(create_invoice_button)
#
#         # Add the header, body, and bottom layouts to the main layout
#         main_layout.addLayout(header_layout)
#         main_layout.addWidget(self.body_label)
#         main_layout.addLayout(bottom_layout)
#
#         # Create a central widget and set the main layout
#         central_widget = QWidget()
#         central_widget.setLayout(main_layout)
#         self.setCentralWidget(central_widget)
#
#         # Connect signals to slots
#         self.body_combo.currentIndexChanged.connect(self.show_data)
#         customer_button.clicked.connect(self.show_customers)
#         invoices_button.clicked.connect(self.show_invoices)
#         create_invoice_button.clicked.connect(self.create_invoice)
#         create_button.clicked.connect(self.create_action)
#         update_button.clicked.connect(self.update_action)
#         delete_button.clicked.connect(self.delete_action)
#
#     def show_data(self, index):
#         item = self.body_combo.currentText()
#
#         if index == 0:
#             pass
#
#         elif item == 'Panel':
#             headers = ["Product Name", "Brand", "Type", "Capacity", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Panel).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif item == 'Inverter':
#             headers = ["Product Name", "Brand", "Type", "Power Rating", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Inverter).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.power_rating)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif item == 'Frame':
#             headers = ["Product Name", "Brand", "Type", "Width", "Height", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Frame).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.width)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.height)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif item == 'AC Cable':
#             headers = ["Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(ACCable).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif item == 'DC Cable':
#             headers = ["#", "Product Name", "Brand", "Type", "Size", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(DCCable).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.size)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif item == 'Battery':
#             headers = ["#", "Product Name", "Brand", "Type", "Warranty", "Capacity", "Voltage", "Purchase Price",
#                        "Sell Price"]
#             db_data = self.db.query(Battery).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.brand)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.warranty)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.capacity)))
#                 table_widget.setItem(row, 5, QTableWidgetItem(item.voltage))
#                 table_widget.setItem(row, 6, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 7, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         elif index == 'Accessories':
#             headers = ["#", "Product Name", "Model", "Type", "Purchase Price", "Sell Price"]
#             db_data = self.db.query(Accessories).all()
#
#             # Create the table widget
#             table_widget = QTableWidget()
#             table_widget.setColumnCount(len(headers))
#             table_widget.setHorizontalHeaderLabels(headers)
#
#             # Add items to the table widget
#             table_widget.setRowCount(len(db_data))
#
#             for row, item in enumerate(db_data):
#                 # table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
#                 table_widget.setItem(row, 0, QTableWidgetItem(str(item.product_name)))
#                 table_widget.setItem(row, 1, QTableWidgetItem(str(item.model)))
#                 table_widget.setItem(row, 2, QTableWidgetItem(str(item.typ)))
#                 table_widget.setItem(row, 3, QTableWidgetItem(str(item.purchase_price)))
#                 table_widget.setItem(row, 4, QTableWidgetItem(str(item.sell_price)))
#
#             # Set the header section resize mode to Stretch
#             header = table_widget.horizontalHeader()
#             header.setSectionResizeMode(QHeaderView.Stretch)
#
#             # Replace the body_label with the table_widget
#             main_layout = self.centralWidget().layout()
#             main_layout.replaceWidget(self.body_label, table_widget)
#             self.body_label = table_widget
#
#         else:
#             return
#
#     def show_customers(self):
#         pass
#
#     def show_invoices(self):
#         pass
#
#     def create_invoice(self):
#         # Perform the create_ action based on the current window
#         pass
#
#     def create_action(self):
#         # Perform the create_ action based on the current window
#         pass
#
#     def update_action(self):
#         # Perform the update action based on the current window
#         pass
#
#     def delete_action(self):
#         # Perform the delete action based on the current window
#         pass
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow('token')
#     window.show()
#     sys.exit(app.exec_())
#
