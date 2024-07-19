from extract_all_spans import extract_all_spans
import re
from bs4 import BeautifulSoup

def convert_to_spanaoh(dict_all_spans_by_sentence, leaf_path, nonleaf_path):
    # regex matching (one or more) digits preceded by underscore, separated by a dash
    pattern = r"_(\d+-\d+)"
    for i, sentence_leaves in enumerate(dict_all_spans_by_sentence):
        with open(leaf_path, 'a+') as leaf_file, open(nonleaf_path,'a+') as nonleaf_file:
            leaf_file.write(f'{i}\t')
            nonleaf_file.write(f'{i}\t')
            for span_id, value in sentence_leaves.items():
                fr_span, eng_span = re.findall(pattern, span_id)
                fr_span = fr_span.replace('-',',')
                eng_span = eng_span.replace('-',',')
                if value[2]:    # True if leaf, False otherwise
                    leaf_file.write(f'{fr_span}-{eng_span} ')
                else:
                    nonleaf_file.write(f'{fr_span}-{eng_span} ')
            nonleaf_file.write('\n')
            leaf_file.write('\n')

# def convert_to_spanaoh_leaves_nonleaves(list_leaves,list_nonleaves, leaf_path, nonleaf_path):
#     # regex matching (one or more) digits preceded by underscore, separated by a dash
#     pattern = r"_(\d+-\d+)"
#     for i, sentence_leaves in enumerate(list_leaves):   # loop over list of lists of leaves per sentence
#         with open(leaf_path, 'a+') as file:
#             file.write(f'{i}\t')
#             for leaf in list_leaves:
#                 print(leaf)
#                 fr_span, eng_span = re.findall(pattern, leaf['id'])
#                 fr_span = fr_span.replace('-',',')
#                 eng_span = eng_span.replace('-',',')
#                 file.write(f'{fr_span}-{eng_span} ')
#             file.write('\n')
#     for i, sentence_nonleaves in enumerate(list_nonleaves):   # loop over list of lists of leaves per sentence
#         with open(nonleaf_path, 'a+') as file:
#             file.write(f'{i}\t')
#             for nonleaf in list_nonleaves:
#                 fr_span, eng_span = re.findall(pattern, nonleaf['id'])
#                 fr_span = fr_span.replace('-',',')
#                 eng_span = eng_span.replace('-',',')
#                 file.write(f'{fr_span}-{eng_span} ')
#             file.write('\n')


if __name__ == "__main__":
    alignment_xml_path = 'dat/ChatBotte_MasterCat.ali.xml'
    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')

    dict_all_spans_by_sentence, dict_all_leaves = extract_all_spans(
        soup, separate_by_sentence=True, mark_leaves=True)
    # list_leaves,list_nonleaves = extract_all_spans(
    #     soup, separate_by_sentence=True, mark_leaves=True)

    leaf_path = 'chat_leaf_ref.txt'
    nonleaf_path = 'chat_nonleaf_ref.txt'
    alignment_filepath = 'chat_full_spanaoh_ref.txt'
    convert_to_spanaoh(dict_all_spans_by_sentence, leaf_path,nonleaf_path)
    # convert_to_spanaoh_leaves_nonleaves(list_leaves,list_nonleaves,leaf_path,nonleaf_path)