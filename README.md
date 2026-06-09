# NotebookLM Video Splitter

A simple python script that splits long videos into fixed-length segments using ffmpeg.

Built because notebookLM has limits on video length (200MB), and I wanted an easy way to process long lectures and recordings.

## Features

- Split videos into chunks (~30 minutes is default)
- Automatic ffmpeg detection
- Fast splitting using stream copy
- CLI

## Installation

pip install imageio-ffmpeg

## Usage

```python split_video.py lecture.mp4```

```python split_video.py lecture.mp4 --minutes 15```

## Example

Input:
4-hour lecture.mp4

Output:
lecture_part001.mp4
lecture_part002.mp4
lecture_part003.mp4
...
