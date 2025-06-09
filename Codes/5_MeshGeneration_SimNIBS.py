import streamlit as st
import subprocess
import os

st.set_page_config(page_title="CHARM Head Model Generator", layout="centered")
st.title("Generate CHARM Computational Head Model")

# --- Define Base Directory ---
PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"

# --- Prefilled Paths ---
default_subject = "sub-001"
default_session = "ses-01"
default_t1 = os.path.join(PWD, "BIDS", default_subject, default_session, "anat", f"{default_subject}_{default_session}_T1w_e1.nii.gz")
default_t2 = os.path.join(PWD, "BIDS", default_subject, default_session, "anat", f"{default_subject}_{default_session}_T2w.nii.gz")
default_output_dir = os.path.join(PWD, "HeadModels")

# --- User Inputs ---
subject_id = st.text_input("Subject ID (e.g., sub-001):", default_subject)
t1_path = st.text_input("Path to T1-weighted image:", default_t1)
t2_path = st.text_input("Path to T2-weighted image:", default_t2)
output_dir = st.text_input("Output Directory (optional, default is current directory):", value=default_output_dir)

run_button = st.button("Generate Head Model")

if run_button:
    if all([subject_id, t1_path, t2_path]):
        try:
            with st.spinner("Running CHARM head model generation..."):
                subprocess.run(["charm", subject_id, t1_path, t2_path], cwd=output_dir, check=True)

            st.success(f"✅ Head model generation complete in: {output_dir}")
        except subprocess.CalledProcessError as e:
            st.error(f"❌ CHARM execution failed: {e}")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")
    else:
        st.warning("Please fill in all fields before running CHARM.")
