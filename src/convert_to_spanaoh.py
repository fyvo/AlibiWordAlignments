from extract_all_spans import extract_all_spans
import re
from bs4 import BeautifulSoup

def convert_to_spanaoh(dict_all_spans_by_sentence, alignment_filepath):
    # regex matching (one or more) digits preceded by underscore, separated by a dash
    pattern = r"_(\d+-\d+)"
    for i, sentence_leaves in enumerate(dict_all_spans_by_sentence):
        with open(alignment_filepath, 'a+') as file:
            file.write(f'{i}\t')
            for span_id in sentence_leaves.keys():
                fr_span, eng_span = re.findall(pattern, span_id)
                fr_span = fr_span.replace('-',',')
                eng_span = eng_span.replace('-',',')
                file.write(f'{fr_span}-{eng_span} ')
            file.write('\n')



if __name__ == "__main__":
    alignment_xml_path = 'dat/ChatBotte_MasterCat.ali.xml'
    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')

    dict_all_spans_by_sentence, dict_all_leaves = extract_all_spans(
        soup, separate_by_sentence=True, mark_leaves=False)

    alignment_filepath = 'chat_spans_tests.txt'
    convert_to_spanaoh(dict_all_spans_by_sentence, alignment_filepath)