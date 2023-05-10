from pathlib import Path
from utils.metrics import calc_cer
from utils.text import normalize_text


def main():
    ref_path = '/mnt/local/salmedina/Data/Processed/index/transcripts.csv'
    ref_dict = dict()
    for entry in [l.strip().split('\t') for l in open(ref_path).readlines()][1:]:
        ref_dict[entry[0]] = entry[1]

    vsr_dir = Path('/mnt/local/salmedina/Data/Renders/vsr/original_tsv')
    wer_dir = Path('/mnt/local/salmedina/Data/Renders/vsr/cer_b40_l200')

    wer_dir.mkdir(parents=True, exist_ok=True)

    for tsv_path in vsr_dir.glob('*.tsv'):
        output_path = wer_dir / tsv_path.name
        lines = list()
        lines.append('\t'.join(['score', 'cer', 'hits', 'sub', 'ins', 'del','hyp']))

        for pred in [l.strip().split('\t') for l in open(tsv_path).readlines()]:    
            sid = tsv_path.stem
            ref = normalize_text(ref_dict[sid])
            hyp = normalize_text(pred[1])

            metrics = calc_cer(ref, hyp)

            lines.append('\t'.join([pred[0],
                                    f'{metrics.cer:.05f}',
                                    f'{metrics.hits}',
                                    f'{metrics.substitutions}',
                                    f'{metrics.insertions}',
                                    f'{metrics.deletions}',
                                    pred[1]]))
        
        with open(output_path, 'w') as output_file:
            output_file.write('\n'.join(lines))


if __name__ == '__main__':
    main()