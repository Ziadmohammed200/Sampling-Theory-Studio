import os
import numpy as np
import pandas as pd
import pyqtgraph as pg
import scipy
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QSlider, QComboBox, QLabel, \
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QLineEdit, QGroupBox, \
    QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import sys

from scipy.interpolate import interp1d


class Signal:
    def __init__(self,name, amplitude, time, signal_id, signal_type, frequency=None):
        self.name=name
        self.amplitude = amplitude
        self.time = time
        self.frequency = frequency
        self.signal_id = signal_id
        self.signal_type = signal_type


class SignalManager:
    def __init__(self, plot_callback):
        self.signals = []
        self.next_signal_id = 1  # Start signal ID from 1
        self.plot_callback = plot_callback
        self.snr = 40  # Default SNR value

    def upload_signal(self, parent):
        """Upload and load signal data from CSV files."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent, "Select Signal Files", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )

        if file_paths:
            for file_path in file_paths:
                try:
                    data = pd.read_csv(file_path)
                    if data.ndim == 1:
                        data = data.reshape(-1, 1)  # Ensure 2D array

                    if data.shape[1] < 2:
                        QMessageBox.warning(
                            parent, "Invalid Data",
                            f"CSV file '{file_path}' must contain at least two columns: time and amplitude."
                        )
                        continue

                    time = data.iloc[:, 0]   # Normalize time to start at zero
                    amplitude = data.iloc[:, 1]
                    frequency = data.iloc[:, 2]
                    amp=data.iloc[:, 3]



                    signal_name = os.path.splitext(os.path.basename(file_path))[0]


                    signal_id = self.next_signal_id
                    signal = Signal(name=signal_name,signal_id=signal_id, time=time, amplitude=amplitude, signal_type="UPLOADED")
                    parent.add_signal_to_table(signal_name,frequency[1],amp[1])

                    self.signals.append(signal)
                    self.next_signal_id += 1

                    # Automatically plot after uploading
                    self.plot_callback()

                except Exception as e:
                    QMessageBox.critical(parent, "Error", f"Failed to load signal '{file_path}':\n{e}")

    def add_signal_component(self, frequency, amplitude_value, parent):
        try:
            frequency = float(frequency)
            amplitude_value = float(amplitude_value)

            signal_id = self.next_signal_id

            if self.signals:
                length = len(self.signals[0].time)
                time = self.signals[0].time
            else:
                length = 1000
                time = np.linspace(0, length / 1000, length)  # Default time array with sampling rate 1000 Hz

            amplitude = amplitude_value * np.sin(2 * np.pi * frequency * time)
            signal_name= f"freq{str(frequency)} amp{str(amplitude_value)}"

            signal = Signal(name=signal_name,amplitude=amplitude, time=time, signal_id=signal_id, signal_type='sinusoidal', frequency=frequency)
            parent.add_signal_to_table(signal_name,str(frequency),str(amplitude_value))

            self.signals.append(signal)
            self.next_signal_id += 1

            # Automatically plot after adding a new signal component
            self.plot_callback()

        except ValueError:
            QMessageBox.warning(parent, "Invalid Input", "Please enter valid numbers for frequency and amplitude.")

    def set_snr(self, snr_value):
        """Set the SNR value for noise addition."""
        self.snr = snr_value

    def get_combined_signal_with_noise(self):
        """Combine all signals and add noise based on the current SNR value."""
        if not self.signals:
            return None, None

        time = self.signals[0].time
        combined_amplitude = np.zeros_like(time)

        for signal in self.signals:
            combined_amplitude += signal.amplitude

        # Signal power calculation
        signal_power = np.mean(combined_amplitude ** 2)

        # Noise power calculation with SNR in decibels (dB)
        noise_power = signal_power / (10 ** (self.snr / 10))
        noise = np.sqrt(noise_power) * np.random.normal(0, 1, len(combined_amplitude))

        # Combine signal with noise
        noisy_signal = combined_amplitude + noise


        return time, noisy_signal
    def remove_signal(self, signal_id):
        """Remove a signal by its ID."""
        self.signals = [signal for signal in self.signals if signal.signal_id != signal_id]


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle('Signal-Studio')
        self.resize(1400, 900)  # Set window size

        # Initialize SignalManager with plot_signals as the callback
        self.signal_manager = SignalManager(self.plot_signals)

        # Create a horizontal layout and set it as the main layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.data = []
        self.time = []
        self.amplitude = []
        self.sampled_amplitude = []
        self.sampling_frequency = 2

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

        # Create a vertical layout for the toolbar
        # Create a vertical layout for the toolbar
        # Initialize the main layout for the toolbar
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setContentsMargins(5, 5, 5, 5)

        # First Section: Upload Button in a grey square
        upload_box = QGroupBox()
        upload_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        upload_box.setStyleSheet("background-color: #d3d3d3; padding: 20px;")
        upload_layout = QVBoxLayout()
        upload_button = QPushButton("Upload")
        upload_button.setIcon(QIcon("path/to/icon.png"))
        upload_button.setStyleSheet("""
            font-size: 14px; 
            padding: 10px;
            background-color: #2196F3; 
            color: white; 
            border-radius: 5px;
        """)
        upload_layout.addWidget(upload_button)
        upload_box.setLayout(upload_layout)
        toolbar_layout.addWidget(upload_box)
        upload_button.clicked.connect(lambda: self.signal_manager.upload_signal(self))

        toolbar_layout.addStretch(1)

        # Second Section: Signal Info Table
        table_box = QGroupBox("Signal Info")
        table_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allows both horizontal and vertical expansion
        table_box.setStyleSheet("background-color: #d3d3d3; padding: 20px; font-size: 16px; font-weight: bold;")
        table_layout = QVBoxLayout()

        self.signal_info_table = QTableWidget()
        self.signal_info_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.signal_info_table.setColumnCount(3)
        self.signal_info_table.setHorizontalHeaderLabels(["Name", "Frequency", "Amplitude"])
        self.signal_info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.signal_info_table.setMinimumHeight(300)
        self.signal_info_table.setMaximumHeight(400)

        header = self.signal_info_table.horizontalHeader()
        header.setFont(QFont("Arial", 14, QFont.Bold))
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStyleSheet("""
            QHeaderView::section {
                padding: 8px;
                background-color: #e0e0e0;
                color: #333333;
                font-size: 14px;
                border: 1px solid #cccccc;
            }
        """)
        header.setMinimumHeight(80)
        self.signal_info_table.setWordWrap(False)

        table_layout.addWidget(self.signal_info_table)
        table_layout.setSizeConstraint(250)
        table_box.setLayout(table_layout)
        table_box.setMinimumHeight(340)  # Reduced overall height
        toolbar_layout.addWidget(table_box)

        toolbar_layout.addSpacing(5)

        # Third Section: Control Unit with Sliders, Dropdowns, and Additional Controls
        controls_box = QGroupBox("Control Unit")
        controls_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        controls_box.setStyleSheet("background-color: #d3d3d3; padding: 20px; font-size: 16px; font-weight: bold;")
        controls_layout = QVBoxLayout()

        # Slider creation function with adjusted spacing
        def create_slider(label_text, default_value):
            slider_layout = QVBoxLayout()
            slider_layout.setSpacing(2)  # Adjusted for tighter layout
            slider_label = QLabel(label_text)
            slider_label.setFixedHeight(20)
            slider_label.setStyleSheet("font-size: 14px; color: #333333;")

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(default_value)
            slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            slider.setStyleSheet("""
                QSlider::groove:horizontal { height: 8px; background: #f0f0f0; }
                QSlider::handle:horizontal { width: 8px; background: black; }
                QSlider::sub-page:horizontal { background: #2196F3; }
            """)

            value_label = QLabel(f"{default_value}")
            value_label.setFixedHeight(20)
            value_label.setAlignment(Qt.AlignCenter)
            slider.valueChanged.connect(lambda value: value_label.setText(f"{value}"))

            # Arrange label, slider, and value in a vertical layout
            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)

            return slider, slider_layout

        self.frequency_slider, frequency_slider_layout = create_slider("Sampling Frequency", 2)
        controls_layout.addLayout(frequency_slider_layout)
        self.frequency_slider.valueChanged.connect(self.update_stem_plot)
        self.frequency_slider.setRange(2,40)

        self.SNR_slider, SNR_slider_layout = create_slider("SNR", 100)
        controls_layout.addLayout(SNR_slider_layout)
        self.SNR_slider.valueChanged.connect(lambda: self.update_plot_with_noise())

        dropdown_layout = QFormLayout()
        dropdown_layout.setHorizontalSpacing(10)

        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Linear", "Quadratic", "Sinusoid"])  # Add options to the combobox
        self.type_dropdown.setStyleSheet("padding: 5px; height: 30px;")
        self.type_dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.type_dropdown.currentIndexChanged.connect(self.update_reconstruction)
        reconstruction_label = QLabel("Reconstruction Method")
        reconstruction_label.setFixedHeight(20)
        reconstruction_label.setStyleSheet("font-size: 14px; color: #333333;")

        dropdown_layout.addRow(reconstruction_label, self.type_dropdown)

        controls_layout.addLayout(dropdown_layout)

        # Additional controls
        adding_signal_box = QGroupBox("Adding Signal")
        adding_signal_box.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
        """)

        # Layout for Adding Signal section
        adding_signal_layout = QVBoxLayout()

        # Frequency and Amplitude Labels and Input Fields
        frequency_label = QLabel("Frequency:")
        frequency_label.setFixedWidth(120)
        frequency_label.setStyleSheet("font-size: 14px; color: #333333; padding-right: 10px;")
        self.freq_input = QLineEdit("1")
        self.freq_input.setFixedHeight(30)
        self.freq_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.freq_input.setStyleSheet("padding: 5px;")

        amplitude_label = QLabel("Amplitude:")
        amplitude_label.setFixedWidth(120)
        amplitude_label.setStyleSheet("font-size: 14px; color: #333333; padding-right: 10px;")
        self.amplitude_input = QLineEdit("1")
        self.amplitude_input.setFixedHeight(30)
        self.amplitude_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.amplitude_input.setStyleSheet("padding: 5px;")

        # Add Signal Button
        add_signal_button = QPushButton("Add Signal")
        add_signal_button.setStyleSheet(
            "font-size: 14px; padding: 10px; background-color: #2196F3; color: white; border-radius: 5px;")
        add_signal_button.clicked.connect(
            lambda: self.signal_manager.add_signal_component(self.freq_input.text(), self.amplitude_input.text(), self))

        input_form = QFormLayout()
        input_form.setHorizontalSpacing(5)
        input_form.addRow(frequency_label, self.freq_input)
        input_form.addRow(amplitude_label, self.amplitude_input)


        # Add Widgets to Adding Signal Layout
        adding_signal_layout.addLayout(input_form)
        adding_signal_layout.addWidget(add_signal_button)

        # Set Layout and Add to Controls Layout
        adding_signal_box.setLayout(adding_signal_layout)
        controls_layout.addWidget(adding_signal_box)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(
            "font-size: 14px; padding: 10px; background-color: #2196F3; color: white; border-radius: 5px;")

        # Form layout for labels and input fields
        clear_button.clicked.connect(self.delete_selected_signal)

        controls_layout.addWidget(add_signal_button)
        controls_layout.addWidget(clear_button)

        controls_box.setLayout(controls_layout)
        toolbar_layout.addWidget(controls_box)

        # Container widget for layout
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar_widget.setStyleSheet("background-color: #f0f0f0; padding: 10px;")

        horizontal_layout.addWidget(toolbar_widget)
        self.setLayout(horizontal_layout)



    def check_data_validity(self, samples, sampled_amplitude):
        try:

            samples = np.array(samples)
            sampled_amplitude = np.array(sampled_amplitude)
            print(f"Checking Data - Samples: {samples}, Sampled Amplitude: {sampled_amplitude}")

            if len(samples) < 2 or len(sampled_amplitude) < 2:
                print("Error: Not enough data points for interpolation.")
                return False

            if np.any(np.isnan(samples)) or np.any(np.isnan(sampled_amplitude)):
                print("Error: Data contains NaN values.")
                return False

            return True
        except Exception as e:
            print(f"Error during data validity check: {e}")
            return False



    def update_reconstruction(self):
        print("Updating reconstruction...")


        self.samples = np.array(self.samples)
        self.sampled_amplitude = np.array(self.sampled_amplitude)

        print(f"Before Reconstruction - Samples: {self.samples}, Sampled Amplitude: {self.sampled_amplitude}")


        if self.check_data_validity(self.samples, self.sampled_amplitude):

            self.reconstruct(self.samples, self.sampled_amplitude)
        else:
            print("Data is not valid for reconstruction.")

        print(f"After Reconstruction - Samples: {self.samples}, Sampled Amplitude: {self.sampled_amplitude}")

    def add_signal_to_table( self,name, frequency, amplitude):
        """Insert a new row in the signal info table with the provided signal name, frequency, and amplitude."""
        row_position = self.signal_info_table.rowCount()
        self.signal_info_table.insertRow(row_position)

        self.signal_info_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.signal_info_table.setItem(row_position, 1, QTableWidgetItem(f"{frequency} Hz"))
        self.signal_info_table.setItem(row_position, 2, QTableWidgetItem(str(amplitude)))
    def delete_selected_signal(self):
        """Delete the selected signal from the table and SignalManager."""
        selected_row = self.signal_info_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a signal to delete.")
            return

        # Get signal ID (assuming name is unique)
        signal_name = self.signal_info_table.item(selected_row, 0).text()
        signal_id = next((signal.signal_id for signal in self.signal_manager.signals if signal.name == signal_name), None)

        if signal_id is not None:
            # Remove signal from SignalManager
            self.signal_manager.remove_signal(signal_id)

            # Remove row from table
            self.signal_info_table.removeRow(selected_row)

            # Update plot after deletion
            self.Clear()
            self.signal_manager.plot_callback()

        else:
            QMessageBox.warning(self, "Error", "Signal not found.")
    def Clear(self):
        if not self.signal_manager.signals:
            self.signal_viewer.clear()
            self.reconstruction_viewer.clear()
            self.difference_viewer.clear()
            self.freq_viewer.clear()

    def plot_signals(self):
        if not self.signal_manager.signals:
            QMessageBox.warning(self, "No Signal", "No signals to plot.")
            return

        time, noisy_signal = self.signal_manager.get_combined_signal_with_noise()
        if time is None or noisy_signal is None:
            return

        if not hasattr(self, 'noisy_plot') or self.noisy_plot is None:
            self.noisy_plot = self.signal_viewer.plot(time, noisy_signal, pen='r')
        else:
            self.noisy_plot.setData(time, noisy_signal)
        if self.signal_manager.signals:
            self.start(noisy_signal, time)

    def update_plot_with_noise(self):
        """Update the plot when SNR slider value changes."""
        self.signal_manager.set_snr(self.SNR_slider.value())
        self.plot_signals()

    # def upload_signal(self):
    #     options = QFileDialog.Options()
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
    #                                                options=options)
    #     if file_path:
    #         try:
    #             self.data = pd.read_csv(file_path)
    #             self.start()
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{e}")

    def start(self,amplitude,time):
        self.time = time
        self.amplitude = amplitude
        self.take_samples(self.time, self.amplitude, self.sampling_frequency)
        self.stem_plot(self.samples, self.sampled_amplitude)
        self.plot(self.time, self.amplitude)
        self.reconstruct(self.samples, self.sampled_amplitude)

    def plot(self, time, amplitude):
        # Plot the original signal if not already plotted
        if not hasattr(self, 'original_plot') or self.original_plot is None:
            self.original_plot = self.signal_viewer.plot(time, amplitude,
                                                         pen=pg.mkPen('#2196F3', width=3))  # Set line color and width
        else:
            self.original_plot.setData(time, amplitude)  # Update data if plot already exists



    def stem_plot(self, time, amplitude):
        # Clear previous sampled plots, including vertical lines and dots
        if hasattr(self, 'sampled_items'):
            for item in self.sampled_items:
                self.signal_viewer.removeItem(item)

        # Create a list to store the new sampled plot items (vertical lines and dots)
        self.sampled_items = []

        # Plot vertical lines and sample dots for the sampled signal
        for x, y in zip(time, amplitude):
            # Plot and store each vertical line
            line = self.signal_viewer.plot([x, x], [0, y], pen=pg.mkPen('r'))
            self.sampled_items.append(line)

        # Plot and store dots as a single item with reduced size
        dots = self.signal_viewer.plot(time, amplitude, pen=None, symbol='o', symbolBrush='r',
                                       symbolSize=7)  # Adjust size as needed
        self.sampled_items.append(dots)

    def update_stem_plot(self):
        self.sampling_frequency = self.frequency_slider.value()
        try:
            self.take_samples(self.time, self.amplitude, self.sampling_frequency)
            self.stem_plot(self.samples, self.sampled_amplitude)
            self.reconstruct(self.samples, self.sampled_amplitude)
        except:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Upload Signal first")
            msg_box.setWindowTitle("Upload Error !")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def calculate_max_frequency(self, amplitude):
        # Use FFT to find the maximum frequency component
        spectrum = np.fft.fft(amplitude)
        freqs = np.fft.fftfreq(len(amplitude), d=(self.time[1] - self.time[0]))  # Assuming uniform sampling
        max_freq = np.abs(freqs[np.argmax(np.abs(spectrum))])
        return max_freq

    def take_samples(self, time, amplitude, sampling_frequency):
        self.samples = np.arange(time[0], time[len(time) - 1], (1 / sampling_frequency))
        self.sampled_amplitude = np.interp(self.samples, time, amplitude)
        self.plot(self.time, self.amplitude)


    def linear_interpolation(self, x_known, y_known, num_points=500):
        print(f"Linear Interpolation called with x_known: {x_known}")
        print(f"Linear Interpolation called with y_known: {y_known}")

        if len(x_known) < 2 or len(y_known) < 2:
            print("Error: Not enough data points for interpolation.")
            return None, None

        try:
            x_known = np.array(x_known)
            y_known = np.array(y_known)

            x_interp = np.linspace(np.min(x_known), np.max(x_known), num_points)
            print(f"x_interp (size: {len(x_interp)}): {x_interp}")

            linear_interp = interp1d(x_known, y_known, kind='linear')
            print(f"linear_interp object created")

            y_interp = linear_interp(x_interp)
            print(f"y_interp (size: {len(y_interp)}): {y_interp}")

            print("Linear interpolation completed successfully.")
            return x_interp, y_interp
        except ValueError as e:
            print(f"ValueError during linear interpolation: {e}")
            return None, None
        except Exception as e:
            print(f"Unexpected error during linear interpolation: {e}")
            return None, None

    def quadratic_interpolation(self, x_known, y_known, num_points=500):
        print(f"Quadratic Interpolation called with x_known: {x_known}")
        print(f"Quadratic Interpolation called with y_known: {y_known}")

        if len(x_known) < 2 or len(y_known) < 2:
            print("Error: Not enough data points for interpolation.")
            return None, None

        try:
            x_interp = np.linspace(min(x_known), max(x_known), num_points)
            quadratic_interp = interp1d(x_known, y_known, kind='quadratic')
            y_interp = quadratic_interp(x_interp)
            print("Quadratic interpolation completed successfully.")
            return x_interp, y_interp
        except Exception as e:
            print(f"Error during quadratic interpolation: {e}")
            return None, None

    def reconstruct(self, samples, sampled_amplitude):
        print("Reconstructing signal...")


        self.reconstruction_viewer.clear()


        method = self.type_dropdown.currentText()

        if method == "Linear":

            reconstructed_time, reconstructed_amplitude = self.linear_interpolation(samples, sampled_amplitude)
        elif method == "Quadratic":

            reconstructed_time, reconstructed_amplitude = self.quadratic_interpolation(samples, sampled_amplitude)
        else:

            reconstructed_amplitude, reconstructed_time = scipy.signal.resample(sampled_amplitude, 5000, samples)

        if reconstructed_time is not None and reconstructed_amplitude is not None:

            self.reconstruction_viewer.plot(reconstructed_time, reconstructed_amplitude, pen='b')
            print("Reconstruction complete.")
        else:
            print("Reconstruction failed due to invalid data.")
        self.plot_frequency(reconstructed_amplitude, reconstructed_time)
        self.get_difference_plot()
        self.difference_viewer.plot(reconstructed_time, reconstructed_amplitude, pen='r')

    def get_difference_plot(self):
        self.difference_viewer.clear()
        self.difference_viewer.plot(self.time, self.amplitude, pen='b')


    def plot_frequency(self, reconstructed_amplitude, reconstructed_time):
        N = len(reconstructed_amplitude)  # Number of samples
        fourier_transform = np.fft.fft(reconstructed_amplitude)
        # Take only the positive half
        fourier_transform = fourier_transform[:]
        freq = np.fft.fftfreq(N, d=(reconstructed_time[1] - reconstructed_time[0]))[:N // 2]
        magnitude = np.abs(fourier_transform[:N // 2])
        # Extract the real part of the Fourier transform for positive frequencies
        # real_part = np.real(fourier_transform)

        # Clear previous frequency plot
        self.freq_viewer.clear()

        # Plot frequency domain data using real part
        self.freq_viewer.plot(freq, magnitude, pen='b')
        self.freq_viewer.showGrid(x=True, y=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GUI()
    main_window.show()
    sys.exit(app.exec_())
