from sklearn.metrics import roc_auc_score
from create_y_true import create_y_true
import numpy as np
ali_file = 'ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt'
fr_file = 'ali/ChatBotte_MasterCat/ChatBotte_sents.txt'
eng_file = 'ali/ChatBotte_MasterCat/MasterCat_sents.txt'

y_true = create_y_true(ali_file,fr_file,eng_file)
y_true = np.concatenate(y_true).ravel().tolist()
y_score = [0.25 for x in range (len(y_true))]
print(roc_auc_score(y_true,y_score))