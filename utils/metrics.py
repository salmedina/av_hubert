import warnings

from typing import List, Union, Dict, Any

from jiwer import transforms as tr
from jiwer.transformations import wer_default, cer_default
from jiwer.process import process_words, process_characters


def calc_wer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate the word error rate (WER) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)

    Returns:
        (float): The word error rate structure of the given reference and
                 hypothesis sentence(s).
    """


    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )
    return output


def calc_cer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = cer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = cer_default,
) -> float:
    """
    Calculate the character error rate (CER) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)

    Returns:
        (float): The character error rate structure of the given reference and
                 hypothesis sentence(s).
    """


    output = process_characters(
        reference, hypothesis, reference_transform, hypothesis_transform
    )
    return output