# Windows Crash Simulator

A visual-only Windows crash/recovery simulation made with Python and Tkinter.

## What it does

- Shows a fake system diagnostic screen.
- Transitions into a Windows-style crash screen.
- Adds progressive glitching, scanlines, flickering and corruption.
- Shows a short recovery/restarting animation.
- Plays a built-in Windows exit/system sound.
- Turns **off only the monitor/display** at the end.

## Safety

This project does **not** intentionally shut down, restart, damage, encrypt, delete, or modify Windows system files.

The final display-off action uses the Windows monitor-power message. The operating system remains running.

## Controls

- `Esc` — exit
- `Ctrl+C` — exit

## Run

```powershell
python "DontOpen.py"
```

Windows only!!!.
