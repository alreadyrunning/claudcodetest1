import subprocess
import sys
import os
import webbrowser
import tkinter as tk
from tkinter import font as tkfont

PORT = 8000
URL = f"http://localhost:{PORT}/learning-path.html"
server_process = None


def start_server():
    global server_process
    if server_process and server_process.poll() is None:
        return
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    webbrowser.open(URL)
    set_status("running")


def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process = None
    set_status("stopped")


def set_status(state):
    if state == "running":
        status_dot.config(bg="#4caf50")
        status_label.config(text="Server running", fg="#4caf50")
        btn_start.config(state="disabled")
        btn_stop.config(state="normal")
    else:
        status_dot.config(bg="#ef5350")
        status_label.config(text="Server stopped", fg="#ef5350")
        btn_start.config(state="normal")
        btn_stop.config(state="disabled")


def on_close():
    stop_server()
    root.destroy()


root = tk.Tk()
root.title("Learning Path Launcher")
root.geometry("300x180")
root.resizable(False, False)
root.configure(bg="#0f1117")
root.protocol("WM_DELETE_WINDOW", on_close)

title_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
label_font = tkfont.Font(family="Segoe UI", size=9)
btn_font = tkfont.Font(family="Segoe UI", size=10)

tk.Label(root, text="Claude Learning Path", font=title_font,
         bg="#0f1117", fg="#a78bfa").pack(pady=(22, 4))
tk.Label(root, text="Start the server to open your progress tracker",
         font=label_font, bg="#0f1117", fg="#888888").pack(pady=(0, 18))

btn_frame = tk.Frame(root, bg="#0f1117")
btn_frame.pack()

btn_start = tk.Button(btn_frame, text="Start", font=btn_font, width=10,
                      bg="#4caf50", fg="#0a1f0a", relief="flat", cursor="hand2",
                      activebackground="#388e3c", activeforeground="#0a1f0a",
                      command=start_server)
btn_start.grid(row=0, column=0, padx=8)

btn_stop = tk.Button(btn_frame, text="Stop", font=btn_font, width=10,
                     bg="#ef5350", fg="#1f0a0a", relief="flat", cursor="hand2",
                     activebackground="#c62828", activeforeground="#1f0a0a",
                     state="disabled", command=stop_server)
btn_stop.grid(row=0, column=1, padx=8)

status_frame = tk.Frame(root, bg="#0f1117")
status_frame.pack(pady=(18, 0))

status_dot = tk.Label(status_frame, text="  ", bg="#ef5350", width=2)
status_dot.grid(row=0, column=0, padx=(0, 6))

status_label = tk.Label(status_frame, text="Server stopped", font=label_font,
                        bg="#0f1117", fg="#ef5350")
status_label.grid(row=0, column=1)

root.mainloop()
