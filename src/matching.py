from scipy.spatial import distance
import pickle
import numpy as np
import sqlite3
import sys
from config import Config
from generation import generate_fingerprints_from_video


def load_fingerprint(file_path: str) -> np.ndarray:
    with open(file_path, "rb") as file:
        fingerprint = pickle.load(file)
    return fingerprint


def match_fingerprints(
    query_fingerprint: np.ndarray, candidate_fingerprint: np.ndarray
) -> float:
    return distance.euclidean(query_fingerprint, candidate_fingerprint)


scores = {}


def query_with_logic(conn, input_fingerprints, logic_func):
    cur = conn.cursor()

    M = len(input_fingerprints)
    i = 0

    while True:
        query = f"SELECT * FROM data LIMIT {M} OFFSET {M+i}"

        i += 1

        cur.execute(query)

        rows = cur.fetchall()

        if not rows:
            break

        logic_func(input_fingerprints, rows)

    conn.close()

    print({[key]: np.mean(value) for key, value in scores})


def compute_scores(input_fingerprints, query):
    for q, f in zip(query, input_fingerprints):
        video_name, _, fingerprint = q

        score = match_fingerprints(fingerprint, f)

        if scores[video_name]:
            scores[video_name].append(score)
        else:
            scores[video_name] = [score]


if __name__ == "__main__":
    input_path = sys.argv[1]
    db_path = sys.argv[2]

    input_fingerprint = generate_fingerprints_from_video(
        input_path, M=Config.M, N=Config.N, H=Config.H, W=Config.W, FPS=Config.FPS
    )

    conn = sqlite3.connect(f"{db_path}/{Config.DB}")

    query_with_logic(conn, input_fingerprint, compute_scores)
