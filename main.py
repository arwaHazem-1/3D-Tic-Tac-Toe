import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from cubic.gui import CubicGUI

def main():
    root = tk.Tk()
    app = CubicGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()