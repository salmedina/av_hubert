from gen_subword import gen_vocab
from pathlib import Path


def main():
    transcript_path = Path('/mnt/Underworld/EPIC/Data/SpeechAnimation/Processed/index/test_text.lst')
    output_prefix = Path('spm_unigram_1000_test')
    gen_vocab(transcript_path, output_prefix, 'unigram', vocab_size=1000)

    vocab_path = output_prefix.with_suffix('.vocab')
    symbols = None
    with open(vocab_path) as vocab_file:
        symbols = [line.strip().split('\t')[0].replace('_', '') for line in vocab_file.readlines()]

    if symbols is not None:
        symbols_path = output_prefix.with_suffix('.wrd')
        with open(symbols_path, 'w') as sym_file:
            sym_file.write('\n'.join(symbols))


if __name__ == '__main__':
    main()