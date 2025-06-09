# 🧠 fMRI-Guided TMS GUI

A user-friendly graphical interface (GUI) for generating individualized TMS targets and electric field simulations using fMRI data. This end-to-end pipeline guides you from raw DICOM data to electric field (EF) visualization — optimized for researchers and clinicians working with neuromodulation interventions.

---

## 📆 Features

- ✅ DICOM to BIDS conversion
- ✅ fMRI preprocessing using AFNI
- ✅ Task contrast visualization (e.g., Drug > Neutral)
- ✅ Brain parcellation and coordinate extraction (e.g., Brainnetome)
- ✅ MNI-to-subject space transformation
- ✅ SimNIBS head model generation
- ✅ Electric field simulation (with coil specification and intensity control)

---

## 🖥️ GUI Overview

All steps are integrated into a clean, clickable GUI using Python and `Streamlit`. No command-line scripting required once setup is complete.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SoleimaniGhazaleh/fmri-guided-TMS-GUI.git
cd fmri-guided-TMS-GUI
```

### 2. Install Requirements

Use a virtual environment or conda environment. Then install dependencies:

```bash
pip install -r requirements.txt
```

Or minimal install for GUI only:

```bash
pip install streamlit
```

> Additional packages (e.g., AFNI, SimNIBS) may be required depending on your selected modules.

---

## 🧰 Launch the GUI

After setup, run:

```bash
python app_launcher.py
```

This will open the GUI where you can click through each step of the pipeline:

- Convert raw DICOM to BIDS format
- Preprocess fMRI using AFNI
- Visualize Drug > Neutral contrast
- Extract individualized TMS coordinates
- Generate SimNIBS head models
- Run electric field simulations

---

## 📂 Directory Structure

```
fmri-guided-TMS-GUI/
│
├── app_launcher.py                  # Main GUI launcher
├── 1_dicom_to_bids_gui.py          # Step 1
├── 2_afni_preproc_gui.py           # Step 2
├── 3_bna_plot_gui_local.py         # Step 3 (optional parcellation)
├── 4_coordinates_MNIspace.py       # Step 4
├── 5_MeshGeneration_SimNIBS.py     # Step 5
├── 6_mni_to_subject_gui.py         # Step 6
├── 7_ContrastVisualizatoin.py      # Step 7
├── 8_EFsimulation.py               # Step 8
├── assets/                         # Images and logos
└── README.md
```

---

## 🧠 Application

This tool is designed to assist with:

- Personalized TMS targeting based on individual fMRI responses
- Network-guided neuromodulation (e.g., frontopolar, DLPFC)
- Simulation of induced electric fields using SimNIBS

---

## 📘 Citation

If you use this pipeline in your research, please cite the following paper:

**Soleimani, Ghazaleh, Christine A. Conelea, Rayus Kuplicki, Alexander Opitz, Kelvin O. Lim, Martin P. Paulus, and Hamed Ekhtiari.** "Targeting VMPFC - amygdala circuit with TMS in substance use disorder: A mechanistic framework." *Addiction Biology* 30, no. 1 (2025): e70011. [https://doi.org/10.1111/adb.70011](https://doi.org/10.1111/adb.70011)

---

## 🙋‍♀️ Author

**Ghazaleh Soleimani**  
Postdoctoral Researcher – Neuroimaging & Neuromodulation  
University of Minnesota / INTAM Network  
📧 [ghazaleh.soleimani@email.com](mailto:ghazaleh.soleimani@email.com)


