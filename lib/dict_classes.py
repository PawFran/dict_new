from dataclasses import dataclass
from lib.utils import extract_from_square_brackets


@dataclass
class AbstractWord:
    base: str
    head_raw: str
    # todo abstract static method from_entry head ?


@dataclass
class LatinVerb(AbstractWord):
    infinite: str
    perfect: str
    supine: str
    conjugation: str  # maybe another class/enum ?

    @staticmethod
    def is_verb(dict_entry_head):
        return '[verb]' in dict_entry_head.lower()

    @staticmethod
    def which_conjugation(dict_entry_head):
        # conjugation may be [I] or [II] or [III] or [IIIa] or [IV]
        conjugation_pattern = '\[I{1,3}V*\]'
        return extract_from_square_brackets(conjugation_pattern, dict_entry_head)

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')
        return LatinVerb(
            base=split[0].strip(),
            head_raw=head,
            infinite=split[1].strip(),
            perfect=split[2].strip(),
            supine=split[3].strip().split(' ')[0].strip(),
            conjugation=LatinVerb.which_conjugation(head)
        )


# TODO add phrasal verb ? idiom ? or maybe english dict should be in different project ?


@dataclass
class LatinNoun(AbstractWord):
    genetive: str
    genre: str
    only_plural: bool
    declension: str  # roman number

    @staticmethod
    def is_noun(dict_entry_head):
        return '[noun]' in dict_entry_head.lower()

    @staticmethod
    def is_only_plural(dict_entry_head):
        return '[pl]' in dict_entry_head.lower()

    @staticmethod
    def which_declension(dict_entry_head):
        # declension may be [I] or [II] or [III vowel] or [III consonant] or [III mixed] or [IV] or [V]
        declension_pattern = '\[I{0,3} *(vowel)*(consonant)*(mixed)*V*\]'
        return extract_from_square_brackets(declension_pattern, dict_entry_head)

    @staticmethod
    def which_genre(dict_entry_head):
        genre_pattern = '\[[fmn]\]'
        return extract_from_square_brackets(genre_pattern, dict_entry_head)

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')
        return LatinNoun(
            base=split[0].strip(),
            head_raw=head,
            genetive=split[1].strip().split(' ')[0].strip(),
            genre=LatinNoun.which_genre(head),
            only_plural=LatinNoun.is_only_plural(head),
            declension=LatinNoun.which_declension(head)
        )


@dataclass
class LatinAdverb(AbstractWord):

    @staticmethod
    def is_adverb(dict_entry_head):
        return '[adv]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        return LatinAdverb(
            base=head.split(' ')[0],
            head_raw=head
        )


@dataclass
class LatinAdjective(AbstractWord):
    femininum: str
    neutrum: str

    @staticmethod
    def is_adjective(dict_entry_head):
        return '[adj]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')
        return LatinAdjective(
            base=split[0],
            head_raw=head,
            femininum=split[1].strip(),
            neutrum=split[2].strip().split(' ')[0]
        )


@dataclass
class EnglishWord(AbstractWord):  # all english dict entries have the same structure, unlike in latin
    part_of_speech: str

    @staticmethod
    def which_part_of_speech(dict_entry_head):
        pattern = 'verb|idiom|noun|adj|adv|phrasal verb'
        return extract_from_square_brackets(pattern, dict_entry_head.lower())

    @staticmethod
    def from_entry_head(head):
        head_without_last_part = head.strip().split(' ')[:-1]
        base = ' '.join(head_without_last_part)
        return EnglishWord(
            base=base,
            head_raw=head,
            part_of_speech=EnglishWord.which_part_of_speech(head)
        )


@dataclass
class DictionaryEntry:
    """storing entries like:
    castīgo, āre, avi, atum [verb] [I]
    (Ancillam miseram domina sevēra castīgat)
    1. karać
    """
    head: AbstractWord  # basic dictionary entry that is base word with another info like in above example
    example: str
    translations: list[str]


@dataclass
class Dictionary:
    """full dictionary"""
    entries: list[DictionaryEntry]

    def append(self, dict_entry):
        self.entries.append(dict_entry)
