import streamlit as st
import os
import subprocess

st.set_page_config(page_title="AFNI Preprocessing GUI", layout="wide")
st.title("🧠 AFNI Task-fMRI Preprocessing Pipeline")

# Define base directory (PWD)
PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"

# Default folders derived from PWD
default_bids = os.path.join(PWD, "BIDS")
default_output = os.path.join(PWD, "Preprocess")
default_required = os.path.join(PWD, "Required")
default_stim = os.path.join(default_required, "stimfolder")
default_slice_timing = os.path.join(default_required, "slice_timing_SB.txt")
default_template = os.path.join(default_required, "MNI152_T1_2009c.nii")

# --- User Inputs with Pre-Filled Defaults ---
subj = st.text_input("👤 Subject ID:", "sub-001")
session = st.text_input("🗂 Session ID:", "ses-01")
bids_dir = st.text_input("📂 BIDS directory:", default_bids)
stim_dir = st.text_input("📁 Stimulus folder:", default_stim)
slice_timing_file = st.text_input("🕒 Slice timing file:", default_slice_timing)
block_duration = st.number_input("🕐 Block duration (sec):", min_value=1, value=31)
output_dir = st.text_input("📤 Output results directory:", default_output)
template_path = st.text_input("📌 MNI Template:", default_template)
anat_echo = st.selectbox("🧬 Anatomical echo:", options=["e1", "e2", "e3", "e4"], index=0)


# --- Run Button ---
if st.button("🚀 Run AFNI Preprocessing"):
    if not all([subj, session, bids_dir, stim_dir, output_dir, template_path]):
        st.error("❌ Please fill in all required fields.")
    else:
        try:
            task_id = f"{subj}-{session}_SB"
            epi_file = os.path.join(bids_dir, subj, session, "func", f"{subj}_{session}_task-craving_run-01_bold.nii.gz")
            anat_file = os.path.join(bids_dir, subj, session, "anat", f"{subj}_{session}_T1w_{anat_echo}.nii.gz")
            stim_meth = os.path.join(stim_dir, "meth-R2.1D")
            stim_neut = os.path.join(stim_dir, "neutral-R2.1D")
            result_dir = os.path.join(output_dir, task_id)

            # --- Check for required files ---
            missing = []
            for path in [epi_file, anat_file, stim_meth, stim_neut, template_path]:
                if not os.path.isfile(path):
                    missing.append(path)

            if missing:
                st.error("🚫 Missing file(s):\n" + "\n".join(missing))
                st.stop()

            os.makedirs(result_dir, exist_ok=True)
            os.chdir(result_dir)

            # --- Refit Template to MNI ---
            st.write("📐 Re-referencing template to MNI space...")
            subprocess.run(["3drefit", "-space", "MNI", template_path])

            # --- AFNI Command ---
            cmd = [
                "afni_proc.py",
                "-subj_id", task_id,
                "-dsets", epi_file,
                "-copy_anat", anat_file,
                "-anat_has_skull", "yes",
                "-blocks", "tshift", "align", "tlrc", "volreg", "blur", "mask", "scale", "regress"
            ]

            if slice_timing_file:
                cmd.extend(["-tshift_opts_ts", "-tpattern", f"@{slice_timing_file}"])

            cmd.extend([
                "-anat_uniform_method", "unifize",
                "-align_opts_aea", "-cost", "lpc+ZZ", "-giant_move",
                "-tlrc_base", template_path,
                "-tlrc_NL_warp",
                "-volreg_align_to", "MIN_OUTLIER",
                "-volreg_align_e2a",
                "-volreg_tlrc_warp",
                "-volreg_warp_dxyz", "2.0",
                "-blur_size", "6.0",
                "-regress_stim_times", stim_meth, stim_neut,
                "-regress_stim_labels", "meth", "neutral",
                "-regress_basis_multi", f"BLOCK({int(block_duration)},1)", f"BLOCK({int(block_duration)},1)",
                "-regress_censor_motion", "0.3",
                "-regress_censor_outliers", "0.1",
                "-regress_opts_3dD", "-bout",
                "-gltsym", "SYM: meth -neutral",
                "-glt_label", "1", "meth_vs_neutral",
                "-remove_preproc_files",
                "-execute"
            ])

            # --- Run AFNI Preprocessing ---
            st.write("🧠 Running AFNI preprocessing...")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            st.success("✅ Preprocessing complete.")
            st.text(result.stdout)

        except Exception as e:
            st.error(f"❌ Error during processing:\n{str(e)}")
