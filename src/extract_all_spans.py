from bs4 import BeautifulSoup


def extract_all_spans(soup, separate_by_sentence=True, mark_leaves=False):
    # returns
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    linkGroups = soup.linkList.find_all('linkGroup')
    all_spans = dict()
    sentence_level = []
    for linkGroup in linkGroups:
        sentence_leaves = dict()
        links = linkGroup.find_all('link')
        if not links:   # skipping the empty linkGroups
            continue
        list_parent_ids = [link['parentID'] for link in links]
        for link in links:
            docspans_fr_eng = [(docspan['beginPos'].split('.')[-1], docspan['endPos'].split(
                '.')[-1], docspan.string) for docspan in link.find_all('docSpan')]
            if mark_leaves:
                if link['id'] not in list_parent_ids:
                    docspans_fr_eng.append(True)
                else:
                    docspans_fr_eng.append(False)
            all_spans[link['id']] = docspans_fr_eng
            if separate_by_sentence:
                sentence_leaves[link['id']] = docspans_fr_eng
        if separate_by_sentence:
            sentence_level.append(sentence_leaves)
    if separate_by_sentence:
        return sentence_level, all_spans
    return all_spans
