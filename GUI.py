import sys
import fastf1
import pandas as pd
from config import *
from plots.py import *
from session.py import *
from wdc import *
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,QLineEdit, QLabel, QComboBox, QTableWidget,QTableWidgetItem)

fastf1.Cache.enable_cache("./cache")

class App(QWidget):
  def __init__(self):
      super().__init__()

      self.setWindowTitle("FastF1 Viewer")
      self.resize(600, 400)

      layout = QVBoxLayout()

      layout.addWidget(QLabel("Year"))
      self.year = QLineEdit("2024")
      layout.addWidget(self.year)

      layout.addWidget(QLabel("Grand Prix"))
      self.gp = QLineEdit("Bahrain")
      layout.addWidget(self.gp)

      layout.addWidget(QLabel("Session"))
      self.session = QComboBox()
      self.session.addItems(["R", "Q", "FP1", "FP2", "FP3"])
      layout.addWidget(self.session)

      self.button = QPushButton("Load Session")
      self.button.clicked.connect(self.load_session)
      layout.addWidget(self.button)

      self.table = QTableWidget()
      layout.addWidget(self.table)

      self.setLayout(layout)

  def load_session(self):

      year = int(self.year.text())
      gp = self.gp.text()
      session = self.session.currentText()

      s = fastf1.get_session(year, gp, session)
      s.load()

      laps = s.laps[['Driver', 'LapNumber', 'LapTime']]
      laps = laps.dropna().head(20)

      self.table.setRowCount(len(laps))
      self.table.setColumnCount(len(laps.columns))
      self.table.setHorizontalHeaderLabels(laps.columns)

      for i, row in laps.iterrows():
          for j, col in enumerate(laps.columns):
              self.table.setItem(
                  i,
                  j,
                  QTableWidgetItem(str(row[col]))
              )
            
app = QApplication(sys.argv)

window = F1App()
window.show()

sys.exit(app.exec())
