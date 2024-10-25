import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sampler")

        # Create a figure and 2x2 subplots
        self.figure, self.axes = plt.subplots(2, 2, figsize=(12, 10))
        self.canvas = FigureCanvas(self.figure)
        self.resize(1200, 1000)

        # Set the figure's background color
        self.figure.patch.set_facecolor('black')
        time=np.linspace(0, 2, 1000)
        f=10
        x_t = np.cos(2*np.pi*f*time)
        t_sampled = np.arange(0,2,1/8)
        x_t_sampled=np.cos(2*np.pi*f*t_sampled)
        self.stem_plot(t_sampled, x_t_sampled, 0, 0)
        self.plot(time, x_t,0,0)


        # Customize each subplot
        for i in range(2):
            for j in range(2):
                ax = self.axes[i, j]
                ax.set_facecolor('black')
                ax.set_xlabel('Time (s)', color='white')
                ax.set_ylabel('Amplitude', color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='white')
                border = Rectangle((0, 0), 1, 1, transform=ax.transAxes, color='white', linewidth=2, fill=False)
                ax.add_patch(border)

        # Add the canvas to the widget layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Adjust layout to prevent overlap
        self.figure.tight_layout()


    def plot(self,x_data, y_data,axis1,axis2):
        self.axes[axis1, axis2].plot(x_data, y_data,color='white')


    def stem_plot(self,x_data, y_data,axis1,axis2):
        self.axes[axis1, axis2].stem(x_data, y_data,basefmt='None')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Viewer()
    main_window.show()
    sys.exit(app.exec_())
