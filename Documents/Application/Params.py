import tkinter as tk
from tkinter import messagebox
import numpy as np

# Default Parameters Generator
def generate_default_parameters():
    # Generate default parameters (e.g., random values or fixed values within a range)
    default_params = np.random.randint(-10, 11, size=13)  # 13 parameters in range [-10, 10]
    return default_params

# Interpret instruction and update parameters
def interpret_instruction(instruction):
    instruction = instruction.lower()
    # Basic action map for interpreting instructions
    action_map = {
        "brighter": {"parameter": "brightness", "change": 10},
        "darker": {"parameter": "brightness", "change": -10},
        "increase brightness": {"parameter": "brightness", "change": 10},
        "decrease brightness": {"parameter": "brightness", "change": -10},
        # Add additional mappings as needed
    }

    # Match instruction with action map
    for key in action_map:
        if key in instruction:
            return action_map[key]["parameter"], action_map[key]["change"]
    
    return None, 0

# Update parameters based on instruction
def update_parameters(current_params, instruction):
    param_to_index = {
        'brightness': 0,
        'exposure': 1,
        'vibrance': 2,
        'highlights': 3,
        'shadows': 4,
        'contrast': 5,
        'saturation': 6,
        'natural_saturation': 7,
        'color_temperature': 8,
        'tint': 9,
        'black_point': 10,
        'vignette': 11,
        'clarity': 12
    }
    
    param, change = interpret_instruction(instruction)
    if param and param in param_to_index:
        current_params[param_to_index[param]] += change
        current_params = np.clip(current_params, -10, 10)  # Clamp values to [-10, 10]
    else:
        # If instruction is unclear, keep parameters unchanged
        messagebox.showwarning("Warning", "Instruction not recognized. No changes made.")
    
    return current_params

# Main function
def main():
    root = tk.Tk()
    root.title("Parameter Update Interface")
    root.geometry("400x300")  # Set default window size
    root.resizable(True, True)  # Allow resizing

    # UI Elements
    sentence_label = tk.Label(root, text="Enter a sentence:")
    sentence_label.pack(pady=5)

    sentence_entry = tk.Entry(root, width=50)
    sentence_entry.pack(pady=5)

    instruction_label = tk.Label(root, text="Enter further instructions:")
    instruction_label.pack(pady=5)

    instruction_entry = tk.Entry(root, width=50)
    instruction_entry.pack(pady=5)

    current_params = None  # To store the current parameters

    # Function to handle initial sentence input
    def handle_sentence():
        nonlocal current_params
        sentence = sentence_entry.get().strip()
        if not sentence:
            messagebox.showwarning("Warning", "Please enter a valid sentence.")
            return
        # Generate default parameters
        current_params = generate_default_parameters()
        messagebox.showinfo("Generated Parameters", f"{current_params.tolist()}")

    # Function to handle parameter updates based on instructions
    def handle_update():
        nonlocal current_params
        if current_params is not None:
            instruction = instruction_entry.get().strip()
            if not instruction:
                messagebox.showwarning("Warning", "Please enter a valid instruction.")
                return
            updated_params = update_parameters(current_params.copy(), instruction)
            messagebox.showinfo("Updated Parameters", f"{updated_params.tolist()}")
            current_params = updated_params  # Update the current parameters
        else:
            messagebox.showwarning("Warning", "Please generate parameters first.")

    # Buttons
    generate_button = tk.Button(root, text="Generate Parameters", command=handle_sentence)
    generate_button.pack(pady=5)

    update_button = tk.Button(root, text="Update Parameters", command=handle_update)
    update_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()