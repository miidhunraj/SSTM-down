import tkinter as tk
import random
import time
import threading
import winsound
import ctypes
from ctypes import wintypes

# ============================================================
# WINDOWS GLITCH / CRASH SIMULATOR
# Safe simulation: does NOT shut down or restart Windows.
# At the end it turns OFF ONLY the monitor/display.
# Press ESC or CTRL+C to exit the simulation.
# ============================================================

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")

W = root.winfo_screenwidth()
H = root.winfo_screenheight()

canvas = tk.Canvas(
    root,
    width=W,
    height=H,
    bg="black",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

# ------------------------------------------------------------
# EXIT
# ------------------------------------------------------------

running = True

def quit_app(event=None):
    global running
    running = False
    root.destroy()

root.bind("<Escape>", quit_app)
root.bind_all("<Control-c>", quit_app)

# Keep the mouse from interacting with the fake crash screen.
root.bind("<Button-1>", lambda e: "break")
root.bind("<Button-2>", lambda e: "break")
root.bind("<Button-3>", lambda e: "break")

# ------------------------------------------------------------
# SAFE WINDOWS DISPLAY OFF
# Turns off ONLY the monitor. It does not shut down Windows.
# ------------------------------------------------------------

def turn_off_display():
    try:
        user32 = ctypes.windll.user32
        HWND_BROADCAST = 0xFFFF
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        MONITOR_OFF = 2
        user32.SendMessageW(
            HWND_BROADCAST,
            WM_SYSCOMMAND,
            SC_MONITORPOWER,
            MONITOR_OFF
        )
    except Exception:
        pass

# ------------------------------------------------------------
# WINDOWS-STYLE EXIT SOUND
# Uses a built-in Windows system sound when available.
# ------------------------------------------------------------

def play_exit_sound():
    try:
        winsound.PlaySound(
            "SystemExit",
            winsound.SND_ALIAS | winsound.SND_ASYNC
        )
    except Exception:
        try:
            winsound.MessageBeep(winsound.MB_ICONHAND)
        except Exception:
            pass

# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------

progress = 0
glitch_level = 0
crash_frame = 0
recovery_frame = 0

diagnostic_messages = [
    "Checking system integrity...",
    "Verifying system files...",
    "Checking device drivers...",
    "Scanning memory...",
    "Validating security components...",
]

stop_codes = [
    "CRITICAL_PROCESS_FAILURE",
    "SYSTEM_SERVICE_EXCEPTION",
    "MEMORY_MANAGEMENT",
    "KERNEL_SECURITY_CHECK_FAILURE",
]

# ------------------------------------------------------------
# DRAW HELPERS
# ------------------------------------------------------------

def glitch_bars(count=12):
    for _ in range(count):
        y = random.randint(0, max(1, H - 8))
        h = random.randint(2, 18)
        x = random.randint(-80, max(1, W - 50))
        width = random.randint(40, max(100, W // 2))

        colors = ["#ffffff", "#00ffff", "#ff003c", "#111111", "#666666"]
        canvas.create_rectangle(
            x, y, x + width, y + h,
            fill=random.choice(colors),
            outline=""
        )

def scanlines():
    for y in range(0, H, 5):
        canvas.create_rectangle(
            0, y, W, y + 1,
            fill="#000000",
            outline=""
        )

# ------------------------------------------------------------
# PHASE 1: DIAGNOSTIC
# ------------------------------------------------------------

def diagnostic():
    global progress

    if not running:
        return

    canvas.delete("all")
    canvas.configure(bg="#050505")

    canvas.create_text(
        50, 45,
        anchor="w",
        text="SYSTEM DIAGNOSTIC",
        fill="#e8e8e8",
        font=("Segoe UI", 22)
    )

    canvas.create_text(
        50, 85,
        anchor="w",
        text="Windows Recovery Environment",
        fill="#777777",
        font=("Segoe UI", 12)
    )

    canvas.create_line(
        50, 115, W - 50, 115,
        fill="#292929"
    )

    msg = diagnostic_messages[
        min(progress // 18, len(diagnostic_messages) - 1)
    ]

    canvas.create_text(
        50, 180,
        anchor="w",
        text=msg,
        fill="#d0d0d0",
        font=("Consolas", 16)
    )

    bar_x, bar_y = 50, 230
    bar_w = min(700, W - 100)
    bar_h = 18

    canvas.create_rectangle(
        bar_x, bar_y,
        bar_x + bar_w, bar_y + bar_h,
        outline="#444444"
    )

    filled = int(bar_w * progress / 100)

    canvas.create_rectangle(
        bar_x, bar_y,
        bar_x + filled, bar_y + bar_h,
        fill="#1677ff",
        outline=""
    )

    canvas.create_text(
        bar_x, bar_y + 45,
        anchor="w",
        text=f"{progress}% complete",
        fill="#888888",
        font=("Consolas", 11)
    )

    info = [
        "Memory integrity        [OK]",
        "System files            [OK]",
        "Kernel integrity        [OK]",
        "Device drivers          [CHECKING]",
        "Security services       [CHECKING]",
    ]

    y = 340
    for line in info:
        color = "#6ee76e" if "[OK]" in line else "#d0d0d0"
        canvas.create_text(
            50, y,
            anchor="w",
            text=line,
            fill=color,
            font=("Consolas", 13)
        )
        y += 32

    canvas.create_text(
        50, H - 55,
        anchor="w",
        text="Do not turn off your computer.",
        fill="#555555",
        font=("Segoe UI", 10)
    )

    progress += random.choice([2, 2, 3, 4])

    if progress >= 100:
        root.after(500, crash_screen)
    else:
        root.after(random.randint(70, 140), diagnostic)

# ------------------------------------------------------------
# PHASE 2: REALISTIC-STYLE CRASH + GLITCH
# ------------------------------------------------------------

def crash_screen():
    global crash_frame

    if not running:
        return

    canvas.delete("all")

    # Normal crash screen base
    canvas.configure(bg="#0067b8")

    canvas.create_text(
        110, 125,
        anchor="w",
        text=":(",
        fill="white",
        font=("Segoe UI Light", 72)
    )

    canvas.create_text(
        115, 270,
        anchor="w",
        text="Your PC ran into a problem.",
        fill="white",
        font=("Segoe UI", 31)
    )

    canvas.create_text(
        115, 325,
        anchor="w",
        text="It needs to restart.",
        fill="white",
        font=("Segoe UI", 31)
    )

    percent = min(crash_frame, 100)

    canvas.create_text(
        115, 405,
        anchor="w",
        text=f"{percent}% complete",
        fill="white",
        font=("Segoe UI", 18)
    )

    code = random.choice(stop_codes)

    canvas.create_text(
        115, 475,
        anchor="w",
        text=f"Stop code: {code}",
        fill="white",
        font=("Consolas", 13)
    )

    # Very short security/system warning.
    if crash_frame > 38:
        warning = random.choice([
            "SYSTEM INTEGRITY FAILURE",
            "SECURITY CHECK FAILED",
            "SYSTEM FAILURE",
        ])
        canvas.create_text(
            115, 520,
            anchor="w",
            text=warning,
            fill="white",
            font=("Consolas", 11)
        )

    # QR-like diagnostic block
    size = 108
    x0 = W - 205
    y0 = H - 180

    for yy in range(12):
        for xx in range(12):
            if random.random() > 0.53:
                canvas.create_rectangle(
                    x0 + xx * 8,
                    y0 + yy * 8,
                    x0 + xx * 8 + 6,
                    y0 + yy * 8 + 6,
                    fill="white",
                    outline=""
                )

    # Increasing visual corruption
    if crash_frame > 22:
        for _ in range(min(30, 5 + crash_frame // 3)):
            glitch_bars(1)

    if crash_frame > 45:
        scanlines()

    # Flicker / corruption near the end
    if crash_frame > 68 and random.random() > 0.35:
        canvas.create_rectangle(
            0, random.randint(0, H - 30),
            W, random.randint(20, 80),
            fill=random.choice(["#000000", "#ffffff", "#ff003c", "#00ffff"]),
            outline=""
        )

    crash_frame += random.randint(2, 4)

    if crash_frame >= 100:
        root.after(700, recovery_screen)
    else:
        root.after(random.randint(70, 150), crash_screen)

# ------------------------------------------------------------
# PHASE 3: GLITCHED RECOVERY
# ------------------------------------------------------------

def recovery_screen():
    global recovery_frame

    if not running:
        return

    canvas.delete("all")

    # Mostly black with corrupted flashes.
    canvas.configure(bg="#000000")

    if recovery_frame < 18:
        title = "Restarting"
    elif recovery_frame < 34:
        title = "Restarting."
    elif recovery_frame < 50:
        title = "Restarting.."
    else:
        title = "Restarting..."

    canvas.create_text(
        W // 2,
        H // 2 - 45,
        text=title,
        fill="white",
        font=("Segoe UI Light", 28)
    )

    # Spinner-like blocks
    cx, cy = W // 2, H // 2 + 20
    for i in range(8):
        angle = (recovery_frame * 0.25) + i * (math.pi / 4)
        x = cx + int(math.cos(angle) * 34)
        y = cy + int(math.sin(angle) * 34)

        canvas.create_rectangle(
            x - 4, y - 4, x + 4, y + 4,
            fill="white",
            outline=""
        )

    canvas.create_text(
        W // 2,
        H - 70,
        text="Please wait...",
        fill="#666666",
        font=("Segoe UI", 11)
    )

    # Corrupted frames
    if recovery_frame > 20:
        glitch_bars(random.randint(2, 12))

    if random.random() > 0.65:
        scanlines()

    recovery_frame += 1

    if recovery_frame >= 75:
        play_exit_sound()
        root.after(1200, display_off)
    else:
        root.after(90, recovery_screen)

# ------------------------------------------------------------
# PHASE 4: DISPLAY ONLY OFF
# ------------------------------------------------------------

def display_off():
    if not running:
        return

    canvas.delete("all")
    canvas.configure(bg="black")

    # Give the sound a moment before the monitor goes dark.
    root.after(350, turn_off_display)

# ------------------------------------------------------------
# START
# ------------------------------------------------------------

diagnostic()
root.mainloop()
