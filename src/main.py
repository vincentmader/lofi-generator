#!../.venv/bin/python3

import os
from videos import generate_random_title
from songs import create_lofi_song
from images import create_background_image, add_text_to_image

# Directory paths
BASE_DIR = "../tmp"
SONG_DIR = os.path.join(BASE_DIR, "generated_songs")
IMAGE_DIR = os.path.join(BASE_DIR, "generated_images")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")

# Ensure directories exist
for directory in [SONG_DIR, IMAGE_DIR, VIDEO_DIR]:
    os.makedirs(directory, exist_ok=True)

def generate_content():
    # Generate a random title first
    title = generate_random_title()
    print(f"Generated title: {title}")

    # Generate song
    song_path = os.path.join(SONG_DIR, f"{title.replace(' ', '_')}.wav")
    print(f"Generating song: {song_path}")
    create_lofi_song(song_path)

    # Generate image
    image_path = os.path.join(IMAGE_DIR, f"{title.replace(' ', '_')}.png")
    print(f"Generating image: {image_path}")
    background = create_background_image()
    add_text_to_image(background, title)
    background.save(image_path)

    # Generate video using ffmpeg
    output_video_path = os.path.join(VIDEO_DIR, f"{title.replace(' ', '_')}.mp4")
    print(f"Generating video: {output_video_path}")
    
    # Get song duration
    import subprocess
    result = subprocess.run(
        ['ffmpeg', '-i', song_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    duration_str = result.stderr.decode('utf-8').split('Duration: ')[1].split(',')[0]
    h, m, s = map(float, duration_str.split(':'))
    duration = int(h * 3600 + m * 60 + s)

    # Create video
    subprocess.run([
        'ffmpeg', '-loop', '1', '-framerate', '2', '-t', str(duration),
        '-i', image_path, '-i', song_path, 
        '-vf', f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v', 'libx264', '-c:a', 'aac', '-r', '30', '-pix_fmt', 'yuv420p', 
        '-shortest', '-y', output_video_path
    ])

    return {
        'title': title,
        'song_path': song_path,
        'image_path': image_path,
        'video_path': output_video_path
    }

if __name__ == "__main__":
    result = generate_content()
    print("\nGeneration complete!")
    print(f"Title: {result['title']}")
    print(f"Song: {result['song_path']}")
    print(f"Image: {result['image_path']}")
    print(f"Video: {result['video_path']}") 
