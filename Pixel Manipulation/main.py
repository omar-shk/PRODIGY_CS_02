import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np

# Initialize the main window
window = tk.Tk()
window.geometry("1400x800+100+100") 
window.title("Image Encryption & Decryption")

# Global variables
global image_encrypted, key, dark_mode
panelA = None
panelB = None
filename = None
image_encrypted = None
key = None
dark_mode = False

# Toggle between light and dark modes
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        window.config(bg="#1e1e1e")  # Dark background for the window
        title_frame.config(bg="#333333")  # Dark background for title frame
        top_frame.config(bg="#2e2e2e")  # Dark background for top frame
        button_frame.config(bg="#2e2e2e")  # Dark background for button frame
        set_widgets_dark_mode()  # Apply dark mode styles to widgets
    else:
        window.config(bg="#ffffff")  # Light background for the window
        title_frame.config(bg="#4B0082")  # Light background for title frame
        top_frame.config(bg="#E6E6FA")  # Light background for top frame
        button_frame.config(bg="#E6E6FA")  # Light background for button frame
        set_widgets_light_mode()  # Apply light mode styles to widgets

# Set widget colors for dark mode
def set_widgets_dark_mode():
    btn_color = "#4C4C4C"  # Dark button color
    text_color = "#FFFFFF"  # White text color
    for widget in window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg=btn_color, fg=text_color)  # Update button color
        elif isinstance(widget, tk.Label):
            widget.config(bg=widget.master.cget('bg'), fg=text_color)  # Update label color
    window.update_idletasks()

# Set widget colors for light mode
def set_widgets_light_mode():
    btn_color = "#FF6347"  # Light button color
    text_color = "#000000"  # Black text color
    for widget in window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg=btn_color, fg=text_color)  # Update button color
        elif isinstance(widget, tk.Label):
            widget.config(bg=widget.master.cget('bg'), fg=text_color)  # Update label color
    window.update_idletasks()

# Extract directory path from a file path
def getpath(path):
    return '/'.join(path.split('/')[:-1]) + '/'

# Extract file name without extension from a file path
def getfilename(path):
    return path.split('/')[-1].split('.')[0]

# Open a file dialog to select an image file
def openfilename():
    return filedialog.askopenfilename(title='Open', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

# Resize image to fit within specified dimensions
def resize_image(image, max_width, max_height):
    img_width, img_height = image.size
    if img_width > max_width or img_height > max_height:
        aspect_ratio = img_width / img_height
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)
    return image

# Load and display the selected image
def open_img():
    global panelA, panelB, filename
    filename = openfilename()
    if filename:
        img = Image.open(filename)
        img = resize_image(img, 600, 700)  # Resize image to fit within the specified dimensions
        img_tk = ImageTk.PhotoImage(img)
        if panelA is None or panelB is None:
            panelA = tk.Label(image=img_tk, bg=window.cget('bg'))
            panelA.image = img_tk
            panelA.pack(side="left", padx=20, pady=20, fill="both", expand=True)
            panelB = tk.Label(image=img_tk, bg=window.cget('bg'))
            panelB.image = img_tk
            panelB.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        else:
            panelA.configure(image=img_tk)
            panelB.configure(image=img_tk)
            panelA.image = img_tk
            panelB.image = img_tk
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Encrypt the selected image
def en_fun(x):
    global image_encrypted, key
    image_input = cv2.imread(x)
    if image_input is not None:
        (x1, y, z) = image_input.shape
        image_input = image_input.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, (x1, y, z)) + np.finfo(float).eps
        image_encrypted = image_input / key
        cv2.imwrite('image_encrypted.jpg', (image_encrypted * 255).astype(np.uint8))
        imge = Image.open('image_encrypted.jpg')
        imge = resize_image(imge, 600, 700)  # Resize image to fit within the specified dimensions
        imge = ImageTk.PhotoImage(imge)
        panelB.configure(image=imge)
        panelB.image = imge
        messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")
    else:
        messagebox.showwarning("Warning", "Failed to read image.")

# Decrypt the encrypted image
def de_fun():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output = (image_output * 255.0).astype(np.uint8)
        cv2.imwrite('image_output.jpg', image_output)
        imgd = Image.open('image_output.jpg')
        imgd = resize_image(imgd, 600, 700)  # Resize image to fit within the specified dimensions
        imgd = ImageTk.PhotoImage(imgd)
        panelB.configure(image=imgd)
        panelB.image = imgd
        messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
    else:
        messagebox.showwarning("Warning", "Image not encrypted yet.")

# Reset the image to the original
def reset():
    global panelB, filename
    if filename:
        original_image = Image.open(filename)
        image = resize_image(original_image, 600, 700)  # Resize image to fit within the specified dimensions
        image = ImageTk.PhotoImage(image)
        panelB.configure(image=image)
        panelB.image = image
        messagebox.showinfo("Success", "Image reset to original format!")
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Download the encrypted image
def download_encrypted():
    global image_encrypted
    if image_encrypted is not None:
        saved_filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if saved_filename:
            cv2.imwrite(saved_filename, (image_encrypted * 255).astype(np.uint8))
            messagebox.showinfo("Success", "Encrypted Image Downloaded Successfully!")
    else:
        messagebox.showwarning("Warning", "No encrypted image to download.")

# Download the decrypted image
def download_decrypted():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output = (image_output * 255.0).astype(np.uint8)
        saved_filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if saved_filename:
            cv2.imwrite(saved_filename, image_output)
            messagebox.showinfo("Success", "Decrypted Image Downloaded Successfully!")
    else:
        messagebox.showwarning("Warning", "No decrypted image to download.")

# Confirm exit and close the window
def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Title Label
title_frame = tk.Frame(window, bg="#4B0082")
title_frame.pack(fill="x", pady=20)

tk.Label(title_frame, text="🔒 Image Encryption & Decryption 🔓", font=("Arial", 40, 'bold'), fg="white", bg="#4B0082").pack()

# Frames for buttons and top section
top_frame = tk.Frame(window, bg="#E6E6FA", padx=20, pady=10)
top_frame.pack(fill="x")

button_frame = tk.Frame(window, bg="#E6E6FA", padx=20, pady=10)
button_frame.pack(fill="x", pady=10)

# Buttons for functionality
tk.Button(top_frame, text="📂 Open Image", command=open_img, font=("Arial", 18), bg="#FFA07A", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)
tk.Button(top_frame, text="🔒 Encrypt", command=lambda: en_fun(filename), font=("Arial", 18), bg="#90EE90", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)
tk.Button(top_frame, text="🔓 Decrypt", command=de_fun, font=("Arial", 18), bg="#FFA07A", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)
tk.Button(top_frame, text="🔄 Reset", command=reset, font=("Arial", 18), bg="#FFD700", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)

tk.Button(button_frame, text="⬇️ Download Encrypted", command=download_encrypted, font=("Arial", 16), bg="#87CEEB", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)
tk.Button(button_frame, text="⬇️ Download Decrypted", command=download_decrypted, font=("Arial", 16), bg="#87CEEB", fg="black", borderwidth=3, relief="raised").pack(side="left", padx=10)

tk.Button(top_frame, text="🌙 Dark Mode", command=toggle_dark_mode, font=("Arial", 18), bg="#708090", fg="white", borderwidth=3, relief="raised").pack(side="right", padx=10)
tk.Button(top_frame, text="🚪 Exit", command=exit_win, font=("Arial", 18), bg="#FF0000", fg="white", borderwidth=3, relief="raised").pack(side="right", padx=10)

# Start the application
window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()