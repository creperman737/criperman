#!/usr/bin/env python3
import ast
import operator
import os
import tkinter as tk

from PIL import Image, ImageTk


APP_TITLE = "Neon Kalkulyator"
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rasm")
IMAGE_FILES = {
    "C": "c.jpg", "/": "boluv.jpg", "*": "kopaytiruv.jpg", "-": "ayruv.jpg",
    "+": "qoshiv.jpg", "=": "barobar.jpg", ".": "nuqta.jpg",
    "0": "nol.jpg", "1": "bir.jpg", "2": "ikki.jpg", "3": "uch.jpg",
    "4": "tor.jpg", "5": "besh.jpg", "6": "olti.jpg", "7": "yetti.jpg",
    "8": "sakkiz.jpg", "9": "to'qiz.jpg", "BS": "del.jpg"
}
OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub,
             ast.Mult: operator.mul, ast.Div: operator.truediv}


def calculate(expression):
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](visit(node.left), visit(node.right))
        raise ValueError("Noto'g'ri ifoda")

    return visit(ast.parse(expression, mode="eval"))


class CustomCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("390x700")
        self.root.minsize(330, 600)
        self.root.configure(bg="#031308")
        self.equation = ""
        self.display_var = tk.StringVar(value="0")
        self.images = {}
        self.button_source = self.load_source_image("tugma.jpg")
        self.backspace_source = self.load_source_image(IMAGE_FILES["BS"])
        self.button_photos = {}
        self.background = self.load_image("orqa fon.jpg", (390, 700), stretch=True)
        if self.background:
            tk.Label(self.root, image=self.background, bg="#031308").place(
                relx=0, rely=0, relwidth=1, relheight=1)
        self.build_display()
        self.build_buttons()

    def load_image(self, filename, size, stretch=False):
        image = self.load_source_image(filename)
        if image is None:
            return None
        if stretch:
            image = image.resize(size, Image.Resampling.LANCZOS)
        else:
            image.thumbnail(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def load_source_image(self, filename):
        path = os.path.join(IMAGE_FOLDER, filename)
        try:
            return Image.open(path).convert("RGB")
        except (OSError, ValueError):
            return None

    def build_display(self):
        display = tk.Frame(self.root, bg="#061b08", highlightthickness=2,
                           highlightbackground="#71ff19")
        display.pack(fill=tk.X, padx=18, pady=(25, 12))
        tk.Label(display, textvariable=self.display_var, anchor="e", padx=14,
                 pady=12, font=("DejaVu Sans", 25, "bold"),
                 fg="#b7ff58", bg="#061b08").pack(fill=tk.X)

    def build_buttons(self):
        frame = tk.Frame(self.root, bg="#031308")
        frame.pack(expand=True, fill=tk.BOTH, padx=18, pady=(4, 22))
        buttons_config = [
            ("C", 0, 0, 1, 1), ("BS", 0, 1, 1, 1), ("/", 0, 2, 1, 1), ("*", 0, 3, 1, 1),
            ("7", 1, 0, 1, 1), ("8", 1, 1, 1, 1), ("9", 1, 2, 1, 1), ("-", 1, 3, 1, 1),
            ("4", 2, 0, 1, 1), ("5", 2, 1, 1, 1), ("6", 2, 2, 1, 1), ("+", 2, 3, 1, 1),
            ("1", 3, 0, 1, 1), ("2", 3, 1, 1, 1), ("3", 3, 2, 1, 1), ("=", 3, 3, 2, 1),
            ("0", 4, 0, 1, 2), (".", 4, 2, 1, 1),
        ]
        for key, row, column, row_span, column_span in buttons_config:
            button = self.create_image_button(
                frame, key, lambda value=key: self.on_button_click(value))
            button.grid(row=row, column=column, rowspan=row_span,
                        columnspan=column_span, padx=3, pady=3, sticky="nsew")
        for row in range(5):
            frame.grid_rowconfigure(row, weight=1)
        for column in range(4):
            frame.grid_columnconfigure(column, weight=1)

    def create_image_button(self, parent, text, command):
        canvas = tk.Canvas(parent, width=86, height=72, bg="#08200b",
                           highlightthickness=0, bd=0)
        background_id = canvas.create_image(0, 0, anchor="nw")
        text_id = None if text == "BS" and self.backspace_source else canvas.create_text(
            43, 36, text=text, fill="#caff82", font=("DejaVu Sans", 18, "bold"))
        canvas.bind("<Configure>", lambda event: self.resize_image_button(
            canvas, event, background_id, text_id))
        canvas.bind("<Button-1>", lambda event: command())
        canvas.bind("<Enter>", lambda event: canvas.configure(bg="#1d5a18"))
        canvas.bind("<Leave>", lambda event: canvas.configure(bg="#08200b"))
        return canvas

    def resize_image_button(self, canvas, event, background_id, text_id):
        if event.width < 2 or event.height < 2:
            return
        if text_id is not None:
            canvas.coords(text_id, event.width / 2, event.height / 2)
        source = self.backspace_source if text_id is None else self.button_source
        if source is not None:
            image = source.resize((event.width, event.height),
                                               Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.button_photos[canvas] = photo
            canvas.itemconfigure(background_id, image=photo)

    def on_button_click(self, key):
        if key == "C":
            self.equation = ""
            self.display_var.set("0")
            return
        if key == "BS":
            self.equation = self.equation[:-1]
            self.display_var.set(self.equation or "0")
            return
        if key == "=":
            try:
                result = calculate(self.equation)
                self.equation = str(round(result, 10))
                self.display_var.set(self.equation)
            except (SyntaxError, ValueError, ZeroDivisionError):
                self.equation = ""
                self.display_var.set("Xato")
            return
        if self.display_var.get() in ("0", "Xato"):
            self.equation = "" if key == "." else key
        else:
            self.equation += key
        self.display_var.set(self.equation or "0")


if __name__ == "__main__":
    root = tk.Tk()
    CustomCalculator(root)
    root.mainloop()
