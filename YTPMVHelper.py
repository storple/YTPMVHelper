import opentimelineio as otio
import os
import mido
import argparse

parser = argparse.ArgumentParser(description="YTPMV Helper Program")
parser.add_argument("--midi", type=str, help="Path to the MIDI file")
parser.add_argument("--video", type=str, help="Path to the video file")
parser.add_argument("--bpm", type=float, help="Beats per minute")
parser.add_argument("--tpb", type=float, help="Ticks per beat")
parser.add_argument("--frame-rate", type=float, help="Frame rate of the video")
parser.add_argument("--output", type=str, help="Output filename for the OTIO file", default="Timeline.otio")

args = parser.parse_args()

tpb = args.tpb
bpm = args.bpm
frame_rate = args.frame_rate
midi_file_path = args.midi
video_file_path = args.video
otio_path = args.output

midi_file_path = os.path.normpath(midi_file_path)
video_file_path = os.path.normpath(video_file_path)
if not otio_path.endswith(".otio"): otio_path += ".otio"

if not os.path.exists(midi_file_path):
    raise FileNotFoundError(f"Midi file not found: {midi_file_path}")
if not os.path.exists(video_file_path):
    raise FileNotFoundError(f"Video file not found: {video_file_path}")

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


midi_start_times = extract_note_start_times(midi_file_path)
print("Note start times saved.")


timeline = otio.schema.Timeline("Temporary Timeline")
video_track = otio.schema.Track(kind=otio.schema.TrackKind.Video)
timeline.tracks.append(video_track)

for i, start_frame in enumerate(midi_start_times):

    duration_frames = midi_start_times[i+1] - start_frame if i < len(midi_start_times) - 1 else 60

    # Create an external reference for the video file
    external_ref = otio.schema.ExternalReference(
        target_url=video_file_path,
        available_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(duration_frames, frame_rate)
        )
    )

    # Create a new clip with the media reference
    clip = otio.schema.Clip(
        name=f"Clip_{i}",
        media_reference=external_ref,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(duration_frames, frame_rate)
        )
    )

    # Flip every other clip
    if i % 2 == 1:
        flip_effect = otio.schema.Effect(
            name="",
            effect_name="Resolve Effect",
            metadata={"Resolve_OTIO": {"Effect Name": "Transform","Enabled": True,"Name": "Transform","Parameters": [{"Default Parameter Value": False,"Parameter ID": "transformationFlipX","Parameter Value": True,"Variant Type": "Bool"}],"Type": 2}}
        )
        clip.effects.append(flip_effect) 

    timeline.tracks[0].append(clip)

# Export the OTIO timeline
otio.adapters.write_to_file(timeline, otio_path)

print(f"Exported OTIO to {otio_path}")
