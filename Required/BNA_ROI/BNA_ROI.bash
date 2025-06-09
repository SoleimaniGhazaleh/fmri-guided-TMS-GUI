#!/bin/bash

# Define the path to the atlas
atlas="/Users/ghazaleh/Documents/Data/FDCR_PretDCS_fine/BNA_ROI/BNA_MPM_thr25_1.25mm-resampled.nii"

# Loop through each region value
for i in {1..246}; do
    echo "Extracting region $i"
    # Use 3dcalc to extract the region
    3dcalc -a $atlas -expr "equals(a,$i)" -prefix "extracted_region_${i}.nii" -datum short
done

echo "Extraction complete."
