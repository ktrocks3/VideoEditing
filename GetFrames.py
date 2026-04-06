import os
import cv2
import math
import numpy as np


def best_grid(n, tile_w, tile_h):
    """
    Pick cols/rows so the final collage is as close to square as possible.
    """
    best = None

    for cols in range(1, n + 1):
        rows = math.ceil(n / cols)
        width = cols * tile_w
        height = rows * tile_h
        score = abs(width - height)  # closer to square is better

        if best is None or score < best[0]:
            best = (score, cols, rows)

    return best[1], best[2]


def make_collage(frames, padding=8, bg_color=(255, 255, 255), scale=0.25):
    if not frames:
        raise ValueError("No frames to combine")

    # Original frame size
    h, w = frames[0].shape[:2]

    # Resize each tile so the final image is manageable
    tile_w = max(1, int(w * scale))
    tile_h = max(1, int(h * scale))

    resized = [cv2.resize(frame, (tile_w, tile_h)) for frame in frames]

    cols, rows = best_grid(len(resized), tile_w, tile_h)

    canvas_w = cols * tile_w + (cols + 1) * padding
    canvas_h = rows * tile_h + (rows + 1) * padding
    canvas = np.full((canvas_h, canvas_w, 3), bg_color, dtype=np.uint8)

    for i, frame in enumerate(resized):
        r = i // cols
        c = i % cols
        x = padding + c * (tile_w + padding)
        y = padding + r * (tile_h + padding)
        canvas[y:y + tile_h, x:x + tile_w] = frame

    return canvas


if __name__ == '__main__':
    directory = input('Please enter the directory path (leave blank for Inputs): ').strip()
    directory = directory if directory else 'Inputs'

    filename = input('Enter the file name: ').strip()
    path = os.path.abspath(os.path.join(directory, filename))

    assert os.path.exists(path) and os.path.isfile(path), "File does not exist"

    os.makedirs('Outputs', exist_ok=True)

    starting_frame = int(input('Please enter the starting frame (0-based): '))
    ending_frame = int(input('Please enter the ending frame (-1 for end of video): '))

    video = cv2.VideoCapture(path)
    assert video.isOpened(), "Could not open video"

    frames = []
    frame_index = 0

    while True:
        success, frame = video.read()
        if not success:
            break

        if frame_index < starting_frame:
            frame_index += 1
            continue

        if ending_frame != -1 and frame_index > ending_frame:
            break

        frames.append(frame)
        frame_index += 1

    video.release()

    if not frames:
        raise ValueError("No frames were extracted. Check your start/end frame values.")

    collage = make_collage(frames, padding=8, scale=0.25)

    output_path = os.path.join('Outputs', 'collage.jpg')
    cv2.imwrite(output_path, collage)

    print(f"Saved collage to {output_path}")
    print(f"Collage shape: {collage.shape[1]}x{collage.shape[0]}")