import streamlit as st
import subprocess
import os
import pandas as pd

# Define mapping table
mapping = {
    "DICOM_Folder": [
        "T1W_MPR_VNAV_4E_0015", "T2W_SPC_VNAV_0026",
        "CRAVING_0021", "CRAVING_0022", "CRAVING_MB_0031",
        "CRAVING_MB_0032", "CRAVING_MB_SBREF_0030",
        "REST_PA_0010", "REST_PA_0011", "REST_PA_SBREF_0009"
    ],
    "Modality": [
        "T1w", "T2w",
        "task-craving_run-01_bold", "task-craving_run-02_bold",
        "task-craving_run-03_bold", "task-craving_run-04_bold",
        "task-craving_run-03_sbref",
        "task-rest_run-01_bold", "task-rest_run-02_bold",
        "task-rest_run-01_sbref"
    ]
}
df = pd.DataFrame(mapping)

# GUI
st.title("DICOM to BIDS Converter")

dicom_root = st.text_input("📂 Enter DICOM root folder:")
bids_root = st.text_input("📁 Enter BIDS output directory:")
subject = st.text_input("👤 Subject ID (e.g., sub-001):")
session = st.text_input("🗂 Session ID (e.g., ses-01):")

if st.button("🚀 Run Conversion"):
    if not dicom_root or not bids_root or not subject or not session:
        st.error("❌ All fields must be filled in.")
    else:
        for _, row in df.iterrows():
            dicom_subfolder = row["DICOM_Folder"]
            modality = row["Modality"]
            modality_type = "anat" if "T1w" in modality or "T2w" in modality else "func"
            input_dir = os.path.join(dicom_root, dicom_subfolder)
            output_dir = os.path.join(bids_root, subject, session, modality_type)
            filename = f"{subject}_{session}_{modality}"

            if os.path.isdir(input_dir):
                os.makedirs(output_dir, exist_ok=True)
                cmd = ["dcm2niix", "-i", "n", "-z", "y", "-f", filename, "-o", output_dir, input_dir]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                st.success(f"✅ Converted: {dicom_subfolder}")
                st.text(result.stdout)
            else:
                st.warning(f"⚠️ Skipped: {dicom_subfolder} not found.")
