import tkinter as tk
from tkinter import ttk
import cv2

class VideoDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem de afisare video pe ecrane multiple")

        self.config = {
            'num_monitors': 2,
            'resolution': (1920, 1080),
            'video_path': ''
        }

        self.cap = None

        self.setup_ui()

    def setup_ui(self):
        # Crearea etichetelor și câmpurilor de introducere pentru configurații
        self.num_monitors_label = ttk.Label(self.root, text="Numar de monitoare:")
        self.num_monitors_label.pack()

        self.num_monitors_entry = ttk.Entry(self.root, width=5)
        self.num_monitors_entry.pack()
        self.num_monitors_entry.insert(0, self.config['num_monitors'])

        self.resolution_label = ttk.Label(self.root, text="Rezolutie: 1920x1080")
        self.resolution_label.pack()

        self.video_path_label = ttk.Label(self.root, text="Video Link:")
        self.video_path_label.pack()

        self.video_path_entry = ttk.Entry(self.root, width=50)
        self.video_path_entry.pack()
        self.video_path_entry.insert(0, self.config['video_path'])

        # Buton pentru încărcarea videoului
        self.load_button = ttk.Button(self.root, text="Incarcare Video", command=self.load_video)
        self.load_button.pack()

        # Buton pentru redarea videoului
        self.play_button = ttk.Button(self.root, text="Play Video", command=self.play_video)
        self.play_button.pack()

    def load_video(self):
        # Funcția care se apelează la apăsarea butonului "Incarcare Video"
        # Obține calea către videoul dorit și inițializează captura videoului
        self.config['video_path'] = self.video_path_entry.get()
        self.cap = cv2.VideoCapture(self.config['video_path'])
        self.config['num_monitors'] = int(self.num_monitors_entry.get())

    def play_video(self):
        # Funcția care se apelează la apăsarea butonului "Play Video"
        if self.cap is None:
            return
        
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        frame_size = (frame_width, frame_height)
        
        # Calculează dimensiunile fiecărui cadru video pentru fiecare monitor
        monitor_cols = int(self.config['num_monitors'] ** 0.5)
        monitor_rows = (self.config['num_monitors'] + monitor_cols - 1) // monitor_cols
        monitor_frame_width = frame_width // monitor_cols
        monitor_frame_height = frame_height // monitor_rows
        
        # Redimensionează fereastra pentru fiecare monitor la dimensiunea cadrelor video
        windows = [cv2.namedWindow(f"Monitor {i}", cv2.WINDOW_NORMAL) for i in range(self.config['num_monitors'])]
        for window in windows:
            cv2.resizeWindow(window, monitor_frame_width, monitor_frame_height)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Afișează fiecare cadru video pe fiecare fereastră de monitor
            for i in range(self.config['num_monitors']):
                col = i % monitor_cols
                row = i // monitor_cols
                start_x = col * monitor_frame_width
                start_y = row * monitor_frame_height
                end_x = start_x + monitor_frame_width
                end_y = start_y + monitor_frame_height
                monitor_frame = frame[start_y:end_y, start_x:end_x, :]
                cv2.imshow(f"Monitor {i}", monitor_frame)
            
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDisplayApp(root)
    root.mainloop()
