import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import subprocess

st.set_page_config(page_title="BNA Activation Pipeline", layout="wide")
st.title("🧠 BNA Activation Extraction and Plotting Pipeline")

# Define base working directory
PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"

# Prefilled paths
default_mask_dir = os.path.join(PWD, "Required", "BNA_ROI")
default_stats_dset = os.path.join(PWD, "Preprocess", "sub-001-ses-01_SB", "sub-001-ses-01_SB.results", "stats.sub-001-ses-01_SB+tlrc[34]")
default_output_file = os.path.join(PWD, "Preprocess", "sub-001-ses-01_SB", "BNA_tstat_results.txt")

# Input paths
mask_dir = st.text_input("📁 Directory containing BNA region masks (e.g., extracted_region_1.nii ... extracted_region_246.nii):", default_mask_dir)
stats_dset = st.text_input("🧠 Full path to AFNI stats dataset (e.g., stats.sub-001_MB+tlrc[34]):", default_stats_dset)
output_file = st.text_input("💾 Output file name for extracted values (e.g., BNA_tstat_results.txt):", default_output_file)

if st.button("🚀 Run BNA Extraction and Plot"):
    if not (os.path.exists(mask_dir) and "[" in stats_dset and ".txt" in output_file):
        st.error("❌ Please check all paths and formats.")
    else:
        results = []

        for i in range(1, 247):
            mask_path = os.path.join(mask_dir, f"extracted_region_{i}.nii")
            if os.path.exists(mask_path):
                try:
                    result = subprocess.run(
                        ["3dmaskave", "-quiet", "-mask", mask_path, stats_dset],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True
                    )
                    mean_val = float(result.stdout.strip())
                    results.append((i, mean_val))
                except subprocess.CalledProcessError:
                    results.append((i, np.nan))
            else:
                results.append((i, np.nan))

        df = pd.DataFrame(results, columns=["Region", "MeanValue"])
        df.to_csv(output_file, sep="\t", index=False)
        st.success(f"✅ Extracted values saved to {output_file}")

        # Plot
        boundary_lines = [30, 40, 78, 140, 148, 162, 178, 246]
        region_names = ['Prefrontal', 'Motor', 'Cingulate/Parietal',
                        'Occipital', 'Temp', 'Insula',
                        'Subcort', 'Brainstem & Cerebellum']

        fig, ax = plt.subplots(figsize=(16, 5))
        ax.bar(df["Region"], df["MeanValue"], color=(0.25, 0.88, 0.82), edgecolor='none')

        for i, boundary in enumerate(boundary_lines):
            ax.axvline(x=boundary + 0.5, color='k', linestyle='--', linewidth=1)
            if i == 0:
                x_center = boundary / 2
            else:
                x_center = (boundary_lines[i - 1] + boundary) / 2
            ax.text(x_center, max(df["MeanValue"]) * 1.05, region_names[i],
                    ha='center', fontsize=10, fontweight='bold')

        ax.set_xlabel("Brainnetome Subregion Index")
        ax.set_ylabel("t-stat (Meth vs Neutral)")
        ax.set_title("BNA t-stats: Meth vs Neutral")
        ax.set_ylim([min(df["MeanValue"]) - 0.5, max(df["MeanValue"]) + 1])
        ax.grid(True)
        st.pyplot(fig)
