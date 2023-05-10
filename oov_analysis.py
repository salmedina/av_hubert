from pathlib import Path
from utils.text import normalize_text


if __name__ == '__main__':
    train_wrd_path = Path('/home/zal/Devel/av_hubert/lrs3.wrd')
    test_wrd_path = Path('/home/zal/Devel/av_hubert/spm_unigram_1000_test.wrd')

    def get_vocab(transcript_path):
        with open(transcript_path) as wrd_file:
            wrd_set = set()
            for sentence in wrd_file.readlines():
                norm_sent = normalize_text(sentence)
                wrd_set.update(norm_sent.split(' '))
            return wrd_set
    
    train_vocab = get_vocab(train_wrd_path)
    test_vocab = get_vocab(test_wrd_path)

    common_words = train_vocab.intersection(test_vocab)
    num_common = len(common_words)
    oov = test_vocab - common_words
    oov_ratio = len(oov) / len(test_vocab)

    print(f'Train tokens:  {len(train_vocab)}')
    print(f'Test tokens:   {len(test_vocab)}')
    print(f'OOV ratio:     {oov_ratio:.04f}')

    