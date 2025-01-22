import tkinter as tk
from tkinter import ttk
from djitellopy import Tello
import cv2
from PIL import Image, ImageTk
import threading

tello = Tello()

frame = None
running = False
package_count = 0

# Function to start the drone and video feed
def start_drone():
    global running
    running = True
    tello.connect()
    tello.streamon()
    update_video_feed()

# Function to stop the drone and video feed
def stop_drone():
    global running
    running = False
    tello.streamoff()
    tello.land()

# Function to update the video feed
def update_video_feed():
    global frame, running, package_count

    if running:
        frame = tello.get_frame_read().frame

        # Simulate package counting logic (replace with actual detection)
        package_count = 5

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)

        video_label.img_tk = img_tk
        video_label.configure(image=img_tk)

        package_counter_label.config(text=f"Packages Detected: {package_count}")

        video_label.after(10, update_video_feed)

# Function to handle Start button click
def on_start():
    threading.Thread(target=start_drone, daemon=True).start()

# Function to handle Stop button click
def on_stop():
    stop_drone()

# Function to handle Shelf Dimensions submission
def submit_dimensions():
    width = shelf_width.get()
    height = shelf_height.get()
    print(f"Shelf Dimensions: {width}x{height}")  # Use these dimensions as needed

# Create the main Tkinter window
root = tk.Tk()
root.title("Drone Package Counter")
root.geometry("600x500")
root.configure(bg="#f0f0f0")  # Light gray background

# Create a custom style
style = ttk.Style()
style.theme_use("clam")  # Use 'clam' theme for modern look

# Customize Button style
style.configure("TButton", 
                font=("Helvetica", 12), 
                padding=5,
                background="blue",  # Green background
                foreground="white")

style.map("TButton", background=[("active", "#45a049")])  # Lighter green when hovered

# Customize Labels
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0", foreground="black")

# Create Start and Stop buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Start", command=on_start)
start_button.grid(row=0, column=0, padx=10)

stop_button = ttk.Button(button_frame, text="Stop", command=on_stop)
stop_button.grid(row=0, column=1, padx=10)

# Shelf dimensions input fields
dimensions_frame = tk.Frame(root, bg="#f0f0f0")
dimensions_frame.pack(pady=10)

tk.Label(dimensions_frame, text="Shelf Width:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
shelf_width = tk.Entry(dimensions_frame, font=("Arial", 12), width=10)
shelf_width.grid(row=0, column=1, padx=5, pady=5)

tk.Label(dimensions_frame, text="Shelf Height:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
shelf_height = tk.Entry(dimensions_frame, font=("Arial", 12), width=10)
shelf_height.grid(row=1, column=1, padx=5, pady=5)

submit_button = ttk.Button(dimensions_frame, text="Submit", command=submit_dimensions)
submit_button.grid(row=2, columnspan=2, pady=10)

# Live video feed display
video_frame = tk.Frame(root, bg="#e0e0e0", relief="groove", borderwidth=2)
video_frame.pack(pady=10)

video_label = tk.Label(video_frame, bg="#000", width=60, height=20)
video_label.pack()

# Package counter display
package_counter_label = tk.Label(root, text="Packages Detected: 0", font=("Arial", 16), bg="#f0f0f0", fg="#333")
package_counter_label.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
