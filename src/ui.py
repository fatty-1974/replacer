import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import pyperclip
from docx_processor import DocxProcessor
import app_info


class DocxReplacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DOCX Замена текста")
        self.root.geometry("700x650")

        self.folder_path = tk.StringVar()
        self.create_menu()
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Справка", menu=help_menu)

        help_menu.add_command(label="О программе", command=self.show_about_window)

        self.create_widgets()

    def create_widgets(self):
        # Выбор папки
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(folder_frame, text="Папка с файлами:").pack(anchor=tk.W)
        folder_input_frame = tk.Frame(folder_frame)
        folder_input_frame.pack(fill=tk.X, pady=5)

        tk.Entry(folder_input_frame, textvariable=self.folder_path, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        tk.Button(folder_input_frame, text="Обзор", command=self.browse_folder).pack(
            side=tk.RIGHT, padx=(5, 0)
        )

        # Текст для поиска
        search_frame = tk.LabelFrame(self.root, text="Текст для поиска")
        search_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.search_text_area = scrolledtext.ScrolledText(search_frame, height=8)
        self.search_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Button(search_frame, text="Вставить из буфера обмена",
                  command=self.paste_search_text).pack(pady=5)

        # Текст для замены
        replace_frame = tk.LabelFrame(self.root, text="Текст для замены")
        replace_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.replace_text_area = scrolledtext.ScrolledText(replace_frame, height=8)
        self.replace_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Button(replace_frame, text="Вставить из буфера обмена",
                  command=self.paste_replace_text).pack(pady=5)

        # Кнопка выполнения
        tk.Button(
            self.root,
            text="Заменить текст во всех файлах",
            command=self.process_files,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=20, padx=10, fill=tk.X)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def paste_search_text(self):
        try:
            text = pyperclip.paste()
            self.search_text_area.delete(1.0, tk.END)
            self.search_text_area.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вставить текст: {e}")

    def paste_replace_text(self):
        try:
            text = pyperclip.paste()
            self.replace_text_area.delete(1.0, tk.END)
            self.replace_text_area.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вставить текст: {e}")

    def process_files(self):
        folder = self.folder_path.get()
        search_text = self.search_text_area.get("1.0", "end-1c")
        replace_text = self.replace_text_area.get("1.0", "end-1c")

        if not folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку с файлами")
            return

        if not search_text:
            messagebox.showerror("Ошибка", "Пожалуйста, введите текст для поиска")
            return

        try:
            processor = DocxProcessor()
            files_processed = processor.process_folder(folder, search_text, replace_text)
            messagebox.showinfo("Успех", f"Обработано файлов: {files_processed}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def show_about_window(self):
        about = tk.Toplevel(self.root)
        about.title("О программе")
        about.geometry("420x420")
        about.resizable(False, False)
        about.configure(bg="#f0f0f0")

        # Центрирование окна относительно главного
        about.update_idletasks()

        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_w = self.root.winfo_width()
        main_h = self.root.winfo_height()

        win_w = about.winfo_width()
        win_h = about.winfo_height()

        pos_x = main_x + (main_w - win_w) // 2
        pos_y = main_y + (main_h - win_h) // 2

        about.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        
        # Логотип
        try:
            if hasattr(sys, "_MEIPASS"):
                logo_path = os.path.join(sys._MEIPASS, "logo.png")
            else:
                logo_path = "logo.png"

            logo_img = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(about, image=logo_img, bg="#f0f0f0")
            logo_label.image = logo_img
            logo_label.pack(pady=10)

        except Exception as e:
            tk.Label(about, text="[Логотип не найден]", fg="red", bg="#f0f0f0").pack(pady=10)


        # Заголовок
        tk.Label(
            about,
            text=app_info.APP_NAME,
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
        ).pack(pady=5)

        # Версия
        tk.Label(
            about,
            text=f"Версия: {app_info.APP_VERSION}",
            font=("Arial", 12),
            bg="#f0f0f0",
        ).pack()

        # Автор
        tk.Label(
            about,
            text=f"Автор: {app_info.APP_AUTHOR}",
            font=("Arial", 12),
            bg="#f0f0f0",
        ).pack()

        # Дата компиляции
        tk.Label(
            about,
            text=f"Дата компиляции: {app_info.get_compile_date()}",
            font=("Arial", 12),
            bg="#f0f0f0",
        ).pack(pady=5)

        # Описание
        tk.Label(
            about,
            text=app_info.APP_DESCRIPTION,
            font=("Arial", 11),
            wraplength=380,
            justify="center",
            bg="#f0f0f0",
        ).pack(pady=15)

        close_btn = tk.Button(
            about,
            text="Закрыть",
            command=about.destroy,
            bg="#F5F7F9",
            #fg="white",
            font=("Arial", 11),
            padx=20,
            pady=5
            )
        close_btn.pack(pady=10)
        # --- ВАЖНО: пересчитать размеры окна ---
        about.update_idletasks()

        # Центрирование окна относительно главного
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_w = self.root.winfo_width()
        main_h = self.root.winfo_height()

        win_w = about.winfo_width()
        win_h = about.winfo_height()

        pos_x = main_x + (main_w - win_w) // 2
        pos_y = main_y + (main_h - win_h) // 2

        #about.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocxReplacerApp(root)
    root.mainloop()
