import tkinter as tk
import random

# Configuration
CANVAS_W = 800
CANVAS_H = 600
ANIMATION = "Stars"  # "Stars" or "Fireworks"

# -------------------- BACKGROUND ANIMATIONS --------------------

def stars_animation():
    canvas.delete("bg")
    for _ in range(60):
        x = random.randint(0, CANVAS_W)
        y = random.randint(0, CANVAS_H)
        r = random.randint(1, 4)
        canvas.create_oval(
            x, y, x+r, y+r,
            fill="white",
            outline="white",
            tags="bg"
        )
    root.after(300, stars_animation)

def fireworks_animation():
    canvas.delete("bg")
    x = random.randint(100, CANVAS_W - 100)
    y = random.randint(80, CANVAS_H - 100)
    for r in range(10, 60, 10):
        canvas.create_oval(
            x-r, y-r, x+r, y+r,
            outline=random.choice(["red", "yellow", "cyan", "magenta"]),
            width=2,
            tags="bg"
        )
    root.after(600, fireworks_animation)

# -------------------- MAIN DISPLAY --------------------

def start_animation():
    canvas.delete("all")

    choice = ANIMATION
    message = "🎉 HAPPY NEW YEAR 2026 🎉"

    # Background animation
    if choice == "Stars":
        stars_animation()
    elif choice == "Fireworks":
        fireworks_animation()

    # Foreground text (message)
    canvas.create_text(
        CANVAS_W//2, CANVAS_H//3,
        text=message,
        font=("Arial", 36, "bold"),
        fill="gold",
        tags="fg"
    )

    canvas.create_text(
        CANVAS_W - 80, CANVAS_H - 30,
        text="– Tejas R S",
        font=("Arial", 14, "italic"),
        fill="white",
        tags="fg"
    )

# -------------------- GUI SETUP --------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Happy New Year 2026")
    root.geometry(f"{CANVAS_W}x{CANVAS_H}")
    root.resizable(False, False)
    # Remove window decorations so the viewer sees only the animation (press Escape to close)
    root.overrideredirect(True)
    root.bind("<Escape>", lambda e: root.destroy())

    canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="black", highlightthickness=0)
    canvas.pack()

    # Start animation automatically
    start_animation()

    root.mainloop()
