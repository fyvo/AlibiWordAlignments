import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from unidecode import unidecode

alignment_xml_path = 'dat\ChatBotte_MasterCat.ali.xml'

path_eng_sents = "scripts/sents_ChatBotte_eng.txt"
path_fr_sents = "scripts/sents_ChatBotte_fr.txt"

with open(alignment_xml_path, 'r') as filehandle:
    soup = BeautifulSoup(filehandle, 'xml')


def extract_leaves(link_group):
    leaves = []
    links = link_group.find_all('link')
    list_parent_ids = [link['parentID'] for link in links]
    for link in links:
        if link['id'] not in list_parent_ids:
            leaves.append(
                [docspan.string for docspan in link.find_all('docSpan')])
    return leaves


# the first linkList contains linkGroups with all the alignments (linkList level='chunk')
linkGroups = soup.linkList.find_all('linkGroup')

# # test
# one_linkGroup = linkGroups.linkGroup
# print(extract_leaves(one_linkGroup))

all_leaf_alignments = []
for linkGroup in linkGroups:
    all_leaf_alignments.append(extract_leaves(linkGroup))


print(len(all_leaf_alignments), '\n',
      all_leaf_alignments[-5], '\n\n', all_leaf_alignments[-4])


def build_indices(path_eng_sents, path_fr_sents):
    indices_dict = {'fr_ids2tokens': [], 'fr_tokens2ids': [],
                    'eng_ids2tokens': [], 'eng_tokens2ids': []}
    with open(path_eng_sents, 'r') as eng_file, open(path_fr_sents, 'r') as fr_file:
        eng_sents = eng_file.readlines()
        fr_sents = fr_file.readlines()
    for eng_sent, fr_sent in zip(eng_sents, fr_sents):
        eng_id2token = eng_sent.split('\t')[1].split()
        # removing the line id and separating by space
        # ['THE', 'MASTER', 'CAT', ',', 'OR', 'PUSS', 'IN', 'BOOTS']
        fr_id2token = fr_sent.split('\t')[1].split()
        eng_token2id = {eng_id2token[i]: i for i in range(len(eng_id2token))}
        # {'THE': 0, 'MASTER': 1, 'CAT': 2, ',': 3, 'OR': 4, 'PUSS': 5, 'IN': 6, 'BOOTS': 7}
        fr_token2id = {fr_id2token[i]: i for i in range(len(fr_id2token))}
        indices_dict['eng_ids2tokens'].append(eng_id2token)
        indices_dict['eng_tokens2ids'].append(eng_token2id)
        indices_dict['fr_ids2tokens'].append(fr_id2token)
        indices_dict['fr_tokens2ids'].append(fr_token2id)
    return indices_dict


indices_dict = build_indices(path_eng_sents, path_fr_sents)
# has 4 structures for every sentence

print('\n\n', all_leaf_alignments[0])


def convert_to_pharaoh(leaf_alignments_list):
    for i, sentence_alignments in enumerate(leaf_alignments_list):
        for fr_leaf, eng_leaf in sentence_alignments:
            eng_span_split = eng_leaf.split()
            fr_span_split = fr_leaf.split()
            print(eng_span_split, fr_span_split)
            with open('sentence_alignments.txt', 'a') as file:
                if len(eng_span_split) == 1 and len(fr_span_split) == 1:
                    print(indices_dict['fr_tokens2ids'][i])
                    print(indices_dict['eng_tokens2ids'][i])
                    file.write(
                        f"{indices_dict['fr_tokens2ids'][i][fr_span_split[0]]}-{indices_dict['eng_tokens2ids'][i][eng_span_split[0]]}")
                elif len(eng_span_split) == 1 and len(fr_span_split) != 1:
                    for token in fr_span_split:
                        file.write(
                            f"{indices_dict['fr_tokens2ids'][i][token]}p{indices_dict['eng_tokens2ids'][i][eng_span_split]}")
                elif len(eng_span_split) != 1 and len(fr_span_split) == 1:
                    for token in eng_span_split:
                        file.write(
                            f"{indices_dict['fr_tokens2ids'][i][fr_span_split]}p{indices_dict['eng_tokens2ids'][i][token]}")
                elif len(eng_span_split) != 1 and len(fr_span_split) != 1:
                    for eng_token in eng_span_split:
                        for fr_token in fr_span_split:
                            file.write(
                                f"{indices_dict['fr_tokens2ids'][i][fr_token]}p{indices_dict['eng_tokens2ids'][i][eng_token]}")


convert_to_pharaoh(all_leaf_alignments)
