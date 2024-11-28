# Create the GraphicsLayoutWidget and set minimum size
        self.window = pg.GraphicsLayoutWidget(show=True, title="Signal Studio")
        self.window.resize(1200, 900)
        self.window.setMinimumSize(500, 500)
        self.window.setBackground('#d3d3d3')  # Set background color for the entire window

        # Create plots
        self.signal_viewer = self.window.addPlot(title="<span style='color: black;'>Signal Viewer</span>")
        self.signal_viewer.setLabel('left', 'Amplitude', color='k')  # Set label color to black
        self.signal_viewer.setLabel('bottom', 'Time (s)', color='k')  # Set label color to black
        self.signal_viewer.getAxis('left').setPen('k')  # Set axis line color to black
        self.signal_viewer.getAxis('bottom').setPen('k')  # Set axis line color to black
        self.signal_viewer.setAspectLocked(False)
        self.signal_viewer.showGrid(x=True, y=True, alpha=0.4)

        self.reconstruction_viewer = self.window.addPlot(title="<span style='color: black;'>Reconstruction Viewer</span>")
        self.reconstruction_viewer.setLabel('left', 'Amplitude', color='k')
        self.reconstruction_viewer.setLabel('bottom', 'Time (s)', color='k')
        self.reconstruction_viewer.getAxis('left').setPen('k')
        self.reconstruction_viewer.getAxis('bottom').setPen('k')
        self.reconstruction_viewer.setAspectLocked(False)
        self.reconstruction_viewer.showGrid(x=True, y=True, alpha=0.4)
        self.reconstruction_viewer.addLegend()

        # Move to the next row
        self.window.nextRow()

        self.difference_viewer = self.window.addPlot(title="<span style='color: black;'>Difference Viewer</span>")
        self.difference_viewer.setLabel('left', 'Amplitude', color='k')
        self.difference_viewer.setLabel('bottom', 'Time (s)', color='k')
        self.difference_viewer.getAxis('left').setPen('k')
        self.difference_viewer.getAxis('bottom').setPen('k')
        self.difference_viewer.setAspectLocked(False)
        self.difference_viewer.showGrid(x=True, y=True, alpha=0.4)

        self.freq_viewer = self.window.addPlot(title="<span style='color: black;'>Frequency Viewer</span>")
        self.freq_viewer.setLabel('left', 'Magnitude', color='k')
        self.freq_viewer.setLabel('bottom', 'Frequency (Hz)', color='k')
        self.freq_viewer.getAxis('left').setPen('k')
        self.freq_viewer.getAxis('bottom').setPen('k')
        self.freq_viewer.setAspectLocked(False)
        self.freq_viewer.showGrid(x=True, y=True, alpha=0.4)

        horizontal_layout.addWidget(self.window)



dots = self.signal_viewer.plot(time, amplitude, pen=None, symbol='o', symbolBrush='r',
                                       symbolSize=7)  # Adjust size as needed

line = self.signal_viewer.plot([x, x], [0, y], pen=pg.mkPen('r'))


def plot(self, time, amplitude):
    # Plot the original signal if not already plotted
    if not hasattr(self, 'original_plot') or self.original_plot is None:
        self.original_plot = self.signal_viewer.plot(time, amplitude,
                                                     pen=pg.mkPen('#2196F3', width=4))  # Set line color and width
    else:
        self.original_plot.setData(time, amplitude)  # Update data if plot already exists