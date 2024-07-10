import re
import pandas as pd
from collections import Counter
# fr_pos_list = ['pos_tags/fr_pos_A.txt','pos_tags/fr_pos_B.txt','pos_tags/fr_pos_C.txt','pos_tags/fr_pos_D.txt','pos_tags/fr_pos_V.txt']
# eng_pos_list = ['pos_tags/eng_pos_A.txt','pos_tags/eng_pos_B.txt','pos_tags/eng_pos_C.txt','pos_tags/eng_pos_D.txt','pos_tags/eng_pos_V.txt']
# ali_w2w_list = ['ali/LAuberge_TheInn/ali_w2w_LAuberge_TheInn.txt','ali/LaBarbeBleue_BlueBeard/ali_w2w_LaBarbeBleue_BlueBeard.txt','ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt','ali/LaDerniereClasse_TheLastLesson/ali_w2w_LaDerniereClasse_TheLastLesson.txt','ali/LaVision_TheVision/ali_w2w_LaVision_TheVision.txt']
# result_pos_list = ['pos_tags/pos_A.csv','pos_tags/pos_B.csv','pos_tags/pos_C.csv','pos_tags/pos_D.csv','pos_tags/pos_V.csv']
fr_pos_list = ['pos_tags/fr_pos_D.txt']
eng_pos_list = ['pos_tags/eng_pos_D.txt']
ali_w2w_list = ['ali/LaDerniereClasse_TheLastLesson/ali_w2w_LaDerniereClasse_TheLastLesson.txt']
result_pos_list = ['pos_tags/D_debugueur.csv']
all_fr_pos_list=[]
all_eng_pos_list=[]
pos_frequencies=[]
for fr_pos, eng_pos, ali_w2w, result_pos in zip(fr_pos_list,eng_pos_list,ali_w2w_list,result_pos_list):
    ali_pos_list=[]
    with open(eng_pos, 'r') as eng_file, open(fr_pos, 'r') as fr_file, open(ali_w2w, 'r') as ali_file:
        # print(len(eng_file), len(fr_file), len(ali_file))
        # , open(result_pos, 'a+') as chat_resolu # add above if we want to save the pos alignments to a file
        for line_eng, line_fr, line_ali in zip(eng_file, fr_file, ali_file):
            pos_fr_list = line_fr.split('\t')[1].split()
            pos_eng_list = line_eng.split('\t')[1].split()
            ali_list = line_ali.split('\t')[1].split() # takes the alignments without the id\t, makes a list of alignments
            # print(pos_fr_list,pos_eng_list,ali_list)
            # print(line_eng, line_fr, line_ali)
            # print(len(pos_fr_list), len(pos_eng_list), len(ali_list), ali_list)
            for ali in ali_list:
                fr_id,eng_id = re.split('-|p', ali)
                # chat_resolu.write(f'{pos_fr_list[int(fr_id)]}-{pos_eng_list[int(eng_id)]} ')
                try:
                    ali_pos_list.append(f'{pos_fr_list[int(fr_id)]}-{pos_eng_list[int(eng_id)]}')
                except:
                    print('out of range: ',fr_id, eng_id)
            all_fr_pos_list.extend(pos_fr_list)
            all_eng_pos_list.extend(pos_eng_list)
    df = pd.DataFrame(ali_pos_list, columns=['alignment_pos'])
    print(df.value_counts())
    c_fr = Counter(all_fr_pos_list)
    c_eng = Counter(all_eng_pos_list)
    print(c_eng, c_fr)
    df.value_counts().to_csv(result_pos)