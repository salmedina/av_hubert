from pathlib import Path


if __name__ == '__main__':
    root_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois')
    name_list_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/names.lst')
    video_frames_count_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/nframes.video.0')
    audio_frames_count_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/nframes.audio.0')
    transcript_path = Path('/mnt/local/salmedina/Data/Processed/index/transcripts.csv')

    train_lst_path = Path('/mnt/local/salmedina/Data/Processed/index/face/train.lst')
    test_lst_path = Path('/mnt/local/salmedina/Data/Processed/index/face/test.lst')
    train_tsv_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/train.tsv')
    test_tsv_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/valid.tsv')
    train_wrd_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/train.wrd')
    test_wrd_path = Path('/mnt/local/salmedina/Data/Renders/videos/rois/valid.wrd')

    # Manifesto
    sid_list = [l.strip() for l in open(name_list_path).readlines()]
    video_frames_list = [l.strip() for l in open(video_frames_count_path).readlines()]
    audio_frames_list = [l.strip() for l in open(audio_frames_count_path).readlines()]

    train_sid_list = [l.strip() for l in open(train_lst_path).readlines()]
    test_sid_list = [l.strip() for l in open(test_lst_path).readlines()]
    
    train_lines = list()
    train_lines.append(str(root_path))
    for sid in train_sid_list:
        sid_idx = sid_list.index(sid)
        video_path = root_path / 'video' / f'{sid}.mp4'
        audio_path = root_path / 'audio' / f'{sid}.wav'
        num_vframes = video_frames_list[sid_idx]
        num_aframes = audio_frames_list[sid_idx]
        line = f'{sid} {video_path}\t{audio_path}\t{num_vframes}\t{num_aframes}'
        train_lines.append(line)
    with open(train_tsv_path, 'w') as output_file:
        output_file.write('\n'.join(train_lines))
    
    test_lines = list()
    test_lines.append(str(root_path))
    for sid in test_sid_list:
        sid_idx = sid_list.index(sid)
        video_path = root_path / 'video' / f'{sid}.mp4'
        audio_path = root_path / 'audio' / f'{sid}.wav'
        num_vframes = video_frames_list[sid_idx]
        num_aframes = audio_frames_list[sid_idx]
        line = f'{sid}\t{video_path}\t{audio_path}\t{num_vframes}\t{num_aframes}'
        test_lines.append(line)
    with open(test_tsv_path, 'w') as output_file:
        output_file.write('\n'.join(test_lines))

    
    # WRD
    transcript_dict = dict()
    for sid, text in [l.strip().split('\t') for l in open(transcript_path).readlines()]:
        transcript_dict[sid] = text
    
    transcript_list = list()
    for sid in train_sid_list:
        transcript_list.append(transcript_dict[sid])
    with open(train_wrd_path, 'w') as output_file:
        output_file.write('\n'.join(transcript_list))
    
    transcript_list = list()
    for sid in test_sid_list:
        transcript_list.append(transcript_dict[sid])
    with open(test_wrd_path, 'w') as output_file:
        output_file.write('\n'.join(transcript_list))
