import tkinter as tk
from tkinter import filedialog, messagebox
import os

APP_NAME = "Py Notepad"

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x600")
        self.current_file = None

        # текстовое поле
        self.text = tk.Text(root, undo=True, wrap="word")
        self.text.pack(fill="both", expand=True, side="left")

        # скроллбар
        scrollbar = tk.Scrollbar(root, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        # меню
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_app)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Перенос по словам", command=self.toggle_wrap)
        menu_bar.add_cascade(label="Вид", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Справка", menu=help_menu)

    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.current_file = None
        self.root.title(APP_NAME)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, f.read())
            self.current_file = path
            self.root.title(f"{os.path.basename(path)} - {APP_NAME}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if path:
            self.current_file = path
            self.save_file()
            self.root.title(f"{os.path.basename(path)} - {APP_NAME}")

    def exit_app(self):
        self.root.quit()

    def toggle_wrap(self):
        current = self.text.cget("wrap")
        self.text.config(wrap="none" if current == "word" else "word")

    def show_about(self):
        messagebox.showinfo("О программе", "Простой блокнот на Python + Tkinter")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
