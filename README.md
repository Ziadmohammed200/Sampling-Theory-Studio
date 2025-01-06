# Sampling-Theory Studio

## Introduction
Sampling an analog signal is a crucial step in any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees the full recovery of a signal when sampled at a frequency greater than or equal to its bandwidth (or twice the maximum frequency for real signals). This project demonstrates the importance and validation of the Nyquist rate through an interactive desktop application.

---

## Features

### 1. **Sample & Recover**
- Load a  signal .
- Visualize the signal and sample it at various frequencies.
- Recover the original signal using the Whittaker–Shannon interpolation formula.
- Display four graphs:
  1. Original signal with sampled points.
  2. Reconstructed signal.
  3. Difference between the original and reconstructed signals.
  4. Frequency domain visualization to check for aliasing.
- Sampling frequency is displayed as actual in HZ.

 ![Aliasing](https://github.com/user-attachments/assets/83f78e51-b2cd-4031-84c4-cc2686836955)


### 2. **Load & Compose**
- User can:
- Load signals from a file or create a mixed signal using the signal mixer.
- Add sinusoidal components with adjustable frequencies and magnitudes .
- Remove components dynamically while preparing the mixed signal.
![Start](https://github.com/user-attachments/assets/c1fcb829-67b4-49bc-81ef-a824fdd9c87d)


### 3. **Additive Noise**
- User also can:
- Add noise to the loaded signal with a custom signal-to-noise ratio (SNR).

![Noisy_signal](https://github.com/user-attachments/assets/403c7499-6f15-4ab3-9c1b-ba0a7b74aa58)


### 4. **Real-Time Processing**
- Sampling and recovery occur in real time without requiring “Update” or “Refresh” buttons.

### 5. **Reconstruction Methods**
- Explore multiple signal reconstruction methods, including Whittaker–Shannon interpolation.
- Allow users to select a reconstruction method via a combobox.

- ![Methods](https://github.com/user-attachments/assets/9e60ec13-7f43-4bbc-9a78-e995a8f708b2)


### 6. **Resizable Interface**
- The application resizes gracefully without disrupting the UI layout.




### 8. **Interactive Demo: Sampling Theory Studio App**
https://github.com/user-attachments/assets/441c5a2d-2587-4ccc-899f-2400b3b24709

---

## Project Structure



### Files
- **README.md**: Project overview and setup instructions.
- **requirements.txt**: List of dependencies.
- **task2.py**: Entry point for the application.
- **icons/**: Icons of program.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/Ziadmohammed200/Signal-Studio.git](https://github.com/Ziadmohammed200/Sampling-Theory-Studio.git)
   cd sampling-theory-studio
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python task2.py
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







