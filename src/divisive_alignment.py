from extract_sentences import extract_sentences

fr_sents_paths = ["ali/LAuberge_TheInn/LAuberge_sents.txt", "ali/LaBarbeBleue_BlueBeard/LaBarbeBleue_sents.txt",
                  "ali/ChatBotte_MasterCat/ChatBotte_sents.txt", "ali/LaDerniereClasse_TheLastLesson/LaDerniereClasse_sents.txt", "ali/LaVision_TheVision/LaVision_sents.txt"]
eng_sents_paths = ["ali/LAuberge_TheInn/TheInn_sents.txt", "ali/LaBarbeBleue_BlueBeard/BlueBeard_sents.txt", "ali/ChatBotte_MasterCat/MasterCat_sents.txt",
                   "ali/LaDerniereClasse_TheLastLesson/TheLastLesson_sents.txt", "ali/LaVision_TheVision/TheVision_sents.txt"]
ali_xml_paths = ["dat/LAuberge_TheInn.ali.xml", "dat/BarbeBleue_BlueBeard.ali.xml",
                     "dat/ChatBotte_MasterCat.ali.xml", "dat/Laderniereclasse_Thelastlesson.ali.xml", "dat/LaVision_TheVision.ali.xml"]
# fr_sents, eng_sents = [], []
# for path_fr, path_eng in zip(fr_sents_paths, eng_sents_paths):
#     list_words_fr = []
#     list_words_eng = []
#     with open(path_fr, 'r') as file:
#         for i, line in enumerate(file):
#             sent_record = line.split('\t')
#             list_words_fr.append(sent_record[1].split())
#     with open(path_eng, 'r') as file:
#         for i, line in enumerate(file):
#             sent_record = line.split('\t')
#             list_words_eng.append(sent_record[1].split())
#     fr_sents.append(list_words_fr)
#     eng_sents.append(list_words_eng)
# def align(fr_span, eng_span):
#     if len(fr_span)==1 or len(eng_span)==1:
#          alignments = []
#          return alignments
#     min_ncut = 2
#     fr_subspan, eng_subspan = fr_span, eng_span
#     for i,fr_token in enumerate(fr_span):
#         for j,eng_token in enumerate(eng_span):

#     align()
#     align()
                 



for path in ali_xml_paths:
    sent_tuple = extract_sentences(path, is_path=True)
    
# iterate through all sent pairs to build #-sents similarity matrices that contain a score for every pair of words
# divide consecutively the matrix at indices that return a minimal similarity score for the non-aligned segments 
# when there's one word left OR when the similarity is low enough
# simalign uses cosine similarity BUT we have a paper about csls
    # for fr_sent, eng_sent in sent_tuple:
    #     align(fr_sent, eng_sent)
                       
def Ncut(A, B):
    # Placeholder function for cut value calculation
    # Needs to be defined based on specific problem
    return (A[0]+B[0])/2

def align(S, T):
    if len(S) == 1 or len(T) == 1:
        # Link each word of S to each word of T
        for s in S:
            for t in T:
                print(f"Link {s} to {t}")
        return
    
    minNcut = 2
    X, Y = S, T
    
    I = len(S)
    J = len(T)
    
    for i in range(2, I+1):
        for j in range(2, J+1):
            A = S[:i]
            B = T[:j]
            if Ncut(A, B) < minNcut:
                minNcut = Ncut(A, B)
                X, Y = A, B
            B_bar = T[j:]
            if Ncut(A, B_bar) < minNcut:
                minNcut = Ncut(A, B_bar)
                X, Y = A, B_bar
    
    align(X, Y)
    align(S[len(X):], T[len(Y):])

# Example usage (pseudo code):
S = ["word1", "word2", "word3"]
T = ["wordA", "wordB", "wordC"]
align(S, T)