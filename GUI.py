import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
import sys


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle('Signal-Studio')
        self.resize(1400, 900)  # Set window size

        # Create a horizontal layout and set it as the main layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # Create the GraphicsLayoutWidget and set minimum size
        self.window = pg.GraphicsLayoutWidget(show=True, title="Signal Studio")
        self.window.resize(1200,900)
        self.window.setMinimumSize(500, 500)
        self.window.setBackground('k')  # Set background color for the entire window

        self.signal_viewer = self.window.addPlot(title="Signal Viewer")
        self.signal_viewer.setLabel('left', 'Amplitude')  # Set y-axis label
        self.signal_viewer.setLabel('bottom', 'Time (s)')  # Set x-axis label
        self.signal_viewer.setAspectLocked(False)
        self.signal_viewer.showGrid(x=True, y=True,alpha=0.4)

        self.reconstruction_viewer = self.window.addPlot(title="Reconstruction Viewer")
        self.reconstruction_viewer.setLabel('left', 'Amplitude')  # Set y-axis label
        self.reconstruction_viewer.setLabel('bottom', 'Time (s)')  # Set x-axis label
        self.reconstruction_viewer.setAspectLocked(False)
        self.reconstruction_viewer.showGrid(x=True, y=True,alpha=0.4)
        self.reconstruction_viewer.addLegend()

        # Move to the next row
        self.window.nextRow()

        self.difference_viewer = self.window.addPlot(title="Difference Viewer")
        self.difference_viewer.setLabel('left', 'Amplitude')  # Set y-axis label
        self.difference_viewer.setLabel('bottom', 'Time (s)')  # Set x-axis label
        self.difference_viewer.setAspectLocked(False)
        self.difference_viewer.showGrid(x=True, y=True,alpha=0.4)

        self.freq_viewer = self.window.addPlot(title="Frequency Viewer")
        self.freq_viewer.setLabel('left', 'Magnitude')  # Set y-axis label
        self.freq_viewer.setLabel('bottom', 'Frequency (Hz)')  # Set x-axis label
        self.freq_viewer.setAspectLocked(False)
        self.freq_viewer.showGrid(x=True, y=True,alpha=0.4)

        horizontal_layout.addWidget(self.window)
        ##########################################################
        #             PLease Marcii Write ur code below          #
        #                       at the end                       #
        #  DO NOT FORGET TO ADD YOR WIDGET TO HORIZONTAL LAYOUT  #
        #        horizontal_layout.addWidget(YOUR WIDGET)        #
        ##########################################################

                        ## Write your code here ##



        self.setLayout(horizontal_layout)
        self.show()

    def plot(self,time,amplitude):
        self.signal_viewer.clear()
        self.signal_viewer.plot(time,amplitude)
    def stem_plot(self):
        pass
    def update_plot(self):
        pass
    def get_difference_plot(self,plot1,plot2):
        pass
    def plot_frequency(self,frequency_plot):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GUI()
    main_window.show()
    sys.exit(app.exec_())
