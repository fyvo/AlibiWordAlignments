from extract_leaves import extract_leaves_with_span_info
import re
from bs4 import BeautifulSoup
from collections import Counter


def convert_to_pharaoh(dict_all_leaves_by_sentence, alignment_filepath):
    ali_lens_distr = []
    # regex matching (one or more) digits preceded by underscore, separated by a dash
    pattern = r"_(\d+-\d+)"
    for i, sentence_leaves in enumerate(dict_all_leaves_by_sentence):
        with open(alignment_filepath, 'a+') as file:
            file.write(f'{i}\t')
            for span_id in sentence_leaves.keys():
                fr_span, eng_span = re.findall(pattern, span_id)
                fr_begin, fr_end = fr_span.split('-')
                eng_begin, eng_end = eng_span.split('-')
                if fr_begin == fr_end and eng_begin == eng_end:  # case: 1 fr to 1 eng token, sure alignment
                    ali_lens_distr.append('1-1')
                    file.write(f'{fr_begin}-{eng_begin} ')
                elif fr_begin != fr_end and eng_begin == eng_end:
                    # case: many fr to 1 eng, potential
                    ali_lens_distr.append(f'{int(fr_end)-int(fr_begin)+1}-1')
                    for j in range(int(fr_begin), int(fr_end)+1):
                        file.write(f'{j}p{eng_begin} ')
                elif fr_begin == fr_end and eng_begin != eng_end:
                    # case: 1 fr to many eng, potential
                    ali_lens_distr.append(f'1-{int(eng_end)-int(eng_begin)+1}')
                    for j in range(int(eng_begin), int(eng_end)+1):
                        file.write(f'{fr_begin}p{j} ')
                elif fr_begin != fr_end and eng_begin != eng_end:  # case: many fr to many eng, potential
                    ali_lens_distr.append(f'{int(fr_end)-int(fr_begin)+1}-{int(eng_end)-int(eng_begin)+1}')                    
                    for j in range(int(fr_begin), int(fr_end)+1):
                        for k in range(int(eng_begin), int(eng_end)+1):
                            file.write(f'{j}p{k} ')
            file.write('\n')
    lens_counter = Counter(ali_lens_distr)
    print(sum(lens_counter.values()))
    for val in lens_counter:
        print (val,'\t', lens_counter[val])
if __name__ == "__main__":
    alignment_xml_path = 'dat/Laderniereclasse_Thelastlesson.ali.xml'
    # alignment_xml_path = input("path to the xml alignments file: ")

    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')

    dict_all_leaves_by_sentence, dict_all_leaves = extract_leaves_with_span_info(
        soup, separate_by_sentence=True)

    alignment_filepath = 'charaoh.txt'
    # alignment_filepath = input(
    #     "path to file where you want to save the w2w leaf alignments: ")
    convert_to_pharaoh(dict_all_leaves_by_sentence, alignment_filepath)
