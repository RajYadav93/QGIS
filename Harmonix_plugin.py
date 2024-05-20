import os
import psycopg2
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QLabel

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'plugin_mod_dialog_base.ui'))


class QGIS_PlugDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(QGIS_PlugDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.error_label = QLabel()  # Assuming there's a QLabel widget for error messages

        # Connect signal from refresh button to slot function
        self.pushButton_3.clicked.connect(self.retrieve_projects_from_database)
        
        # Connect signal from project dropdown to slot function
        self.comboBox.currentIndexChanged.connect(self.handle_project_selection)

        # Database connection parameters
        self.db_params = {
            'host': 'localhost',
            'port': '5432',
            'database': 'postgres',
            'user': 'postgres',
            'password': 'Kumar@123'
        }

    def connect_to_database(self):
        try:
            # Establish connection to the database
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.display_error_message(str(e))

    def retrieve_projects_from_database(self):
        try:
            # Connect to the database
            self.connect_to_database()
            
            # Call a function to retrieve projects from the database
            projects = self.retrieve_projects()
            
            # Populate dropdown or list widget with retrieved projects
            self.populate_projects(projects)
        except Exception as e:
            self.display_error_message(str(e))
        finally:
            # Close the database connection
            self.close_database_connection()

    def retrieve_projects(self):
        # Execute SQL query to retrieve projects from the database
        self.cursor.execute("SELECT project_name FROM table_1")
        projects = self.cursor.fetchall()
        return [project[0] for project in projects]

    def populate_projects(self, projects):
        try:
            # Clear existing items
            self.comboBox.clear()
            # Populate dropdown or list widget with retrieved projects
            for project in projects:
                self.comboBox.addItem(project)
        except Exception as e:
            self.display_error_message(str(e))

    def handle_project_selection(self, index):
        try:
            selected_project = self.comboBox.itemText(index)
            # Call a function to process the selected project
            self.process_selected_project(selected_project)
        except Exception as e:
            self.display_error_message(str(e))

    def display_error_message(self, message):
        # Display error message to the user (e.g., in a label)
        self.error_label.setText(message)

    def close_database_connection(self):
        # Close cursor and connection to the database
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
