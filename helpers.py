from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tempfile
import os
import subprocess
import yt_dlp
import cv2
from ultralytics import YOLO



def get_youtube_stream_url(youtube_url):
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'no_warnings': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info['url']
    except Exception as e:
        return None

# Function to load the model
def load_model():
    # Load YOLO model
    return YOLO("yolov8n.pt")

# Function to perform prediction and visually annotate the image
def predict_and_annotate(model, image):
    results = model(image)
    detected_class_indices = results[0].boxes.cls.cpu().numpy().astype(int)
    detected_class_names = [results[0].names[i] for i in detected_class_indices]
    bounding_boxes = results[0].boxes.xyxy.cpu().numpy()

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 40)  # Adjust font path and size
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]

    for i, (class_name, bbox) in enumerate(zip(detected_class_names, bounding_boxes)):
        color = colors[i % len(colors)]
        draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline=color, width=3)
        text_size = draw.textsize(class_name, font=font)
        draw.text((bbox[0], bbox[1] - text_size[1]), class_name, fill=color, font=font)

    return image


def process_video(video_file, model):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        # Save uploaded video to a temporary file
        tfile.write(video_file.read())
        tfile.flush()
        video_path = tfile.name

    # Initialize video capture
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        tfile.close()  # Clean up temporary file
        raise ValueError("Could not open video source")

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    frame_limit = fps * 5 # Limit processing to the first 10 seconds
    print(frame_limit)
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as processed_video_temp:
        processed_video_path = processed_video_temp.name
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

        frame_count = 0
        while vid.isOpened() and frame_count < frame_limit:
            ret, frame = vid.read()
            if not ret:
                break

            # Convert frame to Image for YOLO detection
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            results = model(image)
            detected_class_indices = results[0].boxes.cls.cpu().numpy().astype(int)
            detected_class_names = [results[0].names[i] for i in detected_class_indices]
            bounding_boxes = results[0].boxes.xyxy.cpu().numpy()

            draw = ImageDraw.Draw(image)
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font = ImageFont.truetype(font_path, 30)
            colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]

            for i, (class_name, bbox) in enumerate(zip(detected_class_names, bounding_boxes)):
                color = colors[i % len(colors)]
                draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline=color, width=2)
                draw.text((bbox[0], bbox[1]), f"{class_name}", fill=color, font=font)

            # Convert back to BGR for OpenCV
            final_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            out.write(final_frame)
            frame_count += 1

        vid.release()
        out.release()

    # Convert processed video to H.264 codec using ffmpeg
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as h264_video_temp:
        h264_video_path = h264_video_temp.name
        subprocess.run([
            'ffmpeg', '-y', '-i', processed_video_path, '-vcodec', 'libx264', '-acodec', 'aac', h264_video_path
        ], check=True)

        # Read the H.264 encoded video file into bytes
        with open(h264_video_path, 'rb') as f:
            video_bytes = f.read()

    # Clean up temporary files
    os.remove(video_path)
    os.remove(processed_video_path)
    os.remove(h264_video_path)

    return video_bytes

def process_youtube_video(video_stream, model):


    # Initialize video capture
    vid = cv2.VideoCapture(video_stream)


    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    frame_limit = fps * 5  # Limit processing to the first 10 seconds
    print(frame_limit)
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as processed_video_temp:
        processed_video_path = processed_video_temp.name
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

        frame_count = 0
        while vid.isOpened() and frame_count < frame_limit:
            ret, frame = vid.read()
            if not ret:
                break

            # Convert frame to Image for YOLO detection
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            results = model(image)
            detected_class_indices = results[0].boxes.cls.cpu().numpy().astype(int)
            detected_class_names = [results[0].names[i] for i in detected_class_indices]
            bounding_boxes = results[0].boxes.xyxy.cpu().numpy()

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 40)
            colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]

            for i, (class_name, bbox) in enumerate(zip(detected_class_names, bounding_boxes)):
                color = colors[i % len(colors)]
                draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline=color, width=3)
                draw.text((bbox[0], bbox[1]), f"{class_name}", fill=color, font=font)

            # Convert back to BGR for OpenCV
            final_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            out.write(final_frame)
            frame_count += 1

        vid.release()
        out.release()

    # Convert processed video to H.264 codec using ffmpeg
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as h264_video_temp:
        h264_video_path = h264_video_temp.name
        subprocess.run([
            'ffmpeg', '-y', '-i', processed_video_path, '-vcodec', 'libx264', '-acodec', 'aac', h264_video_path
        ], check=True)

        # Read the H.264 encoded video file into bytes
        with open(h264_video_path, 'rb') as f:
            video_bytes = f.read()

    # Clean up temporary files
    os.remove(processed_video_path)
    os.remove(h264_video_path)

    return video_bytes