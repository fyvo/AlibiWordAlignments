from bs4 import BeautifulSoup


def extract_leaves_strings_only(soup):
    # returns a list, every element corresponds to one setence, every element contains a list of pairs of aligned leaf strings
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    linkGroups = soup.linkList.find_all('linkGroup')
    all_leaf_alignments_strings_only = []
    for linkGroup in linkGroups:
        leaves = []
        links = linkGroup.find_all('link')
        if not links:   # skipping the empty linkGroups
            continue
        list_parent_ids = [link['parentID'] for link in links]
        for link in links:
            if link['id'] not in list_parent_ids:
                leaves.append(
                    [docspan.string for docspan in link.find_all('docSpan')])
        all_leaf_alignments_strings_only.append(leaves)
    return all_leaf_alignments_strings_only


def extract_leaves_with_span_info(soup, separate_by_sentence=True):
    # returns a dict with linkIDs as keys, lists of 2 tuples containing info about the spans that are linked (beginPos, endPos, string) as values
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    linkGroups = soup.linkList.find_all('linkGroup')
    all_leaves = dict()
    sentence_level = []
    for linkGroup in linkGroups:
        sentence_leaves = dict()
        links = linkGroup.find_all('link')
        if not links:   # skipping the empty linkGroups
            continue
        list_parent_ids = [link['parentID'] for link in links]
        for link in links:
            # a link is a leaf if no other link has it as a parent
            if link['id'] not in list_parent_ids:
                docspans_fr_eng = [(docspan['beginPos'].split('.')[-1], docspan['endPos'].split(
                    '.')[-1], docspan.string) for docspan in link.find_all('docSpan')]
                # for every link, a list of two tuples containing begPos, endPos and the span text for French and for English
                all_leaves[link['id']] = docspans_fr_eng
                if separate_by_sentence:
                    sentence_leaves[link['id']] = docspans_fr_eng
        if separate_by_sentence:
            sentence_level.append(sentence_leaves)
    if separate_by_sentence:
        return sentence_level, all_leaves
    return all_leaves


if __name__ == "__main__":
    # alignment_xml_path = input("path to the xml alignments file: ")
    alignment_xml_path = 'dat/Laderniereclasse_Thelastlesson.ali.xml'
    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')
    dict_all_leaves_by_sentence, dict_all_leaves = extract_leaves_with_span_info(
        soup, separate_by_sentence=True)
    all_leaves_strings = extract_leaves_strings_only(soup)
    print(all_leaves_strings, dict_all_leaves_by_sentence, dict_all_leaves)
