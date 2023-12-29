from tkinter import * 
from src.models import models

if __name__ == '__main__':
    root = Tk()
    app = models.RecordTrackExpense(root)
    root.mainloop()