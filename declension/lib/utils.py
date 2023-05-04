from numpy.random._generator import Generator

from declension.lib.declension_classes import *
from declension.lib.declension_classes import SingleDeclensionPattern
from common.lib.utils import flatten


# todo test it
def filter_by_type(dictionary: Declensions, types: list[DeclensionType]) -> Declensions:
    # 3rd declension is kind of superset of declensions 3rd consonant/vowel/mixed so it means all of them
    if DeclensionType.III in types:
        types += [DeclensionType.III_consonant, DeclensionType.III_vowel, DeclensionType.III_mixed]

    return Declensions([declension for declension in dictionary.declensions
                        if declension.type in types])


# test it ?
def random_declension_entry(declensions: Declensions, rng: Generator) -> DeclensionTest:
    if len(declensions.declensions) == 0:
        raise Exception("cannot select random entry from empty dict")

    patterns: list[SingleDeclensionPattern] = flatten(
        [x.declension_patterns for x in declensions.declensions]
    )
    base_words = [p.base_word for p in patterns]

    random_base_word: str = rng.choice(base_words, 1)[0]
    selected_pattern: SingleDeclensionPattern = [p for p in patterns if p.base_word == random_base_word][0]

    singular: bool = rng.choice([0, 1], 1)[0] == 0
    selected_dict = selected_pattern.singular if singular else selected_pattern.plural
    selected_case = rng.choice([*DeclensionCase]).name.lower()

    answer = selected_dict[selected_case]

    declension_prompt = DeclensionPrompt(random_base_word, 'singularis' if singular else 'pluralis', selected_case)
    declension_test = DeclensionTest(declension_prompt, answer)

    return declension_test
