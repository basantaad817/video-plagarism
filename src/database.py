import sqlite3

def create_connection(db_file):
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(db_file, check_same_thread=False)
    return conn

def create_table(conn):
    """Create a table for storing video information and comparison results."""
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video1_name TEXT NOT NULL,
                video1_path TEXT NOT NULL,
                video2_name TEXT,
                video2_path TEXT,
                similarity_score REAL NOT NULL,
                plagiarism_detected TEXT NOT NULL,  -- "Yes" or "No"
                similarity_percentage DECIMAL(5, 2) NOT NULL  -- Similarity as percentage with 2 decimal places
            )
        ''')

def insert_video_comparison(conn, video1_name, video1_path, video2_name, video2_path, similarity_score, plagiarism_detected, similarity_percentage):
    """Insert a record of video comparison results."""
    with conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO videos (video1_name, video1_path, video2_name, video2_path, similarity_score, plagiarism_detected, similarity_percentage) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                    (video1_name, video1_path, video2_name, video2_path, similarity_score, plagiarism_detected, similarity_percentage))

def get_all_comparisons(conn):
    """Retrieve all comparison results from the database."""
    cur = conn.cursor()
    cur.execute('SELECT video1_name, video2_name, similarity_score, plagiarism_detected, similarity_percentage FROM videos ORDER BY id DESC')
    return cur.fetchall()
