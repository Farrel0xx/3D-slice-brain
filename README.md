cat << 'EOF' > README.md
# DICOM Dual-Series Viewer

A lightweight Python-based medical imaging tool designed for side-by-side comparison of DICOM series, optimized for tumor segmentation analysis.

## 🚀 Features
* **Dual-View Interface**: Display `SE000001` (Left) and `SE000002` (Right) simultaneously.
* **Anatomical Sorting**: Automatically sorts slices by `SliceLocation` for correct spatial orientation.
* **Auto-Normalization**: Applied 1st-99th percentile contrast stretching for enhanced tumor visibility.
* **Independent Controls**: Scroll through each series independently via mouse wheel or dedicated sliders.

## 🛠️ Prerequisites
\`\`\`bash
pip install pydicom numpy matplotlib
\`\`\`

## 📂 Project Structure
The script expects the following directory layout:
\`\`\`text
ST000001/
├── SE000001/  # Primary Series (Left)
└── SE000002/  # Secondary/Segmented Series (Right)
\`\`\`

## ⌨️ Controls
| Input | Action |
| :--- | :--- |
| **Mouse Wheel** | Scroll slices (hover over specific pane) |
| **A / D Keys** | Previous/Next slice (Left Pane) |
| **W / S Keys** | Previous/Next slice (Right Pane) |
| **Sliders** | Direct slice seeking |

## 🔧 Quick Start
1. Clone the repository.
2. Update the \`main_folder\` path in the script to your local data directory.
3. Run the application:
   \`\`\`bash
   python viewer.py
   \`\`\`

## ⚖️ License
MIT License. Free to use and modify for medical research and development.
EOF
