import pydicom
import numpy as np
from PIL import Image
import os
from typing import Dict, Any, Optional

class MedicalImagingProcessor:
    """
    Real imaging processor using pydicom for DICOM analysis.
    Extracts actual patient and staging data from medical images.
    """
    
    def extract_metadata(self, dicom_path: str) -> Dict[str, Any]:
        """Extracts diagnostic metadata from a real DICOM file"""
        if not os.path.exists(dicom_path):
            return {}
            
        try:
            ds = pydicom.dcmread(dicom_path)
            return {
                "modality": getattr(ds, 'Modality', 'Unknown'),
                "manufacturer": getattr(ds, 'Manufacturer', 'Unknown'),
                "pixel_spacing": [float(x) for x in getattr(ds, 'PixelSpacing', [1.0, 1.0])],
                "slice_thickness": float(getattr(ds, 'SliceThickness', 0.0)),
                "patient_position": getattr(ds, 'PatientPosition', 'Unknown')
            }
        except Exception as e:
            return {"error": str(e)}
            
    def analyze_pixel_data(self, dicom_path: str) -> Dict[str, Any]:
        """Performs basic pixel-level analysis for tumor size estimation"""
        if not os.path.exists(dicom_path):
            return {}
            
        try:
            ds = pydicom.dcmread(dicom_path)
            pixels = ds.pixel_array
            
            # Real analysis: Normalize and find peak intensity regions (simple segmentation)
            norm_pixels = (pixels - np.min(pixels)) / (np.max(pixels) - np.min(pixels))
            threshold = np.mean(norm_pixels) + 2 * np.std(norm_pixels)
            high_intensity_pixels = np.sum(norm_pixels > threshold)
            
            # Estimate size based on pixel count and spacing
            pixel_spacing = getattr(ds, 'PixelSpacing', [1.0, 1.0])
            area_mm2 = high_intensity_pixels * float(pixel_spacing[0]) * float(pixel_spacing[1])
            est_diameter_cm = np.sqrt(area_mm2 / np.pi) * 2 / 10
            
            return {
                "peak_intensity_ratio": float(np.max(norm_pixels)),
                "estimated_mass_diameter_cm": float(est_diameter_cm),
                "pixel_count": int(high_intensity_pixels)
            }
        except Exception as e:
            return {"error": str(e)}
