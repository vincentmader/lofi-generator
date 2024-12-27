#!../.venv/bin/python3
#!../.venv/bin/python3

import os
import random
import subprocess

# Directory paths
song_dir = "../tmp/generated_songs"
image_dir = "../tmp/generated_images"
output_dir = "../tmp/videos"

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Function to generate a random fitting title for a lowfi song
def generate_random_title():
    # Adjectives array
    adjectives = [
        "Chill", "Dreamy", "Lonely", "Misty", "Fuzzy", "Smooth", "Gentle", 
        "Cosmic", "Wavy", "Serene", "Quiet", "Midnight", "Swaying", "Warm", 
        "Calm", "Vintage", "Ethereal", "Melancholy", "Gentle", "Nostalgic", 
        "Cozy", "Lush", "Peaceful", "Soothing", "Cinematic"
    ]

    # Nouns array
    nouns = [
        "Vibes", "Waves", "Sunset", "Rain", "Skies", "Clouds", "Beats", 
        "Dreams", "Mornings", "Nights", "Days", "Tides", "Lights", "Reflections", 
        "Streets", "Chords", "Feelings", "Moments", "Journey", "Echoes", 
        "Memories", "Horizon", "Scenes", "Visions", "Passages"
    ]

    # Select random adjective and noun
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    # Combine them into a title
    return f"{adjective} {noun}"

# Loop through all songs in the song directory with enumerate to get the index
for idx, song in enumerate(os.listdir(song_dir)):
    song_path = os.path.join(song_dir, song)
    if not os.path.isfile(song_path):
        continue

    # Get the base name of the song (without the extension)
    song_name = os.path.splitext(song)[0]

    # Use the index to generate a unique image name
    image_name = f"lowfi_image_{idx}"

    # Get the corresponding image (same name as generated)
    image_path = os.path.join(image_dir, f"{image_name}.png")

    # Check if the image exists
    if not os.path.isfile(image_path):
        print(f"No image found for {song_name}, skipping...")
        continue

    # Generate a random title for the video
    title = generate_random_title()

    # Get the duration of the song (in seconds)
    result = subprocess.run(
        ['ffmpeg', '-i', song_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    duration_str = result.stderr.decode('utf-8').split('Duration: ')[1].split(',')[0]
    h, m, s = map(float, duration_str.split(':'))
    duration = int(h * 3600 + m * 60 + s)

    # Generate the video using ffmpeg (including audio and image)
    output_video_path = os.path.join(output_dir, f"{song_name}.mp4")
    subprocess.run([
        'ffmpeg', '-loop', '1', '-framerate', '2', '-t', str(duration),
        '-i', image_path, '-i', song_path, '-vf', f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v', 'libx264', '-c:a', 'aac', '-r', '30', '-pix_fmt', 'yuv420p', '-shortest', '-y', output_video_path
    ])

    print(f"Created video for {song_name} with title: {title}")
