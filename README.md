# NotebookLM Video Splitter
<img width="804" height="289" alt="image" src="https://github.com/user-attachments/assets/713fef03-0332-48f2-9ac9-42a211140f5d" />

<img width="921" height="148" alt="image" src="https://github.com/user-attachments/assets/d35ab02f-6e74-4401-9773-d3be83d47b0e" />

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
