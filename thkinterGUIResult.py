import tkinter as tk
from tkinter import ttk, messagebox

class ResultApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Result Portal")
        root.geometry("1000x700")
        root.config(bg="#EAFBEA")  

        self.style = ttk.Style(root)
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#EAFBEA", foreground="#0A4D00")
        self.style.configure('TEntry', font=('Segoe UI', 11), padding=6)
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=8, background="#2E8B57", foreground='white')
        self.style.map('TButton', background=[('active', '#228B22')])
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground="#0A4D00", background="#EAFBEA")
        self.style.configure('Treeview.Heading', font=('Segoe UI', 12, 'bold'), background="#2E8B57", foreground='white')
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=26)

        self.extra_subjects = []  
        self.build_gui()

    def build_gui(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 25))

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="📝 Student Information", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15))

        self.student_name = self._entry_item(left, "Student Name:", 1)
        self.student_class = self._entry_item(left, "Class:", 2)
        self.student_seat = self._entry_item(left, "Seat No:", 3)

        ttk.Label(left, text="📘 Main Subjects").grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="w")
        self.subject_entries = []
        subjects = ["Java", "Python", "OOSE", "Cyber Security"]
        for i, subj in enumerate(subjects):
            self.subject_entries.append((subj, self._entry_item(left, f"{subj}:", 5 + i)))

        self.extra_start_row = 9 + len(subjects)
        self.extra_container = ttk.Frame(left)
        self.extra_container.grid(row=self.extra_start_row, column=0, columnspan=2, pady=(10, 0), sticky="w")

        self.add_btn = ttk.Button(left, text="➕ Add Extra Subject", command=self.add_extra_subject)
        self.add_btn.grid(row=self.extra_start_row + 1, column=0, columnspan=2, pady=15)

        ttk.Button(left, text="✅ Calculate Result", command=self.calculate).grid(row=self.extra_start_row + 2, column=0, columnspan=2, pady=20)

        ttk.Label(right, text="📊 Result Summary", style='Header.TLabel').pack(anchor="w", pady=(0, 10))
        self.info_label = ttk.Label(right, text="", font=('Segoe UI', 10, 'italic'), background="#EAFBEA", foreground="#0A4D00")
        self.info_label.pack(anchor="w", pady=(0, 10))

        columns = ("Subject", "Marks")
        self.table = ttk.Treeview(right, columns=columns, show="headings", height=20)
        self.table.heading("Subject", text="Subject")
        self.table.heading("Marks", text="Marks")
        self.table.column("Subject", anchor=tk.W, width=300)
        self.table.column("Marks", anchor=tk.CENTER, width=120)
        self.table.pack(fill=tk.BOTH, expand=True)

    def _entry_item(self, parent, label, row, state='normal'):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(parent, state=state, width=35)
        entry.grid(row=row, column=1, sticky="w", pady=5)
        return entry

    def add_extra_subject(self):
        row = len(self.extra_subjects)
        frame = ttk.Frame(self.extra_container)
        frame.grid(row=row, column=0, pady=5, sticky="w")

        name_label = ttk.Label(frame, text="Subject:")
        name_label.grid(row=0, column=0)
        name_entry = ttk.Entry(frame, width=20)
        name_entry.grid(row=0, column=1, padx=5)

        mark_label = ttk.Label(frame, text="Marks:")
        mark_label.grid(row=0, column=2)
        mark_entry = ttk.Entry(frame, width=10)
        mark_entry.grid(row=0, column=3, padx=5)

        self.extra_subjects.append((name_entry, mark_entry))

    def calculate(self):
        self.table.delete(*self.table.get_children())

        name = self.student_name.get().strip()
        cls = self.student_class.get().strip()
        seat = self.student_seat.get().strip()
        if not (name and cls and seat):
            messagebox.showwarning("Missing Info", "Please fill in all student fields.")
            return

        marks_list = []
        failed = []

        for subj, entry in self.subject_entries:
            try:
                val = int(entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter valid marks for {subj}.")
                return
            marks_list.append((subj, val))
            if val < 35:
                failed.append(subj)
            self.table.insert("", tk.END, values=(subj, val))

        for name_entry, mark_entry in self.extra_subjects:
            subj = name_entry.get().strip() or "Extra Subject"
            try:
                val = int(mark_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter valid marks for extra subject.")
                return
            marks_list.append((subj, val))
            if val < 35:
                failed.append(subj)
            self.table.insert("", tk.END, values=(subj, val))

        total = sum([m[1] for m in marks_list])
        count = len(marks_list)
        percentage = total / count
        status = "Failed ❌" if failed else "Passed ✅"

        
        self.table.insert("", tk.END, values=("Total Marks", total))
        self.table.insert("", tk.END, values=("Percentage", f"{percentage:.2f}%"))
        self.table.insert("", tk.END, values=("Result", status))

        info = f"Name: {name}    Class: {cls}    Seat No: {seat}"
        self.info_label.config(text=info)


if __name__ == "__main__":
    root = tk.Tk()
    app = ResultApp(root)
    root.mainloop()
