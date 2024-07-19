import numpy as np

ali_file = 'ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt'
fr_file = 'ali/ChatBotte_MasterCat/ChatBotte_sents.txt'
eng_file = 'ali/ChatBotte_MasterCat/MasterCat_sents.txt'
def create_y_true(ali_file, fr_file, eng_file):
    y_true = []
    with open(ali_file, 'r') as ali_file, open(fr_file, 'r') as fr_file, open(eng_file, 'r') as eng_file:
        for line_ali,line_fr,line_eng in zip(ali_file, fr_file, eng_file):
            len_fr = len(line_fr.split('\t')[1].split())
            len_eng = len(line_eng.split('\t')[1].split())
            ali_true = np.zeros(len_fr*len_eng)
            alis = line_ali.split('\t')[1].split()  # takes the alignments without the id\t, makes a list of strings representing alignments
            alis = [x for x in alis if "p" not in x]
            for ali in alis:
                ali = list(map(int,ali.split('-')))
                ali_true[ali[0]*len_eng+ali[1]] = 1
            y_true.append(ali_true)
    # print(len(y_true),y_true)
    return y_true

if __name__=="__main__":
        
    ali_file = 'ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt'
    fr_file = 'ali/ChatBotte_MasterCat/ChatBotte_sents.txt'
    eng_file = 'ali/ChatBotte_MasterCat/MasterCat_sents.txt'
    create_y_true(ali_file,fr_file,eng_file)