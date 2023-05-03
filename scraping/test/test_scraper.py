from scraping.lib.scraper import LatinDictScraper

scraper = LatinDictScraper(None, None, None)


def test_verb_metadata():
    assert scraper.verb_metadata('transitive and intransitive verb III conjugation ending -io') == '[verb] [III]'
    assert scraper.verb_metadata('transitive verb I conjugation') == '[verb] [I]'
