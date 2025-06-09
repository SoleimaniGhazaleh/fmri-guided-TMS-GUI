import streamlit as st
import os
import subprocess
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from nilearn.plotting import plot_stat_map
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize

st.set_page_config(page_title="AFNI Sub-brick Viewer", layout="centered")
st.title("🧠 Visualize AFNI Sub-brick in MNI Space")

# Base directory
PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"
def_sample = os.path.join(PWD, "Preprocess", "sub-001-ses-01_SB", "sub-001-ses-01_SB.results", "stats.sub-001-ses-01_SB+tlrc.BRIK")

default_mask = os.path.join(PWD, "Required", "MNI_brainmask-resampled.nii")
default_resampled_mask = os.path.join(PWD, "Required", "MNI_brainmask-resampled_rs.nii")

# --- User Inputs ---
stats_brik_path = st.text_input("📂 Full path to AFNI stats dataset (.BRIK file):", value=def_sample)
subbrick_index = st.number_input("🔢 Sub-brick index to visualize:", min_value=0, max_value=100, value=33)

# --- Run and visualize ---
if st.button("📊 Run and Visualize"):
    if not os.path.exists(stats_brik_path):
        st.error(f"❌ The input stats dataset does not exist: {stats_brik_path}")
    else:
        try:
            results_dir = os.path.dirname(stats_brik_path)
            prefix = os.path.basename(stats_brik_path).split('+')[0] + "_MNI"
            mni_output_path = os.path.join(results_dir, f"{prefix}.nii")

            with st.spinner("Resampling mask and generating MNI-aligned image..."):
                subprocess.run([
                    "3dresample", "-master", stats_brik_path,
                    "-input", default_mask,
                    "-prefix", default_resampled_mask,
                    "-overwrite"
                    ], check=True)


                subprocess.run([
                    "3dcalc",
                    "-a", stats_brik_path,
                    "-b", default_resampled_mask,
                    "-expr", "a*b",
                    "-prefix", mni_output_path
                ], check=True)

            # --- Visualization ---
            img_4d = nib.load(mni_output_path)
            img_3d_data = img_4d.slicer[..., subbrick_index]
            img_3d = nib.Nifti1Image(img_3d_data.get_fdata(), affine=img_4d.affine)

            colors_neg = ["darkblue", "blue", "lightblue"]
            colors_pos = ["yellow", "orange", "red"]
            afni_cmap = LinearSegmentedColormap.from_list("afni_diverging", colors_neg + colors_pos, N=256)

            z_slices = list(range(-30, 60, 6))
            n_cols = 5
            n_rows = int(np.ceil(len(z_slices) / n_cols))

            fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(15, 3 * n_rows))
            axes = axes.flatten()

            for i, z in enumerate(z_slices):
                plot_stat_map(
                    img_3d,
                    threshold=0.05,
                    vmin=-0.6, vmax=0.6,
                    cmap=afni_cmap,
                    display_mode='z',
                    cut_coords=[z],
                    axes=axes[i],
                    colorbar=False,
                    annotate=False
                )
                axes[i].set_title(f'z = {z}')

            for j in range(i + 1, len(axes)):
                axes[j].axis('off')

            cbar_ax = fig.add_axes([0.92, 0.2, 0.02, 0.6])
            norm = Normalize(vmin=-0.6, vmax=0.6)
            cb = ColorbarBase(cbar_ax, cmap=afni_cmap, norm=norm)
            cb.set_label(f'Stat value (sub-brick #{subbrick_index})', fontsize=12)

            plt.suptitle(f"Montage with Shared Colorbar – Sub-brick #{subbrick_index}", fontsize=16)
            plt.tight_layout(rect=[0, 0.03, 0.9, 0.95])
            st.pyplot(fig)

        except subprocess.CalledProcessError as e:
            st.error(f"❌ AFNI command failed: {e}")
        except Exception as e:
            st.error(f"⚠️ Error during visualization: {e}")
