import cv2, os
import numpy as np
import sys
import pickle

from config import Config

def process_frame(frame, N, M):
    height, width = frame.shape[:2]
    block_height, block_width = height // N, width // M
    
    centroids_matrix = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            block = frame[i*block_height:(i+1)*block_height, j*block_width:(j+1)*block_width]
            centroids_matrix[i, j] = calculate_gradient_centroids(block)
    return centroids_matrix

def calculate_gradient_centroids(block):
    gx, gy = cv2.Sobel(block, cv2.CV_32F, 1, 0), cv2.Sobel(block, cv2.CV_32F, 0, 1)
    magnitude, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    centroid = np.mean(angle[magnitude > np.mean(magnitude)])
    return centroid

def generate_fingerprints_from_video(file_path, FPS, W, H, N, M):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {file_path}")
        sys.exit(1)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(np.round(fps / FPS))
    
    fingerprints = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = cv2.resize(gray_frame, (W, H))
            fingerprint = process_frame(resized_frame, N, M)
            fingerprints.append(fingerprint)
            
        frame_count += 1

    cap.release()
    return fingerprints

if __name__ == '__main__':
    video_file = sys.argv[1]
    video_name = os.path.basename(video_file).split('.')[0]
    output_dir = f'./fingerprints/{video_name}'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, fingerprint in enumerate(generate_fingerprints_from_video(video_file, M=Config.M, N=Config.N, H=Config.H, W=Config.W, FPS=Config.FPS)):
        fingerprint_path = os.path.join(output_dir, f'{index}.pkl')
        with open(fingerprint_path, 'wb') as f:
            print(fingerprint)
            pickle.dump(fingerprint, f)
