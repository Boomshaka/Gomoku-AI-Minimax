
import tkinter as tk
from gui import BoardFrame

def main():
	window = tk.Tk()
	window.wm_title("Gomoku AI Game")
	board = BoardFrame(window)
	board.pack()
	window.mainloop()


if __name__ == "__main__":
	main()