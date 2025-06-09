# 🧠 fMRI-Guided TMS GUI Suite

This project provides a collection of Streamlit and Python GUI tools for an end-to-end fMRI-guided TMS (Transcranial Magnetic Stimulation) pipeline. It includes DICOM conversion, AFNI preprocessing, ROI-based analysis, functional connectivity targeting, CHARM mesh generation, electric field simulation, and visualization tools — all wrapped in a simple launcher interface.

---

## 🚀 GUI Tools Included

| Tool                                      | Description                                                       |
|-------------------------------------------|-------------------------------------------------------------------|
| **DICOM to BIDS Converter**               | Converts DICOM folders to BIDS using `dcm2niix`                   |
| **AFNI Preprocessing Pipeline**           | Preprocesses fMRI data using `afni_proc.py`                       |
| **Brainnetome Activation Visualizer**     | Extracts and plots regional activation using BNA masks            |
| **Seed-to-Target FC (cluster-based)**     | FC targeting with permutation threshold and `3dClusterize`        |
| **Seed-to-Target FC (min/max)**           | Finds strongest positive and negative FC voxels for targeting     |
| **Mesh Generation (CHARM)**               | Generates subject-specific head model using SimNIBS CHARM         |
| **MNI to Subject Coordinate Converter**   | Converts MNI coordinates to subject space using SimNIBS           |
| **TMS EF Simulation**                     | Runs EF simulation using SimNIBS Python API and coil optimization |
| **AFNI Sub-brick Viewer**                 | Visualizes individual statistical sub-bricks in MNI space         |

Each module is launched from a central `app_launcher.py` GUI or can be run independently.

---

## 📦 Requirements

### ✅ Python Version

- Python 3.8 or newer  
  _(Recommended: install via [Anaconda](https://www.anaconda.com/) or use SimNIBS's Python environment)_

### ✅ Python Packages

Install all required packages using:

```bash
pip install -r requirements.txt
