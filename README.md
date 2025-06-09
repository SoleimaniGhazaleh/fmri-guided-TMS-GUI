# ­ЪДа fMRI-Guided TMS GUI Suite

This project provides a collection of Streamlit and Python GUI tools for an end-to-end fMRI-guided TMS (Transcranial Magnetic Stimulation) pipeline. It includes DICOM conversion, AFNI preprocessing, ROI-based analysis, functional connectivity targeting, CHARM mesh generation, electric field simulation, and visualization tools Рђћ all wrapped in a simple launcher interface.

---

## ­Ъџђ GUI Tools Included

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

## ­ЪД░ Requirements

### РюЁ Python Version

- Python 3.8 or newer  
  _(Recommended: install via [Anaconda](https://www.anaconda.com/) or use SimNIBS's Python environment)_

### РюЁ Python Packages

Install all required packages using:

```bash
pip install -r requirements.txt
```

#### `requirements.txt` content:

```
streamlit
pandas
numpy
matplotlib
tqdm
nibabel
nilearn
simnibs
```

> Рџа№ИЈ `simnibs` should **only** be used inside the official SimNIBS Python environment. See: [SimNIBS Installation](https://simnibs.github.io/simnibs/build/html/installation/index.html)

---

## ­ЪћД External Tools

You must install the following tools and ensure they're accessible in your terminal (`$PATH`):

| Tool                    | Purpose                                                  | Required | Install Link |
|-------------------------|----------------------------------------------------------|----------|---------------|
| **AFNI**                | Preprocessing, FC, sub-brick stats, cluster analysis     | РюЁ       | https://afni.nimh.nih.gov |
| **dcm2niix**            | DICOM to NIfTI conversion                                | РюЁ       | https://github.com/rordenlab/dcm2niix |
| **SimNIBS**             | Head model + EF simulation + coordinate conversion       | РюЁ       | https://simnibs.github.io/simnibs |
| **CHARM** (`charm`)     | Subject-specific mesh generation                         | РюЁ       | included in SimNIBS |
| **mni2subject_coords**  | Converts MNI coordinates to subject space                | РюЁ       | included in SimNIBS |
| **Gmsh**                | Visualize optimized TMS coil placement                   | Optional | https://gmsh.info |

Test tool availability with:

```bash
afni_proc.py -help
3dmaskave -help
dcm2niix --version
mni2subject_coords -h
charm --help
gmsh --version
```

---

## ­ЪЊѓ Folder Structure

```
fmri-guided-TMS-GUI/
РћюРћђРћђ app_launcher.py              # Main GUI launcher (Tkinter)
РћюРћђРћђ requirements.txt             # Python packages
РћюРћђРћђ README.md                    # Project documentation
РћюРћђРћђ Codes/                       # All Streamlit GUI modules
Рћѓ   РћюРћђРћђ 1_dicom_to_bids_gui.py
Рћѓ   РћюРћђРћђ 2_afni_preproc_gui.py
Рћѓ   РћюРћђРћђ ...
РћюРћђРћђ Required/                    # Templates, masks, slice timing, stimuli
Рћѓ   РћюРћђРћђ MNI152_T1_2009c.nii
Рћѓ   РћюРћђРћђ slice_timing_SB.txt
Рћѓ   РћюРћђРћђ stimfolder/
Рћѓ   РћюРћђРћђ BNA_ROI/
Рћѓ   РћюРћђРћђ BNA_211_rs.nii
Рћѓ   РћћРћђРћђ Left_DLPFC_mask_AAL_rs.nii
РћюРћђРћђ HeadModels/                  # Optional SimNIBS head model folder
РћћРћђРћђ .gitignore                   # (Recommended: exclude .nii, .msh, .mat files)
```

---

## РќХ№ИЈ How to Use

### Run the Main GUI

```bash
python app_launcher.py
```

### Run a Module Independently

```bash
streamlit run Codes/8_EFsimulation.py
```

---

## ­ЪЎІРђЇРЎђ№ИЈ Author

Ghazaleh Soleimani  
[soleimanighazaleh.github.io](https://soleimanighazaleh.github.io)

---

## ­ЪЊё License

This repository is for academic and research use. Please cite appropriately if adapted or extended.
