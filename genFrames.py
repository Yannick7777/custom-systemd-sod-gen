import cv2
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import argparse


def rgb_to_ascii(frame):
    ascii_chars = "@#%*+:-. "

    ascii_frame = ""
    for row in frame:
        for pixel in row:
            intensity = sum(pixel) / 3
            index = int((intensity / 255) * (len(ascii_chars) - 1))
            ascii_frame += ascii_chars[index]

    return ascii_frame


def process_video(video_path, output_path, n):
    clip = VideoFileClip(video_path)

    with open(output_path, 'w') as text_file:
        # Iterate every n-th frame + Progress bar
        for i, frame in tqdm(enumerate(clip.iter_frames(fps=clip.fps)), total=int(clip.duration * clip.fps),
                             desc="Processing Frames"):
            if i % n == 0:
                # Resizing
                frame = cv2.resize(frame, (160, 50))
                # Convert frame w/ function
                ascii_frame = rgb_to_ascii(frame)
                text_file.write(ascii_frame)
                text_file.write('=')

    clip.close()
    print(f"Every {n}-th frame written to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert video to ASCII art and save it")

    parser.add_argument("-n", "--nth_frame", type=int, default=1, help="Process every n-th frame (default: 1)")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("output_path", type=str, default="frames.txt", help="Path to the output file")

    args = parser.parse_args()
    process_video(args.video_path, args.output_path, args.nth_frame)
