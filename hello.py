import tkinter as tk
from tkinter import messagebox
import random
from typing import List

# Константы
WORDS: List[str] = [
    "питон", "программирование", "виселица", 
    "курсовая", "студент", "алгоритм", "интерфейс"
]
LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Глобальные переменные игры
word = ""
guessed_letters = []
attempts_left = 6
game_over = False

# Глобальные переменные интерфейса
root = None
hangman_label = None
word_label = None
bottom_frame = None
hangman_images = []  # список изображений виселицы

def load_images():
    """Загружает изображения для виселицы."""
    global hangman_images
    for i in range(7):
        img = tk.PhotoImage(file=f"img/stage{i}.png")
        hangman_images.append(img)

def init_game():
    """Инициализирует новую игру."""
    global word, guessed_letters, attempts_left, game_over
    word = random.choice(WORDS).upper()
    guessed_letters = []
    attempts_left = 6
    game_over = False
    update_display()

def create_widgets():
    """Создает элементы интерфейса."""
    global root, hangman_label, word_label, bottom_frame

    root = tk.Tk()
    root.title("🎮 Виселица")
    root.geometry("500x800")
    root.resizable(False, False)

    load_images()

    # Верхний фрейм (виселица)
    top_frame = tk.Frame(root)
    top_frame.pack(pady=20)

    hangman_label = tk.Label(top_frame)
    hangman_label.pack()

    # Средний фрейм (слово и кнопка новой игры)
    middle_frame = tk.Frame(root)
    middle_frame.pack(pady=20)

    word_label = tk.Label(middle_frame, font=("Arial", 24))
    word_label.pack()

    new_game_btn = tk.Button(
        middle_frame,
        text="Новая игра",
        command=init_game,
        font=("Arial", 12)
    )
    new_game_btn.pack(pady=10)

    # Нижний фрейм (клавиатура)
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(pady=20)

    create_keyboard()
    init_game()

def create_keyboard():
    """Создает клавиатуру для ввода букв."""
    for i, letter in enumerate(LETTERS):
        row, col = divmod(i, 7)
        btn = tk.Button(
            bottom_frame, 
            text=letter, 
            font=("Arial", 12), 
            width=3, 
            command=lambda l=letter: guess_letter(l),
            bg="white"
        )
        btn.grid(row=row, column=col, padx=2, pady=2)

def guess_letter(letter: str):
    """Обрабатывает попытку угадать букву."""
    global guessed_letters, attempts_left, game_over

    if game_over or letter in guessed_letters:
        return

    guessed_letters.append(letter)

    if letter not in word:
        attempts_left -= 1

    update_display()
    check_game_over()

def update_display():
    """Обновляет отображение игры."""
    # Обновляем изображение виселицы
    hangman_label.config(image=hangman_images[6 - attempts_left])
    hangman_label.image = hangman_images[6 - attempts_left]  # важно для отображения

    # Обновляем слово
    displayed_word = " ".join(
        char if char in guessed_letters else "_"
        for char in word
    )
    word_label.config(text=displayed_word)

    # Обновляем кнопки
    update_buttons()

def update_buttons():
    """Обновляет состояние кнопок клавиатуры."""
    for widget in bottom_frame.winfo_children():
        letter = widget["text"]
        if letter in guessed_letters:
            if letter in word:
                widget.config(bg="lightgreen", state="disabled")
            else:
                widget.config(bg="salmon", state="disabled")
        else:
            widget.config(bg="white", state="normal")

def check_game_over():
    """Проверяет условия окончания игры."""
    global game_over

    if all(letter in guessed_letters for letter in word):
        game_over = True
        messagebox.showinfo("Победа!", f"🎉 Вы выиграли! Слово: {word}")
    elif attempts_left <= 0:
        game_over = True
        messagebox.showinfo("Поражение", f"💀 Игра окончена! Слово: {word}")

def main():
    """Запускает игру."""
    create_widgets()
    root.mainloop()

if __name__ == "__main__":
    main()