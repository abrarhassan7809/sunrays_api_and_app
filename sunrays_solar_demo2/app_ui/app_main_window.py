# import sys
# from functools import partial
#
# from PySide2.QtGui import QIcon
# from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
#     QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox
# from PySide2.QtCore import Qt, Signal, QSize
#
# HORIZONTAL_HEADERS = ["Header", "Header", "Header", "Header", "Header", "Header", "Header"]
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle("Main Window")
#         self.setFixedSize(self.screen().size())
#         self.setMinimumSize(900, 600)
#
#         # Create actions
#         action_panel = QAction("Panel", self)
#         action_inverter = QAction("Inverter", self)
#         action_frame = QAction("Frame", self)
#         action_coil = QAction("Coil", self)
#         action_labor_installation = QAction("Labor Installation", self)
#         action_batteries = QAction("Batteries", self)
#         action_accessories = QAction("Accessories", self)
#         action_quotation = QAction("Quotation", self)
#         # action_quotation_item = QAction("Quotation Item", self)
#
#         file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
#         file_save.setShortcut('Ctrl+S')
#         file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
#         file_exit.setShortcut('Ctrl+Q')
#         file_exit.triggered.connect(self.close)
#
#         action_edit = QAction("Edit", self)
#         action_help = QAction("Help", self)
#
#         # Create menu bar
#         menu_bar = self.menuBar()
#         self.setIcon()
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
#         # Add menu items to the left menu
#         menu_items = [
#             ("", "app_icons/icons8-solar-panel-40.png"),
#             ("", "app_icons/icons8-inverter-65.png"),
#             ("", "app_icons/icons8-frame-67.png"),
#             ("", "app_icons/icons8-coil-48.png"),
#             ("", "app_icons/icons8-labor-64.png"),
#             ("", "app_icons/icons8-battery-64.png"),
#             ("", "app_icons/icons8-cart-48.png"),
#             ("", "app_icons/icons8-quotation-64.png"),
#         ]
#
#         # Create a stacked widget for todo windows
#         self.todo_stack = QStackedWidget()
#
#         for index, (text, icon_path) in enumerate(menu_items):
#             button = QPushButton(text)
#             button.setIcon(QIcon(icon_path))
#             button.setIconSize(QSize(50, 50))
#             button.setStyleSheet("padding: 10px 25px 10px 25px;")
#             button.clicked.connect(partial(self.on_menu_item_clicked, index, icon_path))
#             menu_layout.addWidget(button)
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
#             create_button = QPushButton("Create")
#             update_button = QPushButton("Update")
#             delete_button = QPushButton("Delete")
#             button_layout.addWidget(create_button)
#             button_layout.addWidget(update_button)
#             button_layout.addWidget(delete_button)
#             todo_layout.addLayout(button_layout)
#
#             # Connect the "Create" button to open the add window
#             create_button.clicked.connect(self.open_add_window)
#
#             # Connect the "Update" button to open the update window
#             update_button.clicked.connect(self.open_update_window)
#
#             # Connect the "Delete" button to delete the selected item
#             delete_button.clicked.connect(self.delete_item)
#
#             # Add the todo window widget to the stacked widget
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
#     def setIcon(self):
#         appIcon = QIcon("401262_archlinux_icon.png")
#         self.setWindowIcon(appIcon)
#
#     def delete_item(self):
#         # Get the current todo window index
#         current_index = self.todo_stack.currentIndex()
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(current_index)
#
#         # Get the table widget from the todo window widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         # Get the selected item
#         selected_items = table_widget.selectedItems()
#
#         # Check if an item is selected
#         if not selected_items:
#             QMessageBox.warning(self, "Error", "No item selected.")
#             return
#
#         # Get the row indexes of the selected items
#         selected_rows = set()
#         for item in selected_items:
#             selected_rows.add(item.row())
#
#         # Display a confirmation dialog
#         confirmation = QMessageBox.question(
#             self,
#             "Confirmation",
#             "Are you sure you want to delete the selected item(s)?",
#             QMessageBox.Yes | QMessageBox.No,
#             QMessageBox.No
#         )
#
#         if confirmation == QMessageBox.Yes:
#             # Remove the selected item(s) from the table widget
#             for row in sorted(selected_rows, reverse=True):
#                 table_widget.removeRow(row)
#
#     def on_menu_item_clicked(self, index, selected_path):
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
#         headers = []
#         items = []
#
#         # Update the headers and items based on the selected menu item
#         if selected_path == "app_icons/icons8-solar-panel-40.png":
#             headers = ["Panel", "Name", "Brand", "Capacity", "Efficiency", "Dimensions", "Weight"]
#             items = []
#         elif selected_path == "app_icons/icons8-inverter-65.png":
#             headers = ["Manufacturer", "Model", "Serial Number", "Power Rating", "Input Voltage", "Output Voltage", "Efficiency", "Communication Protocol", "Warranty", "Installation Date"]
#             items = []
#         elif selected_path == "app_icons/icons8-frame-67.png":
#             headers = ["Material", "Weight", "Width", "Height", "Thickness", "Manufacturer", ""]
#             items = []
#         elif selected_path == "app_icons/icons8-coil-48.png":
#             headers = ["Material", "Gauge", "Width", "Weight", "Manufacturer", "Price"]
#             items = []
#         elif selected_path == "app_icons/icons8-battery-64.png":
#             headers = ["Brand", "Capacity", "Voltage", "Chemistry", "Weight", "Price"]
#             items = []
#         elif selected_path == "app_icons/icons8-labor-64.png":
#             headers = ["Labor Name", "Start Date", "End Date", "Labor Cost", "Description"]
#             items = []
#         elif selected_path == "app_icons/icons8-cart-48.png":
#             headers = ["Labor Name", "Name", "Description"]
#             items = []
#         elif selected_path == "app_icons/icons8-quotation-64.png":
#             headers = ["Date", "Product Name", "Quantity", "Price",  "Total Amount"]
#             items = []
#         else:
#             return
#
#         # Set the new headers
#         table_widget.setColumnCount(len(headers))
#         table_widget.setHorizontalHeaderLabels(headers)
#
#         # Add items to the table widget
#         table_widget.setRowCount(len(items))
#         for row, item in enumerate(items):
#             for column, data in enumerate(item):
#                 table_widget.setItem(row, column, QTableWidgetItem(data))
#
#         # Resize the columns to fit the content
#         table_widget.resizeColumnsToContents()
#
#         # Set the current todo window index to match the clicked menu item
#         self.todo_stack.setCurrentIndex(index)
#
#     def open_add_window(self):
#         # Create a new add window
#         add_window = AddWindow()
#         add_window.added.connect(self.handle_added_item)
#         add_window.exec_()
#
#     def open_update_window(self):
#         # Get the current todo window index
#         current_index = self.todo_stack.currentIndex()
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(current_index)
#
#         # Get the table widget from the todo window widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         # Get the selected item
#         selected_item = table_widget.selectedItems()
#
#         # Check if an item is selected
#         if not selected_item:
#             QMessageBox.warning(self, "Error", "No item selected.")
#             return
#
#         # Get the row index of the selected item
#         row = selected_item[0].row()
#
#         # Get the item data from the selected row
#         item_data = {}
#         for column in range(table_widget.columnCount()):
#             header = table_widget.horizontalHeaderItem(column).text()
#             item_data[header] = table_widget.item(row, column).text()
#
#         # Create a new update window
#         update_window = UpdateWindow(item_data)
#         update_window.updated.connect(self.handle_updated_item)
#         update_window.exec_()
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
#     def handle_updated_item(self, item_data):
#         # Get the current todo window index
#         current_index = self.todo_stack.currentIndex()
#
#         # Get the corresponding todo window widget
#         todo_widget = self.todo_stack.widget(current_index)
#
#         # Get the table widget from the todo window widget
#         table_widget = todo_widget.findChild(QTableWidget)
#
#         # Get the selected item
#         selected_item = table_widget.selectedItems()
#
#         # Check if an item is selected
#         if not selected_item:
#             QMessageBox.warning(self, "Error", "No item selected.")
#             return
#
#         # Get the row index of the selected item
#         row = selected_item[0].row()
#
#         # Update the item data in the table widget
#         for column, data in enumerate(item_data.values()):
#             item = QTableWidgetItem(data)
#             item.setTextAlignment(Qt.AlignCenter)
#             table_widget.setItem(row, column, item)
#
#
# class AddWindow(QDialog):
#     added = Signal(dict)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Add Window")
#
#         # Create the main layout for the add window
#         main_layout = QVBoxLayout()
#         self.setLayout(main_layout)
#
#         # Create labels and input fields
#         labels = ["Panel", "Name", "Brand", "Capacity", "Efficiency", "Dimensions", "Weight"]
#         self.input_fields = {}
#
#         for label in labels:
#             label_widget = QLabel(label)
#             input_field = QLineEdit()
#             self.input_fields[label] = input_field
#
#             main_layout.addWidget(label_widget)
#             main_layout.addWidget(input_field)
#
#         # Create the "Add" button
#         add_button = QPushButton("Add")
#         add_button.clicked.connect(self.add_item)
#         main_layout.addWidget(add_button)
#
#     def add_item(self):
#         item_data = {label: field.text() for label, field in self.input_fields.items()}
#         self.added.emit(item_data)
#         self.close()
#
#
# class UpdateWindow(QDialog):
#     updated = Signal(dict)
#
#     def __init__(self, item_data):
#         super().__init__()
#         self.setWindowTitle("Update Window")
#
#         # Create the main layout for the update window
#         main_layout = QVBoxLayout()
#         self.setLayout(main_layout)
#
#         # Create labels and input fields
#         self.input_fields = {}
#
#         for label, value in item_data.items():
#             label_widget = QLabel(label)
#             input_field = QLineEdit()
#             input_field.setText(value)
#             self.input_fields[label] = input_field
#
#             main_layout.addWidget(label_widget)
#             main_layout.addWidget(input_field)
#
#         # Create the "Update" button
#         update_button = QPushButton("Update")
#         update_button.clicked.connect(self.update_item)
#         main_layout.addWidget(update_button)
#
#     def update_item(self):
#         item_data = {label: field.text() for label, field in self.input_fields.items()}
#         self.updated.emit(item_data)
#         self.close()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())

# =============2=============
import sys
from functools import partial

import requests
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, \
    QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox
from PySide2.QtCore import Qt, Signal, QSize

HORIZONTAL_HEADERS = ["Header", "Header", "Header", "Header", "Header", "Header", "Header"]


class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        print(token)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Window")
        self.setFixedSize(self.screen().size())
        self.setMinimumSize(900, 600)

        # Create actions
        action_panel = QAction("Panel", self)
        action_inverter = QAction("Inverter", self)
        action_frame = QAction("Frame", self)
        action_coil = QAction("Coil", self)
        action_labor_installation = QAction("Labor Installation", self)
        action_batteries = QAction("Batteries", self)
        action_accessories = QAction("Accessories", self)
        action_quotation = QAction("Quotation", self)
        # action_quotation_item = QAction("Quotation Item", self)

        file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
        file_save.setShortcut('Ctrl+S')
        file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
        file_exit.setShortcut('Ctrl+Q')
        file_exit.triggered.connect(self.close)

        action_edit = QAction("Edit", self)
        action_help = QAction("Help", self)

        # Create menu bar
        menu_bar = self.menuBar()
        self.setIcon()

        # Add File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(file_save)
        file_menu.addAction(file_exit)

        view_menu = menu_bar.addMenu("View")
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

        # Create the central widget
        central_widget = QWidget()

        # Create main layout for the central widget
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create layout for the left menu
        menu_layout = QVBoxLayout()
        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)

        # Add menu items to the left menu
        menu_items = [
            ("", "app_icons/icons8-solar-panel-40.png"),
            ("", "app_icons/icons8-inverter-65.png"),
            ("", "app_icons/icons8-frame-67.png"),
            ("", "app_icons/icons8-coil-48.png"),
            ("", "app_icons/icons8-labor-64.png"),
            ("", "app_icons/icons8-battery-64.png"),
            ("", "app_icons/icons8-cart-48.png"),
            ("", "app_icons/icons8-quotation-64.png"),
        ]

        # Create a stacked widget for todo windows
        self.todo_stack = QStackedWidget()

        for index, (text, icon_path) in enumerate(menu_items):
            button = QPushButton(text)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(50, 50))
            button.setStyleSheet("padding: 10px 25px 10px 25px;")
            button.clicked.connect(partial(self.on_menu_item_clicked, index, icon_path))
            menu_layout.addWidget(button)
            # Create a todo window widget for each menu item
            todo_widget = QWidget()
            todo_layout = QVBoxLayout()
            todo_widget.setLayout(todo_layout)

            # Add table widget to the todo window widget
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(HORIZONTAL_HEADERS))
            table_widget.setHorizontalHeaderLabels(HORIZONTAL_HEADERS)
            table_widget.verticalHeader().setVisible(False)
            table_widget.horizontalHeader().setStretchLastSection(True)
            todo_layout.addWidget(table_widget)

            # Create button layout
            button_layout = QHBoxLayout()
            create_button = QPushButton("Create")
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")
            button_layout.addWidget(create_button)
            button_layout.addWidget(update_button)
            button_layout.addWidget(delete_button)
            todo_layout.addLayout(button_layout)

            # Connect the "Create" button to open the add window
            create_button.clicked.connect(self.open_add_window)

            # Connect the "Update" button to open the update window
            update_button.clicked.connect(self.open_update_window)

            # Connect the "Delete" button to delete the selected item
            delete_button.clicked.connect(self.delete_item)

            # Add the todo window widget to the stacked widget
            self.todo_stack.addWidget(todo_widget)

        # Add left menu and right todos to the main layout
        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.todo_stack)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Show the main window
        self.show()

    def setIcon(self):
        appIcon = QIcon("401262_archlinux_icon.png")
        self.setWindowIcon(appIcon)

    def delete_item(self):
        # Get the current todo window index
        current_index = self.todo_stack.currentIndex()

        # Get the corresponding todo window widget
        todo_widget = self.todo_stack.widget(current_index)

        # Get the table widget from the todo window widget
        table_widget = todo_widget.findChild(QTableWidget)

        # Get the selected item
        selected_items = table_widget.selectedItems()

        # Check if an item is selected
        if not selected_items:
            QMessageBox.warning(self, "Error", "No item selected.")
            return

        # Get the row indexes of the selected items
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())

        # Display a confirmation dialog
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected item(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            # Remove the selected item(s) from the table widget
            for row in sorted(selected_rows, reverse=True):
                table_widget.removeRow(row)

    def on_menu_item_clicked(self, index, selected_path):
        # Check if the clicked menu item is already selected
        if index == self.todo_stack.currentIndex():
            return

        # Get the corresponding todo window widget
        todo_widget = self.todo_stack.widget(index)

        # Find the existing table widget in the todo widget
        table_widget = todo_widget.findChild(QTableWidget)

        if table_widget is None:
            # Create a new table widget if it doesn't exist
            table_widget = QTableWidget(todo_widget)
            todo_widget.layout().addWidget(table_widget)
        else:
            table_widget.clear()

        payload = {
            'name': 'name'
        }
        # Update the headers and items based on the selected menu item
        if selected_path == "app_icons/icons8-solar-panel-40.png":
            headers = ["Panel", "Name", "Brand", "Capacity", "Efficiency", "Dimensions", "Weight"]

            try:
                # Make an HTTP POST request to the API endpoint
                response = requests.post("http://0.0.0.0:8000/user/login/", json=payload)

                if response.status_code == 200:
                    user_data = response.json()
                    print("User Token:", user_data["token"])
                    QMessageBox.information(self, "Login Successful", "User exists!")
                    self.accept()  # Close the login window and proceed
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid email or password")

            except requests.exceptions.RequestException as e:
                QMessageBox.warning(self, "API Error", f"An error occurred: {str(e)}")

        elif selected_path == "app_icons/icons8-inverter-65.png":
            headers = ["Manufacturer", "Model", "Serial Number", "Power Rating", "Input Voltage", "Output Voltage", "Efficiency", "Communication Protocol", "Warranty", "Installation Date"]
            items = []
        elif selected_path == "app_icons/icons8-frame-67.png":
            headers = ["Material", "Weight", "Width", "Height", "Thickness", "Manufacturer", ""]
            items = []
        elif selected_path == "app_icons/icons8-coil-48.png":
            headers = ["Material", "Gauge", "Width", "Weight", "Manufacturer", "Price"]
            items = []
        elif selected_path == "app_icons/icons8-battery-64.png":
            headers = ["Brand", "Capacity", "Voltage", "Chemistry", "Weight", "Price"]
            items = []
        elif selected_path == "app_icons/icons8-labor-64.png":
            headers = ["Labor Name", "Start Date", "End Date", "Labor Cost", "Description"]
            items = []
        elif selected_path == "app_icons/icons8-cart-48.png":
            headers = ["Labor Name", "Name", "Description"]
            items = []
        elif selected_path == "app_icons/icons8-quotation-64.png":
            headers = ["Date", "Product Name", "Quantity", "Price",  "Total Amount"]
            items = []
        else:
            return

        # Set the new headers
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        # Add items to the table widget
        table_widget.setRowCount(len(items))
        for row, item in enumerate(items):
            for column, data in enumerate(item):
                table_widget.setItem(row, column, QTableWidgetItem(data))

        # Resize the columns to fit the content
        table_widget.resizeColumnsToContents()

        # Set the current todo window index to match the clicked menu item
        self.todo_stack.setCurrentIndex(index)

    def open_add_window(self):
        # Create a new add window
        add_window = AddWindow()
        add_window.added.connect(self.handle_added_item)
        add_window.exec_()

    def open_update_window(self):
        # Get the current todo window index
        current_index = self.todo_stack.currentIndex()

        # Get the corresponding todo window widget
        todo_widget = self.todo_stack.widget(current_index)

        # Get the table widget from the todo window widget
        table_widget = todo_widget.findChild(QTableWidget)

        # Get the selected item
        selected_item = table_widget.selectedItems()

        # Check if an item is selected
        if not selected_item:
            QMessageBox.warning(self, "Error", "No item selected.")
            return

        # Get the row index of the selected item
        row = selected_item[0].row()

        # Get the item data from the selected row
        item_data = {}
        for column in range(table_widget.columnCount()):
            header = table_widget.horizontalHeaderItem(column).text()
            item_data[header] = table_widget.item(row, column).text()

        # Create a new update window
        update_window = UpdateWindow(item_data)
        update_window.updated.connect(self.handle_updated_item)
        update_window.exec_()

    def handle_added_item(self, item_data):
        # Get the current todo window index
        current_index = self.todo_stack.currentIndex()

        # Get the corresponding todo window widget
        todo_widget = self.todo_stack.widget(current_index)

        # Get the table widget from the todo window widget
        table_widget = todo_widget.findChild(QTableWidget)

        # Validate the item data
        if all(item_data.values()):
            # Add the item to the table widget
            row_count = table_widget.rowCount()
            table_widget.insertRow(row_count)

            for column, data in enumerate(item_data.values()):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row_count, column, item)
        else:
            # Show an error message if any field is empty
            QMessageBox.warning(self, "Error", "All fields are required.")

    def handle_updated_item(self, item_data):
        # Get the current todo window index
        current_index = self.todo_stack.currentIndex()

        # Get the corresponding todo window widget
        todo_widget = self.todo_stack.widget(current_index)

        # Get the table widget from the todo window widget
        table_widget = todo_widget.findChild(QTableWidget)

        # Get the selected item
        selected_item = table_widget.selectedItems()

        # Check if an item is selected
        if not selected_item:
            QMessageBox.warning(self, "Error", "No item selected.")
            return

        # Get the row index of the selected item
        row = selected_item[0].row()

        # Update the item data in the table widget
        for column, data in enumerate(item_data.values()):
            item = QTableWidgetItem(data)
            item.setTextAlignment(Qt.AlignCenter)
            table_widget.setItem(row, column, item)


class AddWindow(QDialog):
    added = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Window")

        # Create the main layout for the add window
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create labels and input fields
        labels = ["Panel", "Name", "Brand", "Capacity", "Efficiency", "Dimensions", "Weight"]
        self.input_fields = {}

        for label in labels:
            label_widget = QLabel(label)
            input_field = QLineEdit()
            self.input_fields[label] = input_field

            main_layout.addWidget(label_widget)
            main_layout.addWidget(input_field)

        # Create the "Add" button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_item)
        main_layout.addWidget(add_button)

    def add_item(self):
        item_data = {label: field.text() for label, field in self.input_fields.items()}
        self.added.emit(item_data)
        self.close()


class UpdateWindow(QDialog):
    updated = Signal(dict)

    def __init__(self, item_data):
        super().__init__()
        self.setWindowTitle("Update Window")

        # Create the main layout for the update window
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create labels and input fields
        self.input_fields = {}

        for label, value in item_data.items():
            label_widget = QLabel(label)
            input_field = QLineEdit()
            input_field.setText(value)
            self.input_fields[label] = input_field

            main_layout.addWidget(label_widget)
            main_layout.addWidget(input_field)

        # Create the "Update" button
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_item)
        main_layout.addWidget(update_button)

    def update_item(self):
        item_data = {label: field.text() for label, field in self.input_fields.items()}
        self.updated.emit(item_data)
        self.close()


if __name__ == "__main__":
    token = 'daasd232'
    app = QApplication(sys.argv)
    window = MainWindow(token)
    sys.exit(app.exec_())
