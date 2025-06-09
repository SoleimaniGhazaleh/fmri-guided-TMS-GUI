import tkinter as tk
import subprocess
import os
import webbrowser

# Script labels and file names
scripts = {
    "1️⃣ DICOM to BIDS Conversion": "Codes/1_dicom_to_bids_gui.py",
    "2️⃣ fMRI Preprocessing (AFNI)": "Codes/2_afni_preproc_gui.py",
    "3️⃣ Brainnetome Atlas (D vs. N)": "Codes/3_bna_plot_gui_local.py",
    "4️⃣ Activation (D vs. N) MNI Map": "Codes/7_ContrastVisualizatoin.py",
    "5️⃣ Optimized Coordinates in MNI": "Codes/4_coordinates_MNIspace.py",
    "6️⃣ MNI to Subject Transformation": "Codes/6_mni_to_subject_gui.py",
    "7️⃣ Cluster-based Optimization and EF": "Codes/8_EFsimulation.py",
    "⭐ Mesh Generation (SimNIBS) – Time-Intensive Step": "Codes/5_MeshGeneration_SimNIBS.py"

}

def run_app(script_name):
    full_path = os.path.abspath(script_name) if not script_name.startswith("/") else script_name
    subprocess.Popen(["streamlit", "run", full_path])

def open_contact(event):
    webbrowser.open("https://soleimanighazaleh.github.io/")

# GUI setup
root = tk.Tk()
root.title("🧠 fMRI-Guided TMS Pipeline Launcher")
root.geometry("500x550")
root.configure(bg="#1e1e1e")

# Header
tk.Label(root,
         text="🚀 Launch Your fMRI-Guided TMS Workflow",
         font=("Helvetica", 16, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=20)

# Frame for buttons
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

# Create buttons
for label, script in scripts.items():
    tk.Button(frame,
              text=label,
              command=lambda s=script: run_app(s),
              width=50, height=2,
              bg="#f0f0f0", fg="black",
              activebackground="#cccccc",
              activeforeground="black",
              font=("Helvetica", 11, "bold"),
              relief="ridge", bd=2).pack(pady=6)

# Contact link
contact = tk.Label(root,
                   text="🔗 Contact: soleimanighazaleh.github.io",
                   font=("Helvetica", 13, "italic"),
                   bg="#1e1e1e", fg="lightblue", cursor="hand2")
contact.pack(pady=(10, 20))
contact.bind("<Button-1>", open_contact)

root.mainloop()
