# Sampling-Theory Studio

## Introduction
Sampling an analog signal is a crucial step in any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees the full recovery of a signal when sampled at a frequency greater than or equal to its bandwidth (or twice the maximum frequency for real signals). This project demonstrates the importance and validation of the Nyquist rate through an interactive desktop application.

---

## Features

### 1. **Sample & Recover**
- Load a mid-length signal (~1000 points).
- Visualize the signal and sample it at various frequencies.
- Recover the original signal using the Whittaker–Shannon interpolation formula.
- Display four graphs:
  1. Original signal with sampled points.
  2. Reconstructed signal.
  3. Difference between the original and reconstructed signals.
  4. Frequency domain visualization to check for aliasing.
- Sampling frequency is displayed as actual or normalized values (e.g., 0×fmax to 4×fmax).


### 2. **Load & Compose**
- Load signals from a file or create a mixed signal using the signal mixer.
- Add sinusoidal components with adjustable frequencies and magnitudes.
- Remove components dynamically while preparing the mixed signal.
- Ensure default values are displayed to avoid empty fields.
![Start](https://github.com/user-attachments/assets/c1fcb829-67b4-49bc-81ef-a824fdd9c87d)


### 3. **Additive Noise**
- Add noise to the loaded signal with a custom signal-to-noise ratio (SNR).
- Demonstrate the dependency of noise effect on signal frequency.
![Noisy_signal](https://github.com/user-attachments/assets/403c7499-6f15-4ab3-9c1b-ba0a7b74aa58)


### 4. **Real-Time Processing**
- Sampling and recovery occur in real time without requiring “Update” or “Refresh” buttons.

*(Insert video showing real-time updates)*

### 5. **Reconstruction Methods**
- Explore multiple signal reconstruction methods, including Whittaker–Shannon interpolation.
- Allow users to select a reconstruction method via a combobox.
- Compare methods based on performance, with explanations of their pros and cons.

- ![Methods](https://github.com/user-attachments/assets/9e60ec13-7f43-4bbc-9a78-e995a8f708b2)


### 6. **Resizable Interface**
- The application resizes gracefully without disrupting the UI layout.

### 7. **Testing Scenarios**
- Prepare at least three synthetic test signals to explore sampling and aliasing scenarios. Examples include:
  - **Scenario 1:** A mix of 2Hz and 6Hz sinusoids sampled at 12Hz (or above) for accurate recovery, but showing aliasing when sampled at 4Hz.
  - **Scenario 2:** Highlighting noise impact at different frequencies.
  - **Scenario 3:** Sampling a signal with a critical frequency component.
![Aliasing](https://github.com/user-attachments/assets/83f78e51-b2cd-4031-84c4-cc2686836955)

### 8. **Interactive Demo: Sampling Theory Studio App**
https://github.com/user-attachments/assets/441c5a2d-2587-4ccc-899f-2400b3b24709

---

## Project Structure

### Directories
- **src/**: Source code.
- **data/**: Predefined synthetic signals and test cases.
- **docs/**: Documentation and user guides.
- **outputs/**: Generated reports and saved graphs.

### Files
- **README.md**: Project overview and setup instructions.
- **requirements.txt**: List of dependencies.
- **main.py**: Entry point for the application.
- **sampling.py**: Signal sampling and recovery logic.
- **noise_utils.py**: Noise addition and SNR adjustments.
- **ui_design.ui**: Qt Designer file for UI layout.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ziadmohammed200/Signal-Studio.git
   cd sampling-theory-studio
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

---

## Usage

1. **Load or Compose Signals**:
   - Use the "Load Signal" button to import a signal file.
   - Alternatively, create a mixed signal using the signal composer.

2. **Add Noise**:
   - Adjust the SNR slider to add noise to the signal.

3. **Sample and Recover**:
   - Adjust the sampling frequency and observe the reconstruction in real time.

4. **Test Different Reconstruction Methods**:
   - Select a reconstruction method from the combobox and compare results.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
- Inspired by digital signal processing principles and the Nyquist–Shannon sampling theorem.
## Contributors
- [Ziad Mohamed](https://github.com/Ziadmohammed200) 
- [Marcilino Adel](https://github.com/marcilino-adel)
- [Pavly Awad](https://github.com/PavlyAwad)
- [Ahmed Etman](https://github.com/AhmedEtma)







