# Full script integrating all updated steps for seed-to-target FC targeting pipeline (without EF)
# This script assumes AFNI is installed and available in the environment

import streamlit as st
import subprocess
import os
import numpy as np
from tqdm import tqdm

# --- Streamlit Setup ---
st.set_page_config(page_title="Robust Seed-to-Target FC Targeting", layout="centered")
st.title("🎯 Seed-to-Target FC Analysis with Permutation and Cluster Targeting")

PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"

# --- Default Paths ---
default_ts_dset = os.path.join(PWD, "Preprocess", "sub-001-ses-01_SB", "sub-001-ses-01_SB.results", "errts.sub-001-ses-01_SB+tlrc")
default_seed_mask = os.path.join(PWD, "Required", "BNA_211_rs.nii")
default_target_mask = os.path.join(PWD, "Required", "Left_DLPFC_mask_AAL_rs.nii")
default_output_prefix = "sub-001_SB"

# --- Inputs ---
ts_dset = st.text_input("📂 Path to AFNI Time Series Dataset:", default_ts_dset)
seed_mask = st.text_input("🌱 Path to Seed Mask:", default_seed_mask)
target_mask = st.text_input("🎯 Path to Target Mask:", default_target_mask)
output_prefix = st.text_input("📁 Output Prefix:", default_output_prefix)
n_perm = st.number_input("🔁 Number of Permutations:", min_value=100, max_value=5000, value=1000, step=100)

# --- Run Button ---
if st.button("🚀 Run Full FC Targeting Pipeline"):
    if all([ts_dset, seed_mask, target_mask, output_prefix]):
        output_dir = os.path.join(PWD, "Targeting", output_prefix)
        os.makedirs(output_dir, exist_ok=True)

        avg_ts = os.path.join(output_dir, f"{output_prefix}_avg_ts.1D")
        corr_map = os.path.join(output_dir, f"{output_prefix}_seed2target_corr.nii.gz")

        # --- Step 1: Average Seed Time Series ---
        st.write("📌 Extracting average seed time series...")
        subprocess.run(["3dmaskave", "-quiet", "-mask", seed_mask, ts_dset], stdout=open(avg_ts, "w"))

        # --- Step 2: Compute Seed-to-Voxel Correlation ---
        st.write("📌 Computing seed-to-target correlation map...")
        subprocess.run(["3dTcorr1D", "-mask", target_mask, "-prefix", corr_map, ts_dset, avg_ts])

        # --- Step 3: Permutation Testing ---
        st.write("📊 Running permutation testing to determine r threshold...")
        null_max_r = []
        with open(avg_ts, 'r') as f:
            seed_ts_original = np.array([float(val) for val in f.read().strip().split()])

        for i in tqdm(range(n_perm), desc="Permutations"):
            perm_indices = np.random.permutation(len(seed_ts_original))
            seed_ts_shuffled = seed_ts_original[perm_indices]

            perm_ts_file = os.path.join(output_dir, f"perm_ts_{i:04d}.1D")
            with open(perm_ts_file, 'w') as f:
                for val in seed_ts_shuffled:
                    f.write(f"{val:.6f}\n")

            perm_corr_map = os.path.join(output_dir, f"perm_corr_{i:04d}.nii.gz")
            subprocess.run(["3dTcorr1D", "-mask", target_mask, "-prefix", perm_corr_map, ts_dset, perm_ts_file],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            dump_file = os.path.join(output_dir, f"perm_corr_{i:04d}.txt")
            subprocess.run(["3dmaskdump", "-noijk", "-mask", target_mask, perm_corr_map], stdout=open(dump_file, 'w'))
            try:
                with open(dump_file, 'r') as f:
                    vals = [float(line.strip()) for line in f if line.strip()]
                    if vals:
                        null_max_r.append(max(np.abs(vals)))
                    else:
                        print(f"⚠️ Warning: Empty correlation file in permutation {i}")
            except ValueError:
                print(f"⚠️ Warning: Non-numeric values in {dump_file}, skipping permutation {i}")

        if null_max_r:
            r_thresh = np.percentile(null_max_r, 95)
            st.write(f"✅ Permutation-based threshold (p<0.05, two-sided): r = {r_thresh:.4f}")

            # --- Step 4: Threshold Correlation Map ---
            sig_mask = os.path.join(output_dir, f"{output_prefix}_sig_mask.nii.gz")
            subprocess.run(["3dcalc", "-a", corr_map, "-expr", f'ispositive(abs(a)-{r_thresh:.4f})', "-prefix", sig_mask])

            # --- Step 5: Cluster Analysis ---
            cluster_map = os.path.join(output_dir, f"{output_prefix}_cluster_map.nii.gz")
            subprocess.run(["3dClusterize", "-inset", corr_map, "-mask", sig_mask,
                            "-idat", "0", "-ithr", "0", "-NN", "1", "-clust_nvox", "5",
                            "-bisided", "p=0.05", "-pref_map", cluster_map])

            # --- Step 6: Extract Center of Mass ---
            st.write("📌 Extracting center of mass of the final cluster...")
            result = subprocess.run(["3dCM", "-mask", cluster_map, cluster_map],
                                    stdout=subprocess.PIPE, text=True)
            try:
                coords = list(map(float, result.stdout.strip().split()))
                flipped_coords = (-coords[0], -coords[1], coords[2])
                st.success("🎯 Target coordinate (flipped for TMS space):")
                st.code(f"{flipped_coords[0]:.2f}, {flipped_coords[1]:.2f}, {flipped_coords[2]:.2f}")
            except:
                st.warning("⚠️ Could not parse center of mass output.")
        else:
            st.error("❌ No valid permutations produced usable results. Please check your data and masks.")
    else:
        st.warning("⚠️ Please fill in all fields before running the pipeline.")
