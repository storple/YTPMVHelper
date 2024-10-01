import opentimelineio as otio
import os
import mido
import argparse

parser = argparse.ArgumentParser(description="YTPMV Helper Program")
parser.add_argument("--midi-folder", type=str, help="Path to the MIDI folder")
parser.add_argument("--video-folder", type=str, help="Path to the video file folder")
parser.add_argument("--bpm", type=float, help="Beats per minute")
parser.add_argument("--tpb", type=float, help="Ticks per beat")
parser.add_argument("--frame-rate", type=float, help="Frame rate of the video")
parser.add_argument("--output-filename", type=str, help="Output filename", default="Timeline.otio")


args = parser.parse_args()

tpb = args.tpb
bpm = args.bpm
frame_rate = args.frame_rate
midi_folder_path = args.midi_folder
video_folder_path = args.video_folder
output_filename = args.output_filename

midi_folder_path = os.path.normpath(midi_folder_path)
video_folder_path = os.path.normpath(video_folder_path)

if not os.path.exists(midi_folder_path):
    raise FileNotFoundError(f"Midi file not found: {midi_folder_path}")
if not os.path.exists(video_folder_path):
    raise FileNotFoundError(f"Video file not found: {video_folder_path}")

if not output_filename.endswith(".otio"):
    output_filename += ".otio"


def extract_note_start_times(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    note_start_times = []
    current_time = 0
    last_added_time = None  
    for track in midi_file.tracks:
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                converted_time = midi_ticks_to_frames(current_time, tpb, bpm)

                if converted_time != last_added_time:
                    note_start_times.append(converted_time)
                    last_added_time = converted_time 

    return note_start_times

def midi_ticks_to_frames(ticks, tpb, bpm):
    frames = (ticks * frame_rate * 60) / (tpb * bpm)
    return int(round(frames))

timeline = otio.schema.Timeline("Timeline")

for midi_filename in os.listdir(midi_folder_path):
    if midi_filename.endswith(".mid") or midi_filename.endswith(".midi"):
        midi_file_path = os.path.join(midi_folder_path, midi_filename)

        # check for a corresponding video file with the same base name
        base_name = os.path.splitext(midi_filename)[0]
        matching_video_file = None
        for video_filename in os.listdir(video_folder_path):
            if video_filename.startswith(base_name) and video_filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                matching_video_file = os.path.join(video_folder_path, video_filename)
                break

        if not matching_video_file:
            print(f"No matching video found for MIDI file: {midi_filename}")
            continue

        midi_start_times = extract_note_start_times(midi_file_path)
        print(f"Processing {midi_filename} with video {matching_video_file}...")

        # create a new video track for each MIDI/video
        video_track = otio.schema.Track(name=f"Track_{base_name}", kind=otio.schema.TrackKind.Video)

        for i, start_frame in enumerate(midi_start_times):
            duration_frames = midi_start_times[i+1] - start_frame if i < len(midi_start_times) - 1 else 60

            external_ref = otio.schema.ExternalReference(
                target_url=matching_video_file,
                available_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(0, frame_rate),
                    duration=otio.opentime.RationalTime(duration_frames, frame_rate)
                )
            )

            clip = otio.schema.Clip(
                name=f"Clip_{i}",
                media_reference=external_ref,
                source_range=otio.opentime.TimeRange(
                    start_time=otio.opentime.RationalTime(0, frame_rate),
                    duration=otio.opentime.RationalTime(duration_frames, frame_rate)
                )
            )

            # flip every other clip
            if i % 2 == 1:
                flip_effect = otio.schema.Effect(
                    name="",
                    effect_name="Resolve Effect",
                    metadata={"Resolve_OTIO": {"Effect Name": "Transform","Enabled": True,"Name": "Transform","Parameters": [{"Default Parameter Value": False,"Parameter ID": "transformationFlipX","Parameter Value": True,"Variant Type": "Bool"}],"Type": 2}}
                )
                clip.effects.append(flip_effect)

            video_track.append(clip)

        timeline.tracks.append(video_track)

otio.adapters.write_to_file(timeline, output_filename)
print(f"Exported OTIO to {output_filename}")
