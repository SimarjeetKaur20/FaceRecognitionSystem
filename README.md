# Face Recognition Attendance System

A Python-based face recognition system that uses a webcam to identify registered users and automatically marks their attendance in a SQLite database. Built with OpenCV's LBPH algorithm and structured using Object-Oriented Programming principles.

---

## Features

- **User Registration** — Capture 100 face images via webcam and store user details in the database
- **Model Training** — Train an LBPH (Local Binary Pattern Histogram) face recognition model on the captured dataset
- **Live Face Recognition** — Real-time webcam recognition with bounding boxes and confidence scores
- **Automatic Attendance Marking** — Attendance is recorded the first time a person is recognised each day (no duplicates)
- **Attendance Viewing** — View today's attendance or the full history directly in the terminal
- **CSV Export** — Export attendance records (today / all / per user) to CSV files in the `reports/` folder
- **User Deletion** — Remove a user from the database and delete their face dataset in one step
- **Persistent Label Map** — Label-to-name mapping is saved to `trainer/label_map.json` so recognition stays accurate across restarts

---

## Project Structure

```
FaceRecognitionSystem/
├── main.py                        # CLI entry point (numbered menu)
├── requirements.txt
├── .gitignore
│
├── database/
│   └── database.py                # SQLite wrapper (users + attendance tables)
│
├── services/
│   ├── face_capture.py            # Webcam face image capture
│   ├── face_detector.py           # Standalone face detection (bounding boxes only)
│   ├── face_trainer.py            # LBPH model training + label map persistence
│   ├── face_recognizer.py         # Live recognition + attendance marking
│   ├── user_registration.py       # Registration + deletion orchestration
│   └── attendance_service.py      # Attendance queries + CSV export
│
├── utils/
│   └── report_generator.py        # CSV report writer
│
├── dataset/                       # Face images per person (gitignored)
│   └── <PersonName>/              # 100 grayscale .jpg images per user
│
├── trainer/                       # Generated model files (gitignored)
│   ├── trainer.yml                # Trained LBPH model
│   └── label_map.json             # Label ID → person name mapping
│
├── reports/                       # Exported CSV files (gitignored)
├── attendance/                    # Reserved for future use
└── models/                        # Reserved for future use
```

---

## Database Schema

```sql
-- Registered users
CREATE TABLE users (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT    NOT NULL UNIQUE,
    registration_date TEXT    NOT NULL,
    label_id          INTEGER NOT NULL DEFAULT -1
);

-- Daily attendance log
CREATE TABLE attendance (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    date     TEXT    NOT NULL,          -- DD-MM-YYYY
    time     TEXT    NOT NULL,          -- HH:MM:SS
    status   TEXT    NOT NULL DEFAULT 'Present',
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE (user_id, date)              -- one record per person per day
);
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/SimarjeetKaur20/FaceRecognitionSystem.git
cd FaceRecognitionSystem
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

> Requires Python 3.10+. The key dependency is `opencv-contrib-python` which includes the `cv2.face` LBPH module.

**3. Run the application**
```bash
python main.py
```

---

## Usage

The app runs as a numbered CLI menu:

```
=============================================
   Face Recognition Attendance System
=============================================
  1. Register New User
  2. Train Model
  3. Start Face Recognition (mark attendance)
  4. View Today's Attendance
  5. View All Attendance
  6. Export Today's Attendance to CSV
  7. Export All Attendance to CSV
  8. Delete a User
  9. List All Registered Users
  0. Exit
=============================================
```

**Typical workflow:**
1. Run option `1` to register each person (captures 100 face images via webcam)
2. Run option `2` to train the model (only needed after adding/removing users)
3. Run option `3` to start live recognition — attendance is marked automatically
4. Use options `4–7` to view or export attendance records

---

## Technologies

| Library | Purpose |
|---|---|
| Python 3.10+ | Core language |
| OpenCV (`opencv-contrib-python`) | Face detection (Haar Cascade) + LBPH recognition |
| NumPy | Array handling for training data |
| SQLite3 | Embedded database (built into Python) |

---

## Notes

- The `dataset/` folder and `trainer/` model files are excluded from this repository (`.gitignore`) since they contain personal photos and are generated locally.
- After deleting a user, re-run option `2` (Train Model) to rebuild the model without that person.
- Attendance confidence threshold is set to `80` — lower LBPH confidence = better match.

---

## Author

**Simarjeet Kaur**  
[GitHub](https://github.com/SimarjeetKaur20)
