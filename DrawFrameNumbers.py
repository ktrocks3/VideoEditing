import os, cv2

if __name__ == '__main__':
    directory = input('Please enter the directory path (Leave blank for /Inputs): ')
    directory = directory if directory != '' else 'Inputs'
    filename = input('Enter the file name: ')
    path = os.path.abspath(os.path.join(directory, filename))
    assert os.path.exists(path) and os.path.isfile(path), "File does not exist"
    font = cv2.FONT_HERSHEY_SIMPLEX

    os.makedirs('Outputs', exist_ok=True)

    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output = cv2.VideoWriter(
        os.path.join('Outputs', f'labeled_{filename}'),
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    success, frame_number = True, 0
    while success:
        success, frame = video.read()
        if not success:
            break
        cv2.putText(frame, str(frame_number), (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        output.write(frame)
        frame_number += 1

    video.release()
    output.release()
    cv2.destroyAllWindows()