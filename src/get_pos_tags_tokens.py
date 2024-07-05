from bs4 import BeautifulSoup
import re

def get_pos_tag_tokens(soup,path_eng_file,path_fr_file):
    # creates two files specified in path_eng_file and path_fr_file which contain the information about the pos of every token
    # the second linkList contains linkGroups with all the annotations (linkList level='token')
    linkLists = soup.find_all('linkList')
    linkList = linkLists[1]
    linkGroups=linkList.find_all('linkGroup')
    # print(linkGroups, len(linkGroups))
    with open(path_eng_file, 'a+') as eng_file, open(path_fr_file, 'a+') as fr_file:
        for i,linkGroup in enumerate(linkGroups):
            annotations_fr = linkGroup.find_all('annotation', id=re.compile("doc_fr annot_token_"))
            annotations_eng = linkGroup.find_all('annotation', id=re.compile("doc_en annot_token_"))
            if annotations_fr:
                fr_file.write(f"{i}\t")
                for annotation in annotations_fr:
                    pos = annotation.find_all('mark',cat='POS')[0].string
                    fr_file.write(f'{pos} ')
                fr_file.write("\n") 
            if annotations_eng:
                eng_file.write(f"{i}\t")
                for annotation in annotations_eng:
                    pos = annotation.find_all('mark',cat='POS')[0].string
                    eng_file.write(f'{pos} ')
                eng_file.write("\n") 
            annotations_fr=[]
            annotations_eng=[]

if __name__ == "__main__":
    # alignment_xml_path = input("path to the xml alignments file: ")
    alignment_xml_path = 'dat/LaVision_TheVision.ali.xml'
    eng_path="eng_pos_V2.txt"
    fr_path="fr_pos_V2.txt"
    with open(alignment_xml_path, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')
    get_pos_tag_tokens(soup,eng_path, fr_path)