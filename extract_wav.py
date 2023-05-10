from pathlib import Path
import subprocess
import json


def get_video_duration(video_path):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", video_path])
    ffprobe_data = json.loads(out)
    return float(ffprobe_data["format"]["duration"])


def extract_audio(video_path):
    audio_path = video_path.with_suffix('.wav')
    subprocess.check_output(["ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path])
    return audio_path


if __name__ == "__main__":
    lrs3_dir = Path('/mnt/Alfheim/Data/LRS3/test')
    output_path = Path('lrs3_durations.tsv')

    duration_list = list()
    lines = list()
    for mp4_path in lrs3_dir.glob('*/*.mp4'):
        video_duration = get_video_duration(mp4_path)
        duration_list.append(video_duration)
        line = f'{mp4_path.relative_to(lrs3_dir)}\t{video_duration:.03f}'
        lines.append(line)
        print(line)
        extract_audio(mp4_path)

    with open(output_path, 'w') as out_file:
        out_file.write('\n'.join(lines))

    print(f'Mean Duration:  {sum(duration_list) / len(duration_list):.2f} seconds')
    print(f'Total Duration: {sum(duration_list) / 3600:.2f} hours')
