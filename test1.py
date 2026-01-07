import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk
import io

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Background Removal System")
        self.root.geometry("600x600")

        self.input_image = None
        self.output_image = None

        # Upload Button
        self.upload_btn = tk.Button(
            root, text="Upload Image", font=("Arial", 14),
            command=self.upload_image
        )
        self.upload_btn.pack(pady=20)

        # Image Display Area
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Process Button
        self.process_btn = tk.Button(
            root, text="Remove Background", font=("Arial", 14),
            command=self.process_image, state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)

        # Save Button
        self.save_btn = tk.Button(
            root, text="Download Image", font=("Arial", 14),
            command=self.save_image, state=tk.DISABLED
        )
        self.save_btn.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.*")]
        )

        if not file_path:
            return

        self.input_image = Image.open(file_path)

        display_img = self.input_image.resize((300, 300))
        display_img = ImageTk.PhotoImage(display_img)

        self.image_label.config(image=display_img)
        self.image_label.image = display_img

        self.process_btn.config(state=tk.NORMAL)

    def process_image(self):
        try:
            output = remove(self.input_image)

            if isinstance(output, (bytes, bytearray)):
                self.output_image = Image.open(io.BytesIO(output)).convert("RGBA")
            else:
                self.output_image = output

            display_img = self.output_image.resize((300, 300))
            display_img = ImageTk.PhotoImage(display_img)

            self.image_label.config(image=display_img)
            self.image_label.image = display_img

            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )

        if save_path:
            self.output_image.save(save_path)
            messagebox.showinfo("Success", "Image downloaded successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
