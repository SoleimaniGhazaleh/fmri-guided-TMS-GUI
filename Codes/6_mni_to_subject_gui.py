import streamlit as st
import subprocess
import os

st.set_page_config(page_title="MNI to Subject Coordinate Converter", layout="centered")
st.title("🧭 MNI → Subject Coordinate Converter")

# Default example m2m path and coordinates
default_m2m_path = "/Volumes/ExtremeSSD2/LNPI_AUTOMATED/HeadModels/m2m_sub-001"
default_coords = "-40 50 30\n-45 30 40\n-38 42 32\n-46 36 28"

# Inputs
m2m_path = st.text_input("📁 Path to m2m Subject Folder", default_m2m_path)
coords_text = st.text_area("🧠 Enter MNI Coordinates (one per line, space-separated)", default_coords, height=150)

if st.button("🔄 Convert to Subject Space"):
    if not os.path.isdir(m2m_path):
        st.error("❌ Invalid m2m folder path.")
    elif not coords_text.strip():
        st.error("❌ Please enter at least one coordinate.")
    else:
        st.info("Running transformation...")
        coords_lines = [line.strip() for line in coords_text.strip().split("\n") if line.strip()]
        results = []

        for idx, coord in enumerate(coords_lines, start=1):
            try:
                result = subprocess.check_output(["mni2subject_coords", "-c"] + coord.split() + ["-m", m2m_path], text=True)
                transformed = result.strip().split('[')[-1].split(']')[0]  # Extract coordinates inside []
                results.append((f"Target_{idx}", transformed))
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error converting coordinate {coord}: {e}")

        if results:
            st.success("✅ Conversion complete. See below:")
            for label, coords in results:
                st.write(f"{label}: {coords}")
