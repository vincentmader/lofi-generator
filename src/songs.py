#!../.venv/bin/python3

import os
import random
from pydub import AudioSegment
from pydub.playback import play

# Pfad zu den Samples
SAMPLES_DIR = "../tmp/samples/Cymatics - Deluxe Lofi Collection"
OUTPUT_DIR = "../tmp/generated_songs"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to list all audio files in a directory and its subdirectories
def list_audio_files(directory):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                audio_files.append(os.path.join(root, file))
    return audio_files

# Load samples
background_noises = list_audio_files(os.path.join(SAMPLES_DIR, "Cymatics - Deluxe Lofi Collection - FX"))
drum_loops = list_audio_files(os.path.join(SAMPLES_DIR, "Cymatics - Deluxe Lofi Collection - Drum Loops"))
melodic_loops = list_audio_files(os.path.join(SAMPLES_DIR, "Cymatics - Deluxe Lofi Collection - Melodic Loops"))
drum_shots = list_audio_files(os.path.join(SAMPLES_DIR, "Cymatics - Deluxe Lofi Collection - Drum Shots"))

# Helper function to randomize volume
def random_volume(segment, min_db=-15, max_db=0):
    return segment + random.uniform(min_db, max_db)

# Function to create a single Lo-Fi track
def create_lofi_song(output_path):
    song_length = random.randint(60000, 120000)  # Song length in milliseconds (1-2 minutes)

    # Randomly select samples
    background = AudioSegment.from_file(random.choice(background_noises))
    drums = AudioSegment.from_file(random.choice(drum_loops))
    melody = AudioSegment.from_file(random.choice(melodic_loops))
    kick = AudioSegment.from_file(random.choice(drum_shots))

    # Trim to the desired length
    background = background * (song_length // len(background) + 1)
    background = random_volume(background)[:song_length]
    drums = random_volume(drums * (song_length // len(drums) + 1))[:song_length]
    melody = random_volume(melody * (song_length // len(melody) + 1))[:song_length]
    kick = random_volume(kick * (song_length // len(kick) + 1))[:song_length]

    # Layer tracks
    song = background.overlay(drums).overlay(melody).overlay(kick)

    # Export song
    song.export(output_path, format="wav")

# Generate 1000 songs
for i in range(1, 11):
    output_file = os.path.join(OUTPUT_DIR, f"lofi_song_{i}.wav")
    print(f"Generating song {i}: {output_file}")
    create_lofi_song(output_file)

print("Finished generating 1000 Lo-Fi songs.")
