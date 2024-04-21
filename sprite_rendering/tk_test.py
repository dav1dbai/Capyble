import tkinter as tk
import math, time, random

# select a color as the transparent color
TRANS_COLOR = "#000000"

root = tk.Tk()
root.overrideredirect(True)
# root.overrideredirect(False)
root.attributes('-alpha',1)
root.wm_attributes("-topmost", "true")

image = tk.PhotoImage(file='./assets/capybara.png')
tk.Label(root, image=image).pack()

# support dragging window

def start_drag(event):
    global dx, dy
    dx, dy = event.x, event.y

def travel_test():
    global win_x, win_y

    # Define the center of the screen
    win_x = root.winfo_x()
    win_y = root.winfo_y()

    # Choose a random point on the screen
    dest_x = random.randint(0, root.winfo_screenwidth())
    dest_y = random.randint(0, root.winfo_screenheight())

    # Calculate the distance to travel
    dx = dest_x - win_x
    dy = dest_y - win_y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Calculate the unit vector for the direction of movement
    if distance != 0:
        dx_unit = dx / distance
        dy_unit = dy / distance
    else:
        dx_unit, dy_unit = 0, 0

    # Move the window in small increments along the trajectory to the destination
    steps = int(distance)
    for step in range(steps):
        # Calculate the new position based on the step along the trajectory
        x = win_x + int(step * dx_unit)
        y = win_y + int(step * dy_unit)

        # Move the root window to the new position
        root.geometry(f'+{x}+{y}')
        root.update()
        time.sleep(0.005)
    time.sleep(1)

def drag_window(event):
    root.geometry(f'+{event.x_root-dx}+{event.y_root-dy}')

#root.bind('<Button-1>', start_drag)
# root.bind('<B1-Motion>', drag_window)
    
m = tk.Message(text="This is a Tkinter message widget. Pretty exiting, huh? I enjoy Tkinter. It is very simple.")
m.pack(expand=True, fill='x')
m.bind("<Configure>", lambda e: m.configure(width=e.width-10))

while(1):
    travel_test()
    print("traversed")

root.mainloop()