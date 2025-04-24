import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# === Configuration ===
BASE_DIR = "gui_images"
METHODS = ["RISE", "LIME", "GRADCAM"]
LABELS = ["real", "ai_generated"]
IMAGE_RANGE = [str(i) for i in range(1, 11)]
IMAGE_DISPLAY_SIZE = (600, 600)  # Big image size

def load_image(path, size=IMAGE_DISPLAY_SIZE):
    try:
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

# === Main GUI Class ===
class XAIViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("XAI Visualization Viewer")
        self.root.state('zoomed')  # Fullscreen mode (for Windows/macOS)
        self.root.configure(background="white")

        # === Dropdown row ===
        top_frame = tk.Frame(root, bg="white")
        top_frame.pack(pady=10)

        ttk.Label(top_frame, text="Choose class:").grid(row=0, column=0, padx=10)
        self.label_var = tk.StringVar(value="real")
        self.label_dropdown = ttk.Combobox(top_frame, textvariable=self.label_var, values=LABELS, state="readonly", width=15)
        self.label_dropdown.grid(row=0, column=1, padx=10)

        ttk.Label(top_frame, text="Choose image (1–10):").grid(row=0, column=2, padx=10)
        self.image_var = tk.StringVar(value="1")
        self.image_dropdown = ttk.Combobox(top_frame, textvariable=self.image_var, values=IMAGE_RANGE, state="readonly", width=10)
        self.image_dropdown.grid(row=0, column=3, padx=10)

        ttk.Button(top_frame, text="Load Explanations", command=self.load_visualizations).grid(row=0, column=4, padx=20)

        # === Image frames ===
        self.image_frame = tk.Frame(root, bg="white")
        self.image_frame.pack(pady=15)

        self.image_panels = []
        self.pred_labels = []

        for i in range(3):
            subframe = tk.Frame(self.image_frame, bg="white")
            canvas = tk.Label(subframe, bg="white")
            canvas.pack()
            label = tk.Label(subframe, text="", font=("Helvetica", 14), bg="white")
            label.pack(pady=5)
            subframe.grid(row=0, column=i, padx=15)
            self.image_panels.append(canvas)
            self.pred_labels.append(label)

    def load_visualizations(self):
        label = self.label_var.get()
        img_id = self.image_var.get()

        titles = ["Original Image", "CNN + RISE", "CLIP + RISE"]
        # Original image (copied from CNN RISE input)
        original_path = os.path.join(BASE_DIR, "RISE", label, f"img{img_id}.png")
        original_img = load_image(original_path)

        for i, method in enumerate(METHODS):
            path = os.path.join(BASE_DIR, method, label, f"img{img_id}.png")

            if i == 0:  # Original image left
                img = original_img
            else:
                img = load_image(path)

            if img:
                self.image_panels[i].configure(image=img)
                self.image_panels[i].image = img
                self.pred_labels[i].configure(text=f"{titles[i]} (img{img_id})")
            else:
                self.image_panels[i].configure(image="")
                self.pred_labels[i].configure(text=f"{titles[i]} not found")

# === Launch the app ===
if __name__ == "__main__":
    root = tk.Tk()
    app = XAIViewer(root)
    root.mainloop()
