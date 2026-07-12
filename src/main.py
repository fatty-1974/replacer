import tkinter as tk
from ui import DocxReplacerApp

def main():
    root = tk.Tk()
    app = DocxReplacerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()