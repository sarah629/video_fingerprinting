from scipy.spatial import distance
import pickle
import numpy as np


def load_fingerprint(file_path: str) -> np.ndarray:
    with open(file_path, 'rb') as file:
        fingerprint = pickle.load(file)
    return fingerprint


def match_fingerprints(query_fingerprint: np.ndarray, candidate_fingerprint: np.ndarray) -> float:
    return distance.euclidean(query_fingerprint, candidate_fingerprint)


if __name__ == '__main__':
    query_video_fingerprint_path = '../fingerprints/inputs/0.pkl'
    candidate_video_fingerprint_path = '../fingerprints/inputs/0.pkl'

    query_fingerprint = load_fingerprint(query_video_fingerprint_path)
    candidate_fingerprint = load_fingerprint(candidate_video_fingerprint_path)
    match_score = match_fingerprints(query_fingerprint, candidate_fingerprint)
    print(f"Match score: {match_score}")
