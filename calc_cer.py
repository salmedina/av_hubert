from jiwer import cer as calc_cer
from pathlib import Path
from utils.text import normalize_text


def main():
    ref_path = '/mnt/local/salmedina/Data/Processed/index/transcripts.csv'
    ref_dict = dict()
    for entry in [l.strip().split('\t') for l in open(ref_path).readlines()][1:]:
        ref_dict[entry[0]] = entry[1]

    vsr_dir = Path('/mnt/local/salmedina/Data/Renders/vsr/original_tsv')
    vsr_dir = Path('/mnt/local/salmedina/Data/Renders/vsr/tsv_b40_l200')
    wer_dir = Path('/mnt/local/salmedina/Data/Renders/vsr/cer_b40_l200')

    wer_dir.mkdir(parents=True, exist_ok=True)

    for tsv_path in vsr_dir.glob('*.tsv'):
        output_path = wer_dir / tsv_path.name
        lines = list()
        lines.append('\t'.join(['score', 'cer', 'hyp']))

        for pred in [l.strip().split('\t') for l in open(tsv_path).readlines()]:    
            sid = tsv_path.stem
            ref = normalize_text(ref_dict[sid])
            hyp = normalize_text(pred[1])

            lines.append('\t'.join([pred[0], f'{calc_cer(ref, hyp):.05f}', pred[1]]))
        
        with open(output_path, 'w') as output_file:
            output_file.write('\n'.join(lines))


if __name__ == '__main__':
    main()