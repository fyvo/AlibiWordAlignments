path_pos = "pos_tags/fr_pos_B.txt"
path_words = "ali/LaBarbeBleue_BlueBeard/LaBarbeBleue_sents.txt"

with open(path_pos, 'r') as pos, open(path_words,'r') as words:
    for lines in zip(pos,words):
        for line in lines:
            print(line,len(line))
        break