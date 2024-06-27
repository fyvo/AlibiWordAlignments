from bs4 import BeautifulSoup
import re

def get_pos_tag_leaves(soup, separate_by_sentence=True):
    # returns a dict with linkIDs as keys, lists of 2 tuples containing info about the spans that are linked (beginPos, endPos, string) as values
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    linkGroups = soup.find_all(level='token')
    all_leaves = dict()
    sentence_level = []
    # print(linkGroups, len(linkGroups))
    for linkGroup in linkGroups:
        annotations = linkGroup.find_all('annotation', id=re.compile("annot_token_"))
        print(annotations,len(annotations))
        for annotation in annotations:
            pos = annotation.find_all('mark',cat='POS')[0].string
            print(annotation,pos,'\n\n\n')
        # pos_tags = annotations.find_all(id=re.compile("annot_token_"))
        # print(pos_tags, len(pos_tags))
    #     links = linkGroup.find_all('link')
    #     if not links:   # skipping the empty linkGroups
    #         continue
    #     list_parent_ids = [link['parentID'] for link in links]
    #     for link in links:
    #         # a link is a leaf if no other link has it as a parent
    #         if link['id'] not in list_parent_ids:
    #             docspans_fr_eng = [(docspan['beginPos'].split('.')[-1], docspan['endPos'].split(
    #                 '.')[-1], docspan.string) for docspan in link.find_all('docSpan')]
    #             # for every link, a list of two tuples containing begPos, endPos and the span text for French and for English
    #             all_leaves[link['id']] = docspans_fr_eng
    #             if separate_by_sentence:
    #                 sentence_leaves[link['id']] = docspans_fr_eng
    #     if separate_by_sentence:
    #         sentence_level.append(sentence_leaves)
    # if separate_by_sentence:
    #     return sentence_level, all_leaves
    # return all_leaves


if __name__ == "__main__":
    # alignment_xml_path = input("path to the xml alignments file: ")
    alignment_xml_path = 'dat/ChatBotte_MasterCat.ali.xml'
    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')
    get_pos_tag_leaves(soup, separate_by_sentence=True)
    #     soup, separate_by_sentence=True)
    # dict_all_leaves_by_sentence, dict_all_leaves = extract_leaves_with_span_info(
    #     soup, separate_by_sentence=True)
    # print(dict_all_leaves_by_sentence, dict_all_leaves)