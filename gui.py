import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.video_processing import extract_frames
from src.feature_extraction import extract_features_from_frames
from src.plagiarism_detection import calculate_similarity
from src.database import insert_video_comparison, get_all_comparisons
import os
import shutil  # To copy files
import threading

class VideoPlagiarismCheckerGUI:
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn  # Save the database connection
        master.title("Video Plagiarism Detector")
        master.geometry("900x600")  # Set the window size
        master.configure(bg="#f0f0f0")  # Light grey background

        # Title Label
        self.title_label = tk.Label(master, text="Video Plagiarism Detection System", font=("Helvetica", 20), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(master, bg="#7cc3d9", width=200)
        self.sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        # Buttons
        self.compare_two_button = tk.Button(self.sidebar_frame, text="Compare Two Videos", command=self.setup_video_selection, font=("Helvetica", 14), bg="#8cd687")
        self.compare_two_button.pack(pady=10, padx=10, fill=tk.X)

        self.compare_db_button = tk.Button(self.sidebar_frame, text="Compare with Database", command=self.setup_db_comparison, font=("Helvetica", 14), bg="#d19a76")
        self.compare_db_button.pack(pady=10, padx=10, fill=tk.X)

        self.past_results_button = tk.Button(self.sidebar_frame, text="View Past Results", command=self.show_past_results, font=("Helvetica", 14), bg="#f1be6a")
        self.past_results_button.pack(pady=10, padx=10, fill=tk.X)

        self.exit_button = tk.Button(self.sidebar_frame, text="Exit", command=self.exit_program, font=("Helvetica", 14), bg="#ef4b4b")
        self.exit_button.pack(pady=10, padx=10, fill=tk.X)

        # Main Content Area
        self.content_frame = tk.Frame(master, bg="#f0f0f0", width=700)
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # Default setup for video selection
        self.setup_video_selection()  # Automatically set to compare videos

    def setup_video_selection(self):
        self.clear_content_frame()

        # Video Frame for Selection
        self.video_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.video_frame.pack(pady=20)

        # Video 1 Selection
        self.video1_label = tk.Label(self.video_frame, text="Video 1: ", font=("Helvetica", 14), bg="#f0f0f0")
        self.video1_label.grid(row=0, column=0, padx=20)
        self.video1_button = tk.Button(self.video_frame, text="Select Video 1", command=self.select_video1, bg="#8cd687")
        self.video1_button.grid(row=0, column=1, padx=20)

        self.video1_name_label = tk.Label(self.video_frame, text="", font=("Helvetica", 12), bg="#f0f0f0")
        self.video1_name_label.grid(row=1, column=0, columnspan=2, pady=(5, 20))

        # Video 2 Selection
        self.video2_label = tk.Label(self.video_frame, text="Video 2: ", font=("Helvetica", 14), bg="#f0f0f0")
        self.video2_label.grid(row=2, column=0, padx=20)
        self.video2_button = tk.Button(self.video_frame, text="Select Video 2", command=self.select_video2, bg="#8cd687")
        self.video2_button.grid(row=2, column=1, padx=20)

        self.video2_name_label = tk.Label(self.video_frame, text="", font=("Helvetica", 12), bg="#f0f0f0")
        self.video2_name_label.grid(row=3, column=0, columnspan=2, pady=(5, 20))

        # Compare Videos Button
        self.compare_button = tk.Button(self.video_frame, text="Compare Videos", command=self.compare_two_videos, font=("Helvetica", 14), bg="lightblue")
        self.compare_button.grid(row=4, column=0, columnspan=2, pady=20)

    def setup_db_comparison(self):
        self.clear_content_frame()
        self.db_video_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.db_video_frame.pack(pady=20)

        # Database Video Selection
        self.db_video_label = tk.Label(self.db_video_frame, text="Select Video for Database Comparison: ", font=("Helvetica", 14), bg="#f0f0f0")
        self.db_video_label.pack(pady=10)

        self.db_video_button = tk.Button(self.db_video_frame, text="Select Video", command=self.select_video_for_db, font=("Helvetica", 14), bg="#8cd687")
        self.db_video_button.pack(pady=10)

        self.db_video_name_label = tk.Label(self.db_video_frame, text="", font=("Helvetica", 12), width=60, bg="#f0f0f0")
        self.db_video_name_label.pack(pady=(5, 20))

        self.db_compare_button = tk.Button(self.db_video_frame, text="Compare with Database", command=self.compare_with_database, font=("Helvetica", 14), bg="lightblue")
        self.db_compare_button.pack(pady=20)

    def clear_content_frame(self):
        """Clear the content frame of any widgets."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def select_video1(self):
        self.video1_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.video1_path:
            # Store the selected video into 'data/videos/' folder
            self.store_video(self.video1_path)
            self.video1_name_label.config(text=f"Selected: {os.path.basename(self.video1_path)}")

    def select_video2(self):
        self.video2_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.video2_path:
            # Store the selected video into 'data/videos/' folder
            self.store_video(self.video2_path)
            self.video2_name_label.config(text=f"Selected: {os.path.basename(self.video2_path)}")

    def select_video_for_db(self):
        self.db_video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.db_video_path:
            # Store the selected video into 'data/videos/' folder
            self.store_video(self.db_video_path)
            self.db_video_name_label.config(text=f"Selected: {os.path.basename(self.db_video_path)}")

    def store_video(self, video_path):
        """Copy the selected video to the data/videos directory."""
        destination_folder = 'data/videos'  # Specify where to store videos
        os.makedirs(destination_folder, exist_ok=True)  # Create the folder if it doesn't exist
        
        # Create a path for the new file in the destination
        destination_path = os.path.join(destination_folder, os.path.basename(video_path))

        # Copy the video to the destination folder
        try:
            shutil.copy(video_path, destination_path)
            print(f"Video {os.path.basename(video_path)} copied to {destination_path}")  # For debugging
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy video: {e}")
            print(e)

    def extract_and_feature(self, video_path, video_label):
        output_dir = f"data/frames/{video_label}"
        try:
            print(f"Extracting frames from: {video_path}")
            if not os.path.isfile(video_path):
                raise OSError(f"File not found: {video_path}")
            extract_frames(video_path, output_dir, fps=1)  # Frame per seconds:
            features = extract_features_from_frames(output_dir)
            return features
        except OSError as e:
            messagebox.showerror("File Not Found", str(e))
            print(e)  # Print exception for debugging
            return None

    def show_loading(self):
        """Show loading message and progress bar while processing."""
        self.loading_frame = tk.Frame(self.content_frame)
        self.loading_frame.pack(pady=20)

        self.loading_label = tk.Label(self.loading_frame, text="Processing...", font=("Helvetica", 14), bg="yellow")
        self.loading_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(self.loading_frame, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(pady=10, fill=tk.X)
        self.progress_bar.start()  # Start the progress bar

    def hide_loading(self):
        """Hide the loading message and progress bar."""
        self.loading_frame.pack_forget()  # Hide the entire loading frame

    def compare_two_videos(self):
        if not hasattr(self, 'video1_path') or not hasattr(self, 'video2_path'):
            messagebox.showwarning("Input Error", "Please select both videos before comparing.")
            return

        self.show_loading()  # Show loading indicator
        threading.Thread(target=self.process_comparison_videos).start()

    def process_comparison_videos(self):
        try:
            features1 = self.extract_and_feature(self.video1_path, 'video1')
            features2 = self.extract_and_feature(self.video2_path, 'video2')

            if features1 is None or features2 is None:
                return  # Exit if one of the features could not be extracted

            is_plagiarized, similarity = calculate_similarity(features1, features2)
            similarity_percentage = similarity * 100  # Convert to percentage

            # Store comparison in the database
            insert_video_comparison(self.conn, 
                                    os.path.basename(self.video1_path), 
                                    self.video1_path, 
                                    os.path.basename(self.video2_path), 
                                    self.video2_path, 
                                    similarity, 
                                    'Yes' if is_plagiarized else 'No', 
                                    similarity_percentage)

            # Show results in a report window
            self.show_report_window(
                video1=os.path.basename(self.video1_path),
                video2=os.path.basename(self.video2_path),
                similarity=similarity,
                similarity_percentage=similarity_percentage,
                plagiarism_detected='Yes' if is_plagiarized else 'No'
            )
        finally:
            self.hide_loading()  # Hide loading indicator

    def compare_with_database(self):
        if not hasattr(self, 'db_video_path'):
            messagebox.showwarning("Input Error", "Please select a video for database comparison.")
            return

        self.show_loading()  # Show loading indicator
        threading.Thread(target=self.process_db_comparison).start()

    def process_db_comparison(self):
        try:
            print(f"Video Path for DB Comparison: {self.db_video_path}")

            video_features = self.extract_and_feature(self.db_video_path, 'new_video')

            if video_features is None:
                return  # Exit if features could not be extracted

            # Get all comparison entries from the database
            comparisons = get_all_comparisons(self.conn)

            max_similarity = 0
            matched_video = ""  # The name of the video with the highest similarity
            plagiarism_detected = False  # To indicate if plagiarism was detected

            print("Starting comparisons with database videos...")

            for video in comparisons:
                video1_name, video1_path, _, _, _ = video  # Access video records
                
                # Define the correct path to search for videos in the data/videos directory
                video1_full_path = os.path.join('data/videos', video1_name)

                # Debug: Print each video being compared
                print(f"Comparing with Database Video: {video1_name} at {video1_full_path}")

                # Check if the database path is correct
                if not os.path.isfile(video1_full_path):
                    print(f"Database video file does not exist: {video1_full_path}")
                    continue  # Skip this comparison if the file does not exist

                # Extract features for the current video in the database
                db_features = self.extract_and_feature(video1_full_path, 'db_video')

                if db_features is None:
                    print(f"Skipping comparison for {video1_name} due to feature extraction failure.")
                    continue  # Skip this comparison if features cannot be extracted

                # Calculate similarity
                is_plagiarized, similarity = calculate_similarity(video_features, db_features)

                # Check if this is the highest similarity so far
                if similarity > max_similarity:
                    max_similarity = similarity
                    matched_video = video1_name  # Update matched video name
                    plagiarism_detected = is_plagiarized  # Update plagiarism detected status

            # Report if a match was found
            if matched_video:
                # Calculate similarity percentage
                similarity_percentage = max_similarity * 100

                # Store result in the database
                insert_video_comparison(self.conn, 
                                        os.path.basename(self.db_video_path), 
                                        self.db_video_path, 
                                        matched_video, 
                                        None,  # No second video for DB comparison
                                        max_similarity, 
                                        'Yes' if plagiarism_detected else 'No', 
                                        similarity_percentage)

                # Show results in a report window
                self.show_report_window(
                    video1=os.path.basename(self.db_video_path),
                    video2=matched_video,
                    similarity=max_similarity,
                    similarity_percentage=similarity_percentage,
                    plagiarism_detected='Yes' if plagiarism_detected else 'No'
                )
            else:
                messagebox.showinfo("No Match", "No matching video found in the database.")
        finally:
            self.hide_loading()  # Hide loading indicator

    def show_report_window(self, video1, video2, similarity, similarity_percentage, plagiarism_detected):
        """Display the comparison result in a new window."""
        report_window = tk.Toplevel(self.master)
        report_window.title("Comparison Result")
        report_window.geometry("400x300")

        report_text = (
            f"Video 1: {video1}\n"
            f"Video 2: {video2}\n"
            f"Similarity Score: {similarity:.2f}\n"
            f"Similarity Percentage: {similarity_percentage:.2f}%\n"
            f"Plagiarism Detected: {plagiarism_detected}\n"
        )

        report_label = tk.Label(report_window, text=report_text, font=("Helvetica", 14), justify="left")
        report_label.pack(pady=20)

        close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
        close_button.pack(pady=(10, 20))

    def show_past_results(self):
        # Clear current content
        self.clear_content_frame()

        # Create a new frame to display past results
        past_results_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        past_results_frame.pack(pady=20)

        # Create a label to indicate past results
        label = tk.Label(past_results_frame, text="Past Video Comparisons", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

         # Create Treeview to show results
        self.results_treeview = ttk.Treeview(past_results_frame, columns=("Video 1",  "Video 2", "Similarity Percentage", "Plagiarism Detected"), show='headings')
        self.results_treeview.heading("Video 1", text="Video 1")
        self.results_treeview.heading("Video 2", text="Video 2")
        self.results_treeview.heading("Similarity Percentage", text="Similarity Percentage")

        self.results_treeview.heading("Plagiarism Detected", text="Plagiarism Detected")

        # Configure the width of each column
        self.results_treeview.column("Video 1", width=150)
        self.results_treeview.column("Video 2", width=150)
        self.results_treeview.column("Similarity Percentage", width=160)
        self.results_treeview.column("Plagiarism Detected", width=140)

        self.results_treeview.pack(expand=True, fill=tk.BOTH)

        # Fetch and display past results
        results = get_all_comparisons(self.conn)
        for row in results:
            self.results_treeview.insert("", tk.END, values=row)  # Insert the entire row returned from the DB

        # Back Button
        back_button = tk.Button(past_results_frame, text="Back", command=self.setup_video_selection, bg="lightblue")
        back_button.pack(pady=10)

    def exit_program(self):
        self.master.quit()  # Properly exit the application

def main():
    root = tk.Tk()
    app = VideoPlagiarismCheckerGUI(root, None)  # Pass None here, the actual connection is passed in main.py
    root.mainloop()

if __name__ == "__main__":
    main()
