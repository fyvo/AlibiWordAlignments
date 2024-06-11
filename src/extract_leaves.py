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
# def build_indices(path_eng_sents, path_fr_sents):
#     indices_dict = {'fr_ids2tokens': [], 'fr_tokens2ids': [],
#                     'eng_ids2tokens': [], 'eng_tokens2ids': []}
#     with open(path_eng_sents, 'r') as eng_file, open(path_fr_sents, 'r') as fr_file:
#         eng_sents = eng_file.readlines()
#         fr_sents = fr_file.readlines()
#     for eng_sent, fr_sent in zip(eng_sents, fr_sents):
#         eng_id2token = eng_sent.split('\t')[1].split()
#         # removing the line id and separating by space
#         # ['THE', 'MASTER', 'CAT', ',', 'OR', 'PUSS', 'IN', 'BOOTS']
#         fr_id2token = fr_sent.split('\t')[1].split()
#         eng_token2id = {eng_id2token[i]: [] for i in range(len(eng_id2token))}
#         for i, token in enumerate(eng_id2token):
#             eng_token2id[token].append(i)
#         # {'THE': 0, 'MASTER': 1, 'CAT': 2, ',': 3, 'OR': 4, 'PUSS': 5, 'IN': 6, 'BOOTS': 7}
#         fr_token2id = {fr_id2token[i]: [] for i in range(len(fr_id2token))}
#         for i, token in enumerate(fr_id2token):
#             fr_token2id[token].append(i)
#         indices_dict['eng_ids2tokens'].append(eng_id2token)
#         indices_dict['eng_tokens2ids'].append(eng_token2id)
#         indices_dict['fr_ids2tokens'].append(fr_id2token)
#         indices_dict['fr_tokens2ids'].append(fr_token2id)
#     return indices_dict


# indices_dict = build_indices(path_eng_sents, path_fr_sents)
# # has 4 structures for every sentence

# print('\n\n', all_leaf_alignments[0])


# def convert_to_pharaoh(leaf_alignments_list):
#     for i, sentence_alignments in enumerate(leaf_alignments_list):
#         with open('sentence_alignments.txt', 'a+') as file:
#             for fr_leaf, eng_leaf in sentence_alignments:
#                 eng_span_split = eng_leaf.split()
#                 fr_span_split = fr_leaf.split()
#                 print(eng_span_split, fr_span_split)
#                 if len(eng_span_split) == 1 and len(fr_span_split) == 1:
#                     file.write(
#                         f"{indices_dict['fr_ids2tokens'][i].index(fr_span_split[0])}-{indices_dict['eng_ids2tokens'][i].index(eng_span_split[0])} ")
#                 elif len(eng_span_split) == 1 and len(fr_span_split) != 1:
#                     for token in fr_span_split:
#                         file.write(
#                             f"{indices_dict['fr_ids2tokens'][i].index(token)}p{indices_dict['eng_ids2tokens'][i].index(eng_span_split[0])} ")
#                 elif len(eng_span_split) != 1 and len(fr_span_split) == 1:
#                     for token in eng_span_split:
#                         file.write(
#                             f"{indices_dict['fr_ids2tokens'][i].index(fr_span_split[0])}p{indices_dict['eng_ids2tokens'][i].index(token)} ")
#                 elif len(eng_span_split) != 1 and len(fr_span_split) != 1:
#                     for eng_token in eng_span_split:
#                         for fr_token in fr_span_split:
#                             file.write(
#                                 f"{indices_dict['fr_ids2tokens'][i].index(fr_token)}p{indices_dict['eng_ids2tokens'][i].index(eng_token)} ")

#             file.write('\n')


# convert_to_pharaoh(all_leaf_alignments)
