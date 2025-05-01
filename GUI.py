import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# === Configuration ===
BASE_DIR = "gui_images"
METHODS = ["RISE", "LIME", "GRADCAM"]
LABELS = ["real", "ai_generated"]
IMAGE_IDS = [str(i) for i in range(1, 11)]
IMG_SIZE = (750, 750)
METHOD_SIZES = {
    
    "RISE": (550, 160),
    "LIME": (550, 160),
    "GRADCAM": (380, 160),
}

# Image loader
def load_image(path, size=IMG_SIZE):
    try:
        img = Image.open(path).resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# GUI class
class XAIViewerStacked:
    def __init__(self, root):
        self.root = root
        self.root.title("XAI Visualization Viewer")
        self.root.state('zoomed')
        self.root.configure(bg="white")

        # === Main layout ===
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, anchor='n')

        # === Top selection menu ===
        top_frame = tk.Frame(main_frame, bg="white")
        top_frame.pack(pady=2, anchor='n')  # ↓ Reduced padding here

        ttk.Label(top_frame, text="Choose class:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        self.label_var = tk.StringVar(value="real")
        class_dropdown = ttk.Combobox(top_frame, textvariable=self.label_var, values=LABELS, state="readonly", width=15)
        class_dropdown.grid(row=0, column=1)
        self.label_var.trace_add("write", lambda *args: self.load_visualizations())

        ttk.Label(top_frame, text="Choose image (1–10):", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)
        self.image_var = tk.StringVar(value="1")
        image_dropdown = ttk.Combobox(top_frame, textvariable=self.image_var, values=IMAGE_IDS, state="readonly", width=15)
        image_dropdown.grid(row=0, column=3)
        self.image_var.trace_add("write", lambda *args: self.load_visualizations())

        # === Content layout ===
        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=0)

        # === Left and Right Panels for text ===
        self.left_text = tk.Text(content_frame, width=30, height=40, wrap="word", font=("Arial", 10))
        self.left_text.insert(tk.END, "Color Interpretation:\n\n- Red: High relevance\n- Yellow: Medium relevance\n- Blue: Low relevance\n- Transparent: No effect")
        self.left_text.config(state="disabled")
        self.left_text.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        self.right_text = tk.Text(content_frame, width=40, height=40, wrap="word", font=("Arial", 10))
        self.right_text.insert(tk.END, "Model Predictions will appear here.")
        self.right_text.config(state="disabled")
        self.right_text.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.Y)

        # === Image Display Area ===
        self.center_frame = tk.Frame(content_frame, bg="white")
        self.center_frame.pack(side=tk.LEFT, expand=True, pady=5, anchor='n')

        self.image_panels = []
        self.label_panels = []

        for method in ["Original"] + METHODS:
            frame = tk.Frame(self.center_frame, bg="white")
            text_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), bg="white")
            text_label.pack(pady=1)
            img_label = tk.Label(frame, bg="white")
            img_label.pack()
            frame.pack(pady=5)

            self.label_panels.append(text_label)
            self.image_panels.append(img_label)



    def load_visualizations(self):
        label = self.label_var.get()
        img_id = self.image_var.get()
        filename = f"img{img_id}.png"

        # Load other methods
        for i, method in enumerate(["Original"] + METHODS):
            path = os.path.join(BASE_DIR, method, label, filename)
            size = METHOD_SIZES.get(method, IMG_SIZE)
            img = load_image(path, size=size)
            if img:
                self.label_panels[i].configure(text=f"{method} Explanation" if method != "Original" else "Original Image")
                self.image_panels[i].configure(image=img)
                self.image_panels[i].image = img
            else:
                self.image_panels[i].configure(image="")
                self.label_panels[i].configure(text=f"{method} not found for img{img_id}")


# === Run ===
if __name__ == "__main__":
    root = tk.Tk()
    app = XAIViewerStacked(root)
    root.mainloop()
