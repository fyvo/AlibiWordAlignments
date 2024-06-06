from bs4 import BeautifulSoup
import sys


def extract_sentences(soup):
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    linkGroups = soup.linkList.find_all('linkGroup')
    sentence_tuples = []
    for linkGroup in linkGroups:
        links = linkGroup.find_all('link')
        for link in links:
            if link['parentID'] == "ROOT":
                spans = link.find_all('docSpan')
                sentence_tuples.append(
                    (spans[0].string, spans[1].string))
    return sentence_tuples


def write_eng_fr_to_files(sentences_tuple, path_eng_file, path_fr_file):
    with open(path_eng_file, 'w') as eng_file, open(path_fr_file, 'w') as fr_file:
        for i, sent_pair in enumerate(sentences_tuple):
            fr_file.write(f'{i}\t{sent_pair[0]}\n')
            eng_file.write(f'{i}\t{sent_pair[1]}\n')


if __name__ == "__main__":

    alignment_xml_path = 'dat/ChatBotte_MasterCat.ali.xml'

    alignment_xml_path = input("path to the xml alignments file: ")

    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')

    sents = extract_sentences(soup)

    path_eng = "scripts/sents_ChatBotte_eng.txt"
    path_fr = "scripts/sents_ChatBotte_fr.txt"

    path_eng = input(
        "path to file where you want to save the eng sentences: ")
    path_fr = input("path to file where you want to save the fr sentences: ")
    # path_eng = sys.argv[2]
    # path_fr = sys.argv[3]

    write_eng_fr_to_files(sents, path_eng, path_fr)
