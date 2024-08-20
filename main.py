from gui import VideoPlagiarismCheckerGUI
from src.database import create_connection, create_table
import tkinter as tk

def main():
    """Main function to start the Video Plagiarism Checker GUI."""
    # Create a connection to the database
    conn = create_connection("videos.db")
    
    # Create table if it doesn't exist
    create_table(conn)

    # Initialize the main application window
    root = tk.Tk()
    app = VideoPlagiarismCheckerGUI(root, conn)  # Pass the database connection to GUI
    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()
