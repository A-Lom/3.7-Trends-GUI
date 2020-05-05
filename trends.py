import sys
import pycountry
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from pytrends.request import TrendReq
pytrend = TrendReq()


# Class that creates the GUI and contains most of it's features
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    # System that runs if the user wants interest over time
    def button_time_clicked(self):
        list = []
        text = self.input.text().split(",")
        for ref in text:
            list.append(ref.strip())
        # Checks to see if list of searches is empty
        if list == ['']:
            self.min_num_alert()
            return
        # Checks to see if there is an empty search
        if '' in list:
            self.missing_term_alert()
            return
        # Checks to see of there are more than 5 search terms
        if len(list) > 5:
            self.max_num_alert(len(list))
            return
        if self.multi_graph_check.isChecked():  # Bool Variable check
            pass
        else:
            plt.close('all')
        interest_over_time(list)

    # System that runs if the user wants interest by regeion
    def button_region_clicked(self):
        list = []
        text = self.input.text().split(",")
        for ref in text:
            list.append(ref.strip())
        # Checks to see if list of searches is empty
        if list == ['']:
            self.min_num_alert()
            return
        # Checks to see if there is an empty search
        if '' in list:
            self.missing_term_alert()
            return
        # Checks to see of there are more than 5 search terms
        if len(list) > 5:
            self.max_num_alert(len(list))
            return
        if self.multi_graph_check.isChecked():  # Bool Variable check
            pass
        else:
            plt.close('all')
        region = self.region.currentText()
        interest_by_region(list, region)

    # System to close all graphs
    def button_close_graph_clicked(self):
        plt.close('all')

    # System to close the program
    def button_close_clicked(self):
        sys.exit()

    # When people do things that will crash the program these events will
    # happen
    # Alert for when someone has an empty search term
    def missing_term_alert(self):
        alert = QMessageBox()
        alert.setWindowTitle("ALERT")
        alert.setText("You have inputed a blank search term.\nPlease add a "
                      "search term(s) and try again")
        alert.setIcon(QMessageBox.Critical)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()

    # Alet for if a user has more than 5 search terms due
    # to google only accepting a max of 5
    def max_num_alert(self, list_num):
        alert = QMessageBox()
        alert.setWindowTitle("ALERT")
        alert.setText(f"You have inputed more than 5 search terms."
                      f"\nPlease remove {list_num-5} "
                      f"search term(s) and try again")
        alert.setIcon(QMessageBox.Critical)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()

    # Alet for if a user has no search term provided
    def min_num_alert(self):
        alert = QMessageBox()
        alert.setWindowTitle("ALERT")
        alert.setText("You have inputed 0 search terms.\n"
                      "Please add a search term(s) and try again")
        alert.setIcon(QMessageBox.Critical)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()

    # Creates the main gui for the code. (AKA the skeleton of the code)
    def initUI(self):
        self.setGeometry(0, 0, 500, 500)
        self.setWindowTitle("Test")

        # Creates a info labele
        self.label = QLabel(self)
        self.label.setText("Seperate searches by a ,")
        self.label.resize(150, 30)
        self.label.move(150, 0)

        # Creates where you enter the search terms
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter Search Here")
        self.input.resize(150, 30)
        self.input.move(150, 40)

        # Creates the interest over time button
        self.button_time = QPushButton(self)
        self.button_time.setText("Search for interest over time")
        self.button_time.move(5, 80)
        self.button_time.resize(200, 30)
        self.button_time.clicked.connect(self.button_time_clicked)

        # Creates the interest BY region button
        self.button_region = QPushButton(self)
        self.button_region.setText("Search for interest by region")
        self.button_region.move(210, 80)
        self.button_region.resize(200, 30)
        self.button_region.clicked.connect(self.button_region_clicked)

        # Creates the close graphs button
        self.button_close_graph = QPushButton(self)
        self.button_close_graph.setText("Close Graphs")
        self.button_close_graph.move(105, 120)
        self.button_close_graph.clicked.connect(self.button_close_graph_clicked)

        # Creates the best button in the world. (The Close Button!!!)
        self.button_close = QPushButton(self)
        self.button_close.setText("Exit")
        self.button_close.move(210, 120)
        self.button_close.clicked.connect(self.button_close_clicked)

        # Creates the checkbox to allow you to keep graphs open
        self.multi_graph_check = QCheckBox(self)
        self.multi_graph_check.setText("Keep graphs open")
        self.multi_graph_check.resize(200, 30)
        self.multi_graph_check.move(150, 150)

        # Creates the dropdown box to seletect a region for interest by region
        self.region = QComboBox(self)
        self.region.resize(300, 30)
        self.region.addItem("Worldwide")
        for country in pycountry.countries:
            self.region.addItem(country.name)


# Displays the error alert box
def error():
        alert = QMessageBox()
        alert.setWindowTitle("ERROR")
        alert.setText("There has been an error")
        alert.setInformativeText("This could be due to there being "
                                 "no graph to be displayed")
        alert.setIcon(QMessageBox.Critical)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()


# The interest over time system
def interest_over_time(list):
    pytrend.build_payload(kw_list=list)
    interest_over_time = pytrend.interest_over_time()
    interest_over_time.plot(y=list, figsize=(15, 8), kind ='line')
    plt.show()


# The interest by regeion system
def interest_by_region(list, region):

    if region == "Worldwide":
        pytrend.build_payload(kw_list=list)
    else:
        region = pycountry.countries.get(name=region)
        print(region.alpha_2)
        pytrend.build_payload(kw_list=list, geo=region.alpha_2)
    try:
        interest_by_region = pytrend.interest_by_region(inc_low_vol=True, resolution='COUNTRY')
    except:
        error()
        return
    interest_by_region.plot(y=list, figsize=(15, 8), kind ='bar')
    plt.show()


# The brain of the main GUI
def gui():
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec())


# Starts the code
gui()
