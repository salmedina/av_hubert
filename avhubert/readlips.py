import shutil
import tempfile
from argparse import Namespace
from base64 import b64encode
from pathlib import Path

import cv2
import dlib
import hubert
import hubert_asr
import hubert_pretraining
import numpy as np
import skvideo
import skvideo.io
from preparation.align_mouth import (crop_patch, landmarks_interpolate,
                                     write_video_ffmpeg)
from tqdm import tqdm

import fairseq
from fairseq import checkpoint_utils, options, tasks, utils
from fairseq.dataclass.configs import GenerationConfig


def detect_landmark(image, detector, predictor):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rects = detector(gray, 1)
    coords = None
    for (_, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        coords = np.zeros((68, 2), dtype=np.int32)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


def extract_roi(input_video_path, output_video_path, face_predictor_path, mean_face_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_predictor_path)
    STD_SIZE = (256, 256)
    mean_face_landmarks = np.load(mean_face_path)
    stablePntsIDs = [33, 36, 39, 42, 45]
    videogen = skvideo.io.vread(input_video_path)
    frames = np.array([frame for frame in videogen])
    landmarks = []
    landmark = None
    for frame in tqdm(frames):
        landmark = detect_landmark(frame, detector, predictor)
        landmarks.append(landmark)
    preprocessed_landmarks = landmarks_interpolate(landmarks)
    rois = crop_patch(input_video_path,
                      preprocessed_landmarks, mean_face_landmarks, stablePntsIDs, STD_SIZE, 
                      window_margin=12, start_idx=48, stop_idx=68, crop_height=96, crop_width=96)
    write_video_ffmpeg(rois, output_video_path, "/usr/bin/ffmpeg")


def predict(video_path: str, ckpt_path: str, beam_sz: int=20, beam_len: int=20):
    num_frames = int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT))
    tmp_dir = tempfile.mkdtemp()
    tsv_cont = ["/\n", f"test-0\t{video_path}\t{None}\t{num_frames}\t{int(16_000*num_frames/25)}\n"]
    label_cont = ["DUMMY\n"]
    with open(f"{tmp_dir}/test.tsv", "w") as fo:
      fo.write("".join(tsv_cont))
    with open(f"{tmp_dir}/test.wrd", "w") as fo:
      fo.write("".join(label_cont))

    modalities = ["video"]
    gen_subset = "test"
    gen_cfg = GenerationConfig(beam=beam_sz,
                               max_len_b=beam_len)
    models, saved_cfg, task = checkpoint_utils.load_model_ensemble_and_task([ckpt_path])
    models = [model.eval().cuda() for model in models]
    saved_cfg.task.modalities = modalities
    saved_cfg.task.data = tmp_dir
    saved_cfg.task.label_dir = tmp_dir
    task = tasks.setup_task(saved_cfg.task)
    task.load_dataset(gen_subset, task_cfg=saved_cfg.task)
    generator = task.build_generator(models, gen_cfg)

    def decode_fn(x):
        dictionary = task.target_dictionary
        symbols_ignore = generator.symbols_to_strip_from_output
        symbols_ignore.add(dictionary.pad())
        return task.datasets[gen_subset].label_processors[0].decode(x, symbols_ignore)

    itr = task.get_batch_iterator(dataset=task.dataset(gen_subset)).next_epoch_itr(shuffle=False)
    sample = next(itr)
    sample = utils.move_to_cuda(sample)
    hypos = task.inference_step(generator, models, sample)

    shutil.rmtree(tmp_dir)

    decoded_hypos = list()
    for hypo in hypos[0]:
        decoded_hypos.append((hypo['score'], decode_fn(hypo['tokens'].int().cpu())))

    return decoded_hypos


def read_lips(roi_path, ckpt_path, output_path, beam_sz: int=20, beam_len: int=20):
    
    hypos = predict(roi_path.__str__(),
                    ckpt_path.__str__(),
                    beam_sz=beam_sz,
                    beam_len=beam_len)
    
    print(f'Hypothesis:')
    output_lines = list()
    for hypo in hypos:
        line = f'{hypo[0]:.05f}\t{hypo[1]}'
        print(line)
        output_lines.append(line)
    
    with open(output_path, 'w') as output_file:
        output_file.write('\n'.join(output_lines))


if __name__ == '__main__':
    beam_size = 10
    beam_length = 20

    ckpt_path = Path("/home/salmedina/Devel/GH/av_hubert/data/finetune-model.pt")
    face_predictor_path = "/home/salmedina/Devel/GH/av_hubert/data/misc/shape_predictor_68_face_landmarks.dat"
    mean_face_path = "/home/salmedina/Devel/GH/av_hubert/data/misc/20words_mean_face.npy"

    videos_dir = Path("/mnt/local/salmedina/Data/Renders/videos/25fps")
    rois_dir = Path("/mnt/local/salmedina/Data/Renders/videos/rois/video")
    output_dir = Path(f"/mnt/local/salmedina/Data/Renders/vsr/tsv_b{beam_size}_l{beam_length}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for video_path in videos_dir.glob("*.mp4"):
        sample_name = video_path.stem
        roi_path = rois_dir / f"{sample_name}.mp4"
        output_path = output_dir / f"{sample_name}.tsv"
        if not output_path.exists():
            print(f"Processing {sample_name}")
            if not roi_path.exists():
                extract_roi(video_path.__str__(),
                            roi_path,
                            face_predictor_path,
                            mean_face_path)
        read_lips(roi_path,
                    ckpt_path,
                    output_path,
                    beam_sz=beam_size,
                    beam_len=beam_length)
    
    # extract_roi(video_path, roi_path, face_predictor_path, mean_face_path)
    # read_lips(roi_path, ckpt_path, output_path)