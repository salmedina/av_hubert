from pathlib import Path
import subprocess
import json


def get_video_duration(video_path):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", video_path])
    ffprobe_data = json.loads(out)
    return float(ffprobe_data["format"]["duration"])


def read_text(video_path):
    text_path = video_path.with_suffix('.txt')
    with open(text_path) as text_file:
        lines = text_file.readlines()
        transcript = lines[0].strip().replace('Text:  ', '')
        conf_id = lines[1].strip().replace('Conf:  ', '')
        return transcript, conf_id


if __name__ == "__main__":
    lrs3_dir = Path('/mnt/Alfheim/Data/LRS3/test')
    output_path = Path('lrs3_durations.tsv')

    duration_list = list()
    lines = list()
    for mp4_path in lrs3_dir.glob('*/*.mp4'):
        video_duration = get_video_duration(mp4_path)
        transcript, conf_id = read_text(mp4_path)
        transcript = transcript.replace('\t', ' ')
        duration_list.append(video_duration)
        line = f'{mp4_path.relative_to(lrs3_dir).with_suffix("")}\t{video_duration:.03f}\t{conf_id}\t{transcript}'
        lines.append(line)
        print(line)

    with open(output_path, 'w') as out_file:
        out_file.write('\n'.join(lines))

    print(f'Mean Duration:  {sum(duration_list) / len(duration_list):.2f} seconds')
    print(f'Total Duration: {sum(duration_list) / 3600:.2f} hours')
