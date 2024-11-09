from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QMessageBox, QDesktopWidget
import sys

class Intro(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Multi-Chart Viewer")
        self.resize(400, 200)
        self.center()

        # Welcome Label
        self.welcome_label = QLabel("Welcome to the multi-chart viewer tool!\nSelect the data type and enter the ticker symbol below.", self)

        # ComboBox for data type selection
        self.data_type_label = QLabel("Select Data Type:", self)
        self.data_type_combo = QComboBox(self)
        self.data_type_combo.addItems(["Stocks", "Crypto", "Futures"])

        # Input for ticker symbol
        self.ticker_label = QLabel("Enter Ticker Symbol:", self)
        self.ticker_input = QLineEdit(self)

        # Button to fetch price
        self.fetch_button = QPushButton("Fetch Price", self)
        self.fetch_button.clicked.connect(self.fetch_price)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.data_type_label)
        layout.addWidget(self.data_type_combo)
        layout.addWidget(self.ticker_label)
        layout.addWidget(self.ticker_input)
        layout.addWidget(self.fetch_button)

        self.setLayout(layout)

        # Variables to hold data for later use
        self.ticker = None
        self.choice = None

    def center(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def fetch_price(self):
        # Get user inputs
        data_type = self.data_type_combo.currentText()
        self.ticker = self.ticker_input.text().upper()

        # Validate ticker input
        if not self.ticker:
            QMessageBox.warning(self, "Input Error", "Please enter a valid ticker symbol.")
            return

        # Determine data type choice
        self.choice = {"Stocks": "1", "Crypto": "2", "Futures": "3"}[data_type]
        self.close()

    def get_results(self):
        return self.ticker, self.choice

def run_gui():
    app = QApplication(sys.argv)
    window = Intro()
    window.show()
    app.exec_()
    return window.get_results()

if __name__ == "__main__":
    run_gui()
