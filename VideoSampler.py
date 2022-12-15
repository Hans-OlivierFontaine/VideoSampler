from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
import argparse
import cv2
from multiprocessing import Pool, Process

VIDEO_FILE_TYPES = ["AVI", "MP4", "MOV"]


def video_sample(source: Path,
                 output: Path,
                 sampling_rate: int = 5,
                 directories: bool = True):
    cap = cv2.VideoCapture(source.__str__())
    frame_period = 1 / cap.get(cv2.CAP_PROP_FPS)
    sampling_period = 1 / sampling_rate
    time_covered = 0
    assert 1 / frame_period > sampling_rate, f"FPS({1 / frame_period}) should be higher than sampling rate({sampling_rate})"
    i = 0
    while True:
        success, frame = cap.read()
        if time_covered >= i * sampling_period:
            filename = output
            if directories:
                filename = filename / source.stem
            filename = filename / f"{source.stem}{i:05}.png"
            cv2.imwrite(filename=filename.__str__(), img=frame)
            i += 1
        if not success:
            return
        time_covered += frame_period


def operate_gui(opts):
    root = tk.Tk()
    root.withdraw()
    opts.source = askdirectory()
    root.destroy()
    root = tk.Tk()
    root.withdraw()
    opts.output = askdirectory()
    root.destroy()
    root = tk.Tk()
    root.withdraw()
    opts.sampling_rate = simpledialog.askinteger("Image sampling rate", "Image sampling rate")
    root.destroy()
    root = tk.Tk()
    root.withdraw()
    opts.workers = simpledialog.askinteger("Number of workers to handle it", "# workers")
    root.destroy()
    return opts


def parse_opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="VideoSampler", description="")
    parser.add_argument("-s", "--source", type=Path, default=Path(__file__).parent / "data", help="Path to the video files")
    parser.add_argument("-o", "--output", type=Path, default=Path(__file__).parent / "output", help="Path of the output image files")
    parser.add_argument("-r", "--sampling_rate", type=int, default=5, help="Number of frames recorded every second")
    parser.add_argument("-w", "--workers", type=int, default=1, help="Number of workers")
    parser.add_argument("-d", "--directories", action="store_true", help="Arrange the output images in subfolders")
    parser.add_argument("-g", "--gui", action="store_true", help="Use GUI queries")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_opts()
    if args.gui:
        args = operate_gui(opts=args)
    videos = (p.resolve() for p in Path(args.source).rglob("*") if p.suffix[1:].upper() in VIDEO_FILE_TYPES)
    Path(args.output).mkdir(exist_ok=True)
    for video in videos:
        if args.directories:
            (Path(args.output) / video.stem).mkdir(exist_ok=True)
            print(f"Creating new folder for storing {video.stem} frames")
        video_sample(source=video, output=args.output, directories=False)
    # processes = []
    # pool = Pool(processes=args.workers)
