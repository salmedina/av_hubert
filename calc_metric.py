import argparse
from pathlib import Path
from utils.metrics import calc_cer, calc_wer
from utils.text import normalize_text
from easydict import EasyDict as edict


def load_transcript(path, type):
    ref_dict = dict()
    if type == 'imt':
        for entry in [l.strip().split('\t') for l in open(path).readlines()][1:]:
            ref_dict[entry[0]] = entry[1]
    elif type == 'lrs3':
        for entry in [l.strip().split('\t') for l in open(path).readlines()]:
            key = entry[0].replace('/', '_')
            ref_dict[key] = entry[2]

    return ref_dict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--epoch', type=int,
                        help='Epoch number to be processed')
    parser.add_argument('-r', '--run_name', type=str, default='bright-rain-92',
                        help='Name of the run to be processed')
    parser.add_argument('-m', '--metric', type=str, default='wer',
                        help='Metric to be computed: cer, wer')
    return parser.parse_args()


def get_metric_func(metric_label):
    if metric_label == 'cer':
        return calc_cer
    elif metric_label == 'wer':
        return calc_wer
    
    return None


def main(args):
    epoch = args.epoch
    run_name = args.run_name
    metric_name = args.metric

    assert metric_name in ['cer', 'wer'], f'Metric has to be wer or cer'
    calc_metric_func = get_metric_func(metric_name)

    transcripts = edict(imt=edict(path='/mnt/local/salmedina/Data/Processed/index/transcripts.csv',
                                  type='imt'),
                        lrs3=edict(path='/mnt/local/salmedina/Data/LRS3/test_index.tsv',
                                  type='lrs3'))

    ref_dict = load_transcript(path=transcripts.lrs3.path,
                               type=transcripts.lrs3.type)

    vsr_dir = Path(f'/mnt/local/salmedina/Output/VSR/lrs3_test/vsr/{run_name}-{epoch}/tsv')
    output_dir = Path(f'/mnt/local/salmedina/Output/VSR/lrs3_test/vsr/{run_name}-{epoch}/{metric_name}')

    output_dir.mkdir(parents=True, exist_ok=True)

    for tsv_path in vsr_dir.glob('*.tsv'):
        output_path = output_dir / tsv_path.name
        lines = list()
        lines.append('\t'.join(['score', metric_name, 'hits', 'sub', 'ins', 'del', 'hyp', 'ref']))

        for pred in [l.strip().split('\t') for l in open(tsv_path).readlines()]:    
            sid = tsv_path.stem
            ref = normalize_text(ref_dict[sid])
            hyp = normalize_text(pred[1])

            metrics = calc_metric_func(ref, hyp)
            if metric_name == 'cer':
                error_rate = metrics.cer
            elif metric_name == 'wer':
                error_rate = metrics.wer

            lines.append('\t'.join([pred[0],
                                    f'{error_rate:.05f}',
                                    f'{metrics.hits}',
                                    f'{metrics.substitutions}',
                                    f'{metrics.insertions}',
                                    f'{metrics.deletions}',
                                    hyp,
                                    ref]))
        
        with open(output_path, 'w') as output_file:
            output_file.write('\n'.join(lines))


if __name__ == '__main__':
    args = parse_args()
    main(args)