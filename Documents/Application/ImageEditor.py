import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageTk
import numpy as np

class ParameterUpdater:
    def generate_parameters(self):
        return [-66, 6.6, -50, -100, 50, 15, 80, 0, -50, 100, 0, 0, 10]
    def update_parameters(self,instruction):
        return [-36, 6.6, -50, -100, 50, 15, 80, 0, -50, 50, 0, 0, 30]



class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.parameter_updater = ParameterUpdater()
        self.image = None  # Current image being manipulated
        self.original_image = None  # Store the original image for reset
        self.photo_image = None
        self.first_instruction_applied = False  # Flag for first instruction

        # Load Image Button
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        # Instruction Label
        self.instruction_label = tk.Label(root, text="Enter filter description:")
        self.instruction_label.pack(side=tk.LEFT)

        # Instruction Entry
        self.instruction_entry = tk.Entry(root)
        self.instruction_entry.bind("<Return>", self.apply_filter)
        self.instruction_entry.pack(side=tk.LEFT)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_parameters)
        self.reset_button.pack()

        # Image Display Label
        self.image_label = tk.Label(root)
        self.image_label.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.original_image = self.image.copy()  # Save the original image
            self.show_image(self.image)

    def show_image(self, img):
        img.thumbnail((1000, 1000))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def apply_filter(self, event=None):
        if self.image:
            instruction = self.instruction_entry.get().strip()  # Get the instruction and strip whitespace

            if instruction:  # Check if the instruction is not empty
                messagebox.showinfo("Loading", "Applying filter, please wait...")
                if not self.first_instruction_applied:  # First application
                    params = self.parameter_updater.generate_parameters()  # Generate initial parameters
                    self.adjust_image(params)
                    messagebox.showinfo("Done", "Filter applied successfully!You can further adjust it ." )
                    self.first_instruction_applied = True  # Set flag for first instruction
                else:  # Subsequent applications
                    params = self.parameter_updater.update_parameters(instruction)  # Update parameters based on new instruction
                    self.adjust_image(params)
                    messagebox.showinfo("Done", "Updated successfully!")

                self.instruction_entry.delete(0, tk.END)  # Clear the entry box after applying the filter
               
            else:
                messagebox.showwarning("Input Error", "Please enter a valid instruction.")

    def adjust_image(self, params):
        if self.image:
            brightness = params[0] / 100 + 1
            exposure = params[1] + 1
            vibrance = params[2] / 10 + 1
            highlights = params[3] / 10.0
            shadows = params[4] / 5
            contrast = params[5] / 500 + 1
            saturation = params[6] / 100 + 1
            natural_saturation = params[7] / 10.0 + 1
            color_temperature = params[8] / 10
            tint = params[9] / 10
            black_spot = params[10]
            clarity = params[12] / 30.0

            # Adjust the image using the parameters
            enhancer = ImageEnhance.Brightness(self.image)
            img = enhancer.enhance(brightness)
            img = enhancer.enhance(1 + exposure / 100.0)  # Scale exposure adjustment
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1 + vibrance / 100.0)
            img = enhancer.enhance(saturation)
            img = enhancer.enhance(1 + natural_saturation / 100.0)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
            enhancer = ImageEnhance.Color(img)
            img = self.adjust_temperature_tint(img, color_temperature, tint)
            img = self.adjust_highlights_shadows(img, highlights, shadows)
            img = self.desaturate_blacks(img, black_spot)
            img = ImageEnhance.Sharpness(img).enhance(clarity)

            self.image = img  # Update the current image
            self.show_image(img)

    def reset_parameters(self):
        if self.original_image:
            self.image = self.original_image.copy()  # Restore the original image
            self.first_instruction_applied = False  # Reset the application state
            self.show_image(self.image)  # Display the original image
            self.instruction_entry.delete(0, tk.END)  # Clear instruction entry
            messagebox.showinfo("Reset", "Image and parameters have been reset!")
        else:
            messagebox.showwarning("Reset Error", "No image loaded to reset!")

    def adjust_highlights_shadows(self, img, highlights, shadows):
        img_np = np.array(img).astype(np.float32)
        highlight_mask = img_np > 128
        shadow_mask = img_np <= 128

        # Brighten highlights using a smoother approach
        img_np[highlight_mask] = np.clip(img_np[highlight_mask] + (highlights * (img_np[highlight_mask] / 255)), 0, 255)

        # Brighten shadows using a smoother approach
        img_np[shadow_mask] = np.clip(img_np[shadow_mask] + (shadows * (1 - img_np[shadow_mask] / 255)), 0, 255)

        return Image.fromarray(img_np.astype(np.uint8))

    def desaturate_blacks(self, img, desaturation_amount, threshold=30):
        img_np = np.array(img)
        black_pixels = np.where(np.all(img_np <= threshold, axis=-1))

        for i in range(len(black_pixels[0])):
            row = black_pixels[0][i]
            col = black_pixels[1][i]
            avg = np.mean(img_np[row, col])
            img_np[row, col] = [
                int(val - (val - avg) * desaturation_amount / 100)
                for val in img_np[row, col]
            ]

        return Image.fromarray(img_np)

    def adjust_temperature_tint(self, img, temperature, tint):
        img_np = np.array(img).astype(np.int32)

        img_np[:, :, 2] = np.clip(img_np[:, :, 2] - temperature, 0, 255)
        img_np[:, :, 0] = np.clip(img_np[:, :, 0] + temperature, 0, 255)
        img_np[:, :, 1] = np.clip(img_np[:, :, 1] - tint, 0, 255)
        img_np[:, :, 2] = np.clip(img_np[:, :, 2] + tint, 0, 255)

        return Image.fromarray(img_np.astype(np.uint8))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()