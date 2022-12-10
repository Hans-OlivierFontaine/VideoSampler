from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
import argparse
import cv2
from multiprocessing import Pool, Process

VIDEO_FILE_TYPES = ["AVI", "MP4", "MOV"]


def video_sample(source: Path, output: Path, sampling_rate: int, directories: bool):
    cap = cv2.VideoCapture(source.__str__())
    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    i = 0
    while True:
        flag, frame = cap.read()
        filename = output
        if directories:
            filename = filename / source.stem
            filename = filename / f"i:05"
        cv2.imwrite(filename=filename, img=frame)
        if flag:
            return
        i += 1
    pass


def parse_opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="VideoSampler", description="")
    parser.add_argument("-s", "--source", type=Path, help="Path to the video files")
    parser.add_argument("-o", "--output", type=Path, help="Path of the output image files")
    parser.add_argument("-r", "--sampling_rate", type=int, help="Number of frames recorded every second")
    parser.add_argument("-w", "--workers", type=int, help="Number of workers")
    parser.add_argument("-d", "--directories", action="store_true", help="Arrange the output images in subfolders")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_opts()
    if args.source is None:
        root = tk.Tk()
        root.withdraw()
        args.source = askdirectory()
        root.destroy()
    if args.output is None:
        root = tk.Tk()
        root.withdraw()
        args.output = askdirectory()
        root.destroy()
    if args.sampling_rate is None:
        args.sampling_rate = simpledialog.askinteger("Image sampling rate", "Image sampling rate")
    if args.workers is None:
        args.workers = simpledialog.askinteger("Number of workers to handle it", "# workers")
    videos = (p.resolve() for p in Path(args.source).rglob("**/*") if p.suffix in VIDEO_FILE_TYPES)
    processes = []
    pool = Pool(processes=args.workers)
