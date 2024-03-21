import os
import pickle
import sqlite3
import sys
from tqdm import tqdm
from config import Config


def load_and_store(folder_path, conn):
    cur = conn.cursor()

    cur.execute(
        """
      CREATE TABLE IF NOT EXISTS data (
          video_name TEXT,
          id INTEGER,
          data BLOB
      );
      """
    )

    videos = os.listdir(folder_path)

    for video_idx in tqdm(range(len(videos))):
        video_name = videos[video_idx]
        video_path = os.path.join(folder_path, video_name)
        if os.path.isdir(video_path):

            fingerprints = os.listdir(video_path)

            for fingerprint_idx in tqdm(range(len(fingerprints))):
                filename = fingerprints[fingerprint_idx]

                if filename.endswith(".pkl"):
                    full_path = os.path.join(video_path, filename)
                    with open(full_path, "rb") as f:
                        data = pickle.load(f)

                    file_id = int(filename.split(".")[0])

                    data_bytes = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

                    cur.execute(
                        "INSERT INTO data (video_name, id, data) VALUES (?, ?, ?)",
                        (video_name, file_id, data_bytes),
                    )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    folder_path = sys.argv[1]
    db_path = sys.argv[2]

    conn = sqlite3.connect(f"{db_path}/{Config.DB}")
    print("connection successful ", conn)

    load_and_store(folder_path, conn)

    # cur.execute("SELECT * FROM data LIMIT 10")

    # rows = cur.fetchall()

    # print(pickle.loads(rows[2][2]))
