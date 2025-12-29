import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ======================
# CONFIGURATION
# ======================
main_folder = '/home/ghost00/segmentation_tumor/ST000001/'

def load_series_by_name(folder_name):
    path = os.path.join(main_folder, folder_name)
    if not os.path.exists(path):
        print(f"⚠️ Folder {folder_name} tidak ditemukan!")
        return []
    
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    slices = []
    for f in files:
        try:
            ds = pydicom.dcmread(f)
            # Ambil InstanceNumber atau SliceLocation untuk pengurutan anatomi
            z_pos = ds.SliceLocation if hasattr(ds, 'SliceLocation') else (ds.InstanceNumber if hasattr(ds, 'InstanceNumber') else 0)
            slices.append((z_pos, ds.pixel_array))
        except:
            continue
    
    # Urutkan berdasarkan posisi anatomi (Z-axis)
    slices.sort(key=lambda x: x[0])
    
    # Normalisasi kontras (Leveling)
    processed = []
    for _, img in slices:
        # Teknik Clip 1-99 percentile untuk menghilangkan noise outlier
        low, high = np.percentile(img, (1, 99))
        img_norm = np.clip(img, low, high)
        img_norm = (img_norm - img_norm.min()) / (img_norm.max() - img_norm.min() + 1e-6)
        processed.append(img_norm)
    return processed

# ======================
# DATA LOADING
# ======================
print("🔄 Loading Data...")

# Memastikan SE000001 di kiri dan SE000002 di kanan
left_images = load_series_by_name('SE000001')
right_images = load_series_by_name('SE000003')

if not left_images or not right_images:
    print("❌ Error: Salah satu atau kedua folder (SE000001/SE000002) kosong atau tidak ada.")
    exit()

print(f"✅ Terload: Kiri ({len(left_images)} Slices) | Kanan ({len(right_images)} Slices)")

# ======================
# VISUALIZATION
# ======================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))
fig.canvas.manager.set_window_title('Tumor Segmentation Viewer - SE01 vs SE02')
fig.patch.set_facecolor('#0f172a') # Dark theme

# Initial indices
idx1 = len(left_images) // 2
idx2 = len(right_images) // 2

im1 = ax1.imshow(left_images[idx1], cmap='gray')
im2 = ax2.imshow(right_images[idx2], cmap='gray')

for ax, title in zip([ax1, ax2], ['SERIES 01 (LEFT)', 'SERIES 02 (RIGHT)']):
    ax.axis('off')
    ax.set_title(title, color='#38bdf8', fontsize=12, fontweight='bold')

# Info text overlay
info1 = ax1.text(0.02, 0.02, f'Slice: {idx1+1}', transform=ax1.transAxes, color='yellow')
info2 = ax2.text(0.02, 0.02, f'Slice: {idx2+1}', transform=ax2.transAxes, color='yellow')

# Sliders
ax_slid1 = plt.axes([0.15, 0.05, 0.3, 0.03], facecolor='#1e293b')
ax_slid2 = plt.axes([0.55, 0.05, 0.3, 0.03], facecolor='#1e293b')

slider1 = Slider(ax_slid1, 'S1 ', 0, len(left_images)-1, valinit=idx1, valstep=1, color='#38bdf8')
slider2 = Slider(ax_slid2, 'S2 ', 0, len(right_images)-1, valinit=idx2, valstep=1, color='#38bdf8')

def update(val):
    i1 = int(slider1.val)
    i2 = int(slider2.val)
    im1.set_data(left_images[i1])
    im2.set_data(right_images[i2])
    info1.set_text(f'Slice: {i1+1}/{len(left_images)}')
    info2.set_text(f'Slice: {i2+1}/{len(right_images)}')
    fig.canvas.draw_idle()

slider1.on_changed(update)
slider2.on_changed(update)

# Scroll Interaction
def on_scroll(event):
    if event.inaxes == ax1:
        new_val = np.clip(slider1.val + (1 if event.button == 'up' else -1), 0, len(left_images)-1)
        slider1.set_val(new_val)
    elif event.inaxes == ax2:
        new_val = np.clip(slider2.val + (1 if event.button == 'up' else -1), 0, len(right_images)-1)
        slider2.set_val(new_val)

fig.canvas.mpl_connect('scroll_event', on_scroll)

plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.show()
