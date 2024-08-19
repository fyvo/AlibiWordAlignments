from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import Counter

# def get_pos_tag_tokens(soup,path_eng_file,path_fr_file):
#     # creates two files specified in path_eng_file and path_fr_file which contain the information about the pos of every token
#     # the second linkList contains linkGroups with all the annotations (linkList level='token')
#     linkLists = soup.find_all('linkList')
#     linkList = linkLists[1]
#     linkGroups=linkList.find_all('linkGroup')
#     # print(linkGroups, len(linkGroups))
#     with open(path_eng_file, 'a+') as eng_file, open(path_fr_file, 'a+') as fr_file:
#         for i,linkGroup in enumerate(linkGroups):
#             annotations_fr = linkGroup.find_all('annotation', id=re.compile("doc_fr annot_token_"))
#             annotations_eng = linkGroup.find_all('annotation', id=re.compile("doc_en annot_token_"))
#             if annotations_fr:
#                 fr_file.write(f"{i}\t")
#                 for annotation in annotations_fr:
#                     sent_token_id = annotation.find_all('docSpan')[0].tokenID
#                     # TODO make all of them into one big list, sort by sentence, then write from list to file
#                     pos = annotation.find_all('mark',cat='POS')[0].string
#                     fr_file.write(f'{pos} ')
#                 fr_file.write("\n") 
#             if annotations_eng:
#                 eng_file.write(f"{i}\t")
#                 for annotation in annotations_eng:
#                     sent_token_id = annotation.find_all('docSpan')[0].tokenID
#                     pos = annotation.find_all('mark',cat='POS')[0].string
#                     eng_file.write(f'{pos} ')
#                 eng_file.write("\n") 
#             annotations_fr=[]
#             annotations_eng=[]



def get_pos_tag_tokens(soup):
    # creates two files specified in path_eng_file and path_fr_file which contain the information about the pos of every token
    # the second linkList contains linkGroups with all the annotations (linkList level='token')
    linkLists = soup.find_all('linkList')
    linkList = linkLists[1]
    # print(linkGroups, len(linkGroups))
    big_fr_dict = dict()
    big_eng_dict = dict()
    annotations_fr = linkList.find_all('annotation', id=re.compile("doc_fr annot_token_"))
    annotations_eng = linkList.find_all('annotation', id=re.compile("doc_en annot_token_"))
    if annotations_fr:
        for annotation in annotations_fr:
            sent_token_id = annotation.find_all('docSpan')[0]['tokenID']
            sent_id, token_id = sent_token_id.split()[1].split('.')    # dropping the 'doc_fr' part of the id, splitting sent.token
            # TODO make all of them into one big list, sort by sentence, then write from list to file
            # actually dont save in file but retrieve the aligned pos only
            # actually dont make one big list but a nested dict?
            # actually you need the list to sort ?
            # yes but you actually don't need to sort
            # I do need to sort bc sent 1 has id 1 in eng and 2 in fr
            pos = annotation.find_all('mark',cat='POS')[0].string
            if int(sent_id) not in big_fr_dict:
                big_fr_dict[int(sent_id)] = dict()
            big_fr_dict[int(sent_id)][int(token_id)] = pos
    if annotations_eng:
        for annotation in annotations_eng:
            sent_token_id = annotation.find_all('docSpan')[0]['tokenID']
            sent_id, token_id = sent_token_id.split()[1].split('.')    # dropping the 'doc_fr' part of the id, splitting sent.token
            pos = annotation.find_all('mark',cat='POS')[0].string
            # big_eng_list.append((int(sent_id), int(token_id), pos))
            if int(sent_id) not in big_eng_dict:
                big_eng_dict[int(sent_id)] = dict()
            big_eng_dict[int(sent_id)][int(token_id)] = pos
    # annotations_fr=[]
    # annotations_eng=[]
    sorted_fr = dict(sorted(big_fr_dict.items()))
    sorted_eng = dict(sorted(big_eng_dict.items()))
    # sorted_fr = sorted(big_fr_list, key = lambda x: (x[0], x[1]))
    # print(len(big_eng_list), len(big_fr_list),sorted_fr[:100], sorted_eng[:100])
    # del sorted_eng[1]
    return sorted_fr, sorted_eng

def check_pos_of_ali(fr_dict, eng_dict, ali_w2w, result_path):
    all_fr_pos_list=[]
    all_eng_pos_list=[]
    ali_pos_list=[]
    with open(ali_w2w, 'r') as ali_file:
        # print(len(eng_file), len(fr_file), len(ali_file))
        # , open(result_pos, 'a+') as chat_resolu # add above if we want to save the pos alignments to a file
        print(len(fr_dict), len(eng_dict))
        for line_ali,fr_key,eng_key in zip(ali_file, fr_dict, eng_dict):
            ali_list = line_ali.split('\t')[1].split() # takes the alignments without the id\t, makes a list of alignments
            # print(pos_fr_list,pos_eng_list,ali_list)
            # print(line_eng, line_fr, line_ali)
            # print(len(pos_fr_list), len(pos_eng_list), len(ali_list), ali_list)
            for ali in ali_list:
                fr_id,eng_id = re.split('-|p', ali)
                # chat_resolu.write(f'{pos_fr_list[int(fr_id)]}-{pos_eng_list[int(eng_id)]} ')
                try:
                    ali_pos_list.append(f'{fr_dict[fr_key][int(fr_id)]}-{eng_dict[eng_key][int(eng_id)]}')
                except:
                    print('out of range: ',fr_key, eng_key, fr_id, eng_id)
            all_fr_pos_list.extend(fr_dict[fr_key].values())
            all_eng_pos_list.extend(eng_dict[eng_key].values())
    df = pd.DataFrame(ali_pos_list, columns=['alignment_pos'])
    # print(df.value_counts())
    c_fr = Counter(all_fr_pos_list)
    c_eng = Counter(all_eng_pos_list)
    print(c_eng, c_fr, sum(c_eng.values()), sum(c_fr.values()))
    df.value_counts().to_csv(result_path)
    return all_fr_pos_list, all_eng_pos_list, df

    
if __name__ == "__main__":
    ali_w2w_paths = ['ali/LAuberge_TheInn/ali_w2w_LAuberge_TheInn.txt','ali/LaBarbeBleue_BlueBeard/ali_w2w_LaBarbeBleue_BlueBeard.txt','ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt','ali/LaDerniereClasse_TheLastLesson/ali_w2w_LaDerniereClasse_TheLastLesson.txt','ali/LaVision_TheVision/ali_w2w_LaVision_TheVision.txt']
    ali_xml_paths = ["dat/LAuberge_TheInn.ali.xml", "dat/BarbeBleue_BlueBeard.ali.xml",
                     "dat/ChatBotte_MasterCat.ali.xml", "dat/Laderniereclasse_Thelastlesson.ali.xml", "dat/LaVision_TheVision.ali.xml"]
    # alignment_xml_path = 'dat/LaVision_TheVision.ali.xml'
    # ali_w2w_path = "ali/LaVision_TheVision/ali_w2w_LaVision_TheVision.txt"
    result_path = 'bozeratunku.csv'
    all_fr_pos = []
    all_eng_pos = []
    all_dfs = []
    for alignment_xml_path, ali_w2w_path in zip(ali_xml_paths,ali_w2w_paths):
        with open(alignment_xml_path, 'r') as filehandle:
            soup = BeautifulSoup(filehandle, 'xml')
        sorted_fr, sorted_eng = get_pos_tag_tokens(soup)
        if alignment_xml_path == 'dat/LaVision_TheVision.ali.xml':   # I APOLOGIZE FOR THIS LINE
            del sorted_eng[1]
        if alignment_xml_path == "dat/BarbeBleue_BlueBeard.ali.xml":
            del sorted_eng[20]
        if alignment_xml_path == "dat/Laderniereclasse_Thelastlesson.ali.xml":   # I AM STILL VERY SORRY
            del sorted_fr[12]
            del sorted_eng[13]
        fr_pos, eng_pos, df = check_pos_of_ali(sorted_fr,sorted_eng,ali_w2w_path,result_path)
        all_fr_pos.extend(fr_pos)
        all_eng_pos.extend(eng_pos)
        all_dfs.append(df)
    ultimate_pos_pair_df = pd.concat(all_dfs)
    print(ultimate_pos_pair_df.value_counts())
    ultimate_pos_pair_df.value_counts().to_csv("ULTIMATE_POS.csv")
    c_fr = Counter(all_fr_pos)
    c_eng = Counter(all_eng_pos)
    print(c_eng, c_fr, sum(c_eng.values()), sum(c_fr.values()))