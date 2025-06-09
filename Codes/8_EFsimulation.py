import streamlit as st
import os
from simnibs import opt_struct
import subprocess

st.set_page_config(page_title="TMS EF Simulation with SimNIBS", layout="centered")
st.title("⚡ TMS Electric Field Simulation")

# --- Defaults ---
PWD = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED"
default_subject_id = "sub-001"
default_headmodel_path = os.path.join(PWD, "HeadModels", f"m2m_{default_subject_id}", f"{default_subject_id}.msh")
default_coords = "40.2 -52.3 28.0"  # flipped MNI coord example
default_output_dir = os.path.join(PWD, "HeadModels", f"m2m_{default_subject_id}")
default_coil = "/Users/ghazaleh/Applications/SimNIBS-4.0/simnibs_env/lib/python3.9/site-packages/simnibs/resources/coil_models/Drakaki_BrainStim_2022/MagVenture_Cool-B65.ccd"
gmsh_path = "/usr/local/bin/gmsh"  # Path to Gmsh executable

# --- Inputs ---
subject_id = st.text_input("Subject ID (used for naming and locating head model):", default_subject_id)
headmodel_path = st.text_input("Path to SimNIBS .msh head model:", default_headmodel_path)
mni_coords = st.text_input("MNI Coordinate (flipped):", default_coords)
coil_model = st.text_input("Full Path to Coil Model (.ccd):", default_coil)
output_dir = st.text_input("Output Directory:", default_output_dir)

if st.button("⚡ Run TMS EF Simulation"):
    if not os.path.exists(headmodel_path):
        st.error("❌ Head model (.msh) file does not exist.")
    else:
        st.info("Converting MNI → subject coordinates...")
        m2m_path = os.path.join(PWD, "HeadModels", f"m2m_{subject_id}")

        try:
            coords = mni_coords.strip().split()
            if len(coords) != 3:
                raise ValueError("You must enter exactly 3 values for MNI coordinates.")

            result = subprocess.check_output([
                "mni2subject_coords", "-c", *coords, "-m", m2m_path
            ], text=True)

            subject_coords = result.strip().split('[')[-1].split(']')[0].strip()
            st.success(f"✅ Converted coordinates: {subject_coords}")

            # Prepare for EF simulation using simnibs Python API
            st.info("Simulating TMS EF using SimNIBS Python API...")

            # Parse converted coordinate string to float list
            target_coords = [float(val) for val in subject_coords.split()]

            # Clean up previous simulation files if they exist
            for fname in os.listdir(output_dir):
                if fname.startswith("simnibs_simulation") or fname.startswith("TMSopt_TARGET"):
                    os.remove(os.path.join(output_dir, fname))

            opt = opt_struct.TMSoptimize()
            opt.fnamehead = headmodel_path
            opt.pathfem = output_dir
            opt.fnamecoil = coil_model
            opt.target = target_coords
            opt.method = 'ADM'  # Use fast method
            opt.solver_options = ''  # Use default solver (CG+AMG)
            opt.open_in_gmsh = False  # We'll open it manually below

            # Optional tuning
            opt.target_size = 5
            opt.distance = 4
            opt.search_radius = 20
            opt.spatial_resolution = 5
            opt.angle_resolution = 30
            opt.search_angle = 360

            opt.run()

            ef_map = os.path.join(output_dir, "TMSopt_TARGET.nii.gz")
            coil_info = os.path.join(output_dir, "TMSopt_TARGET.TMSopt.txt")
            gmsh_file = os.path.join(output_dir, f"{subject_id}_TMS_optimize_MagVenture_Cool-B65.msh")

            st.success("✅ EF simulation complete!")
            st.write("### Outputs:")
            st.write(f"🧠 EF map: `{ef_map}`")
            st.write(f"📄 Coil info: `{coil_info}`")

            if os.path.exists(coil_info):
                with open(coil_info) as f:
                    st.text(f.read())

            # --- Open Gmsh with the optimized coil mesh ---
            if os.path.exists(gmsh_file):
                st.info("🟢 Opening Gmsh to display the optimized coil placement mesh...")
                subprocess.Popen([gmsh_path, gmsh_file])
            else:
                st.warning("⚠️ Gmsh mesh file not found. It may not have been generated.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
