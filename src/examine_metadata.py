import re
import pandas as pd
from bs4 import BeautifulSoup
from extract_leaves import extract_leaves_with_span_info
from extract_all_spans import extract_all_spans
import matplotlib.pyplot as plt
from tabulate import tabulate


def get_nb_sents_nb_words_ratio(sents_file_fr, sents_file_eng):
    # returns number of lines in the sentences file-1 (the last line is empty) and nb of words (separated by spaces)
    nb_words_fr = 0
    with open(sents_file_fr, 'r') as file:
        for i, line in enumerate(file):
            sent_record = line.split('\t')
            nb_words_fr += len(sent_record[1].split())
    nb_words_eng = 0
    with open(sents_file_eng, 'r') as file:
        for i, line in enumerate(file):
            sent_record = line.split('\t')
            nb_words_eng += len(sent_record[1].split())
    print(
        f"number of sentences in {sents_file_fr}: {i}\nnumber of words: {nb_words_fr}")
    print(
        f"number of sentences in {sents_file_eng}: {i}\nnumber of words: {nb_words_eng}")
    print(
        f"Ratio of nb of French/nb of English words: {nb_words_fr/nb_words_eng:.4f}")
    return i, nb_words_fr, nb_words_eng, nb_words_fr/nb_words_eng


def extract_nb_words_in_span(example):
    # regex matching (one or more) digits preceded by underscore, separated by a dash, representing ranges of token ids
    pattern = r"_(\d+-\d+)"
    fr_span, eng_span = re.findall(pattern, example)
    fr_begin, fr_end = fr_span.split('-')
    eng_begin, eng_end = eng_span.split('-')
    return [int(fr_end)-int(fr_begin)+1, int(eng_end)-int(eng_begin)+1]


def check_tree_depth(example):
    # regex matching (one or more) digits preceded by a dot, followed by an underscore (second number in the id)
    pattern = r"\.\d+_"
    depth_str = re.findall(pattern, example)  # ['.8_']
    depth_str = depth_str[0][1:-1]
    return int(depth_str)


def get_distribution_of_span_lengths(df_leaf_spans):
    print(df_leaf_spans['nb_words_fr_span'].value_counts())
    print(df_leaf_spans['nb_words_eng_span'].value_counts())
    plt.subplot(1, 2, 1)
    df_leaf_spans['nb_words_fr_span'].value_counts().plot(
        kind='bar', title='fr nb leaves with x words')
    plt.subplot(1, 2, 2)
    df_leaf_spans['nb_words_eng_span'].value_counts().plot(
        kind='bar', title='eng leaves with x words')
    plt.show()


def count_w2w_alignments(path_ali_w2w):
    with open(path_ali_w2w) as w2w_filehandle:
        w2w_string = w2w_filehandle.read()
    print(
        f"nb of w2w alignments created: {w2w_string.count('-')} sure, {w2w_string.count('p')} potential")
    return w2w_string.count('-'), w2w_string.count('p')


def analyse_alignments(path_ali_xml):
    with open(path_ali_xml, 'r') as ali_filehandle:
        soup = BeautifulSoup(ali_filehandle, 'xml')

    list_dicts_all_spans_by_sentence, dict_all_spans = extract_all_spans(
        soup, separate_by_sentence=True, mark_leaves=True)

    df_all_spans = pd.DataFrame.from_dict(
        dict_all_spans, orient='index').reset_index()
    df_all_spans.columns = ['link_id', 'fr_span', 'eng_span', 'is_leaf']
    df_all_spans['fr_text'] = df_all_spans['fr_span'].map(
        lambda span: span[2])  # span: (beginPos, endPos, string)
    df_all_spans['eng_text'] = df_all_spans['eng_span'].map(
        lambda span: span[2])
    df_all_spans['nb_chars_fr_span'] = df_all_spans['fr_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_all_spans['nb_chars_eng_span'] = df_all_spans['eng_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_all_spans['nb_words_span'] = df_all_spans['link_id'].map(
        extract_nb_words_in_span)
    df_all_spans[['nb_words_fr_span', 'nb_words_eng_span']] = pd.DataFrame(
        df_all_spans.nb_words_span.tolist(), index=df_all_spans.index)
    df_leaf_spans = df_all_spans.loc[(df_all_spans['is_leaf'] == True)]
    df_leaf_spans['tree_depth'] = df_leaf_spans['link_id'].map(
        check_tree_depth)
    get_distribution_of_span_lengths(df_leaf_spans)
    # print(df_leaf_spans[df_leaf_spans['nb_words_fr_span'] > 10]) # print ids of longest leaves!
    # print(
    #     f'Max depth of an alignment tree: {df_leaf_spans["tree_depth"].max()}, in sent id={df_leaf_spans.loc[df_leaf_spans["tree_depth"].idxmax()].link_id.split(".")[0]}')
    # print(
    #     f"Mean number of words in all fr spans: {df_all_spans['nb_words_fr_span'].mean():.3f}\nMean number of words in all eng spans: {df_all_spans['nb_words_eng_span'].mean():.3f}")
    # print(
    #     f"Mean number of words in fr leaf spans: {df_leaf_spans['nb_words_fr_span'].mean(): .3f}\nMean number of words in eng leaf spans: {df_leaf_spans['nb_words_eng_span'].mean(): .3f}")
    # print(
    #     f"Mean number of characters in all fr spans: {df_all_spans['nb_chars_fr_span'].mean():.3f}\nMean number of characters in all eng spans: {df_all_spans['nb_chars_eng_span'].mean():.3f}")
    # print(
    #     f"Mean number of characters in fr leaf spans: {df_leaf_spans['nb_chars_fr_span'].mean(): .3f}\nMean number of characters in eng leaf spans: {df_leaf_spans['nb_chars_eng_span'].mean(): .3f}")
    return len(df_all_spans), len(df_leaf_spans), df_all_spans['nb_words_fr_span'].mean(), df_all_spans['nb_words_eng_span'].mean(), df_leaf_spans['nb_words_fr_span'].mean(), df_leaf_spans['nb_words_eng_span'].mean()


# TODO:
# load two files to get_nb_sents_nb_words and print both lengths and ratio DONE
# extract second number in the id and find max tree depth
# get number of sure and potential w2w alis from the second path in analyse_alignments
# keep in mind that the number of words is a bit strange as sometimes punctuation is separated
if __name__ == "__main__":
    text_ids = ['Auberge', 'Barbe', 'Chat', 'DerniereClasse', 'Vision']
    ali_xml_paths = ["dat/LAuberge_TheInn.ali.xml", "dat/BarbeBleue_BlueBeard.ali.xml",
                     "dat/ChatBotte_MasterCat.ali.xml", "dat/Laderniereclasse_Thelastlesson.ali.xml", "dat/LaVision_TheVision.ali.xml"]
    ali_w2w_paths = ["ali/LAuberge_TheInn/ali_w2w_LAuberge_TheInn.txt", "ali/LaBarbeBleue_BlueBeard/ali_w2w_LaBarbeBleue_BlueBeard.txt",
                     "ali/ChatBotte_MasterCat/ali_w2w_ChatBotte_MasterCat.txt", "ali/LaDerniereClasse_TheLastLesson/ali_w2w_LaDerniereClasse_TheLastLesson.txt", "ali/LaVision_TheVision/ali_w2w_LaVision_TheVision.txt"]
    fr_sents_paths = ["ali/LAuberge_TheInn/LAuberge_sents.txt", "ali/LaBarbeBleue_BlueBeard/LaBarbeBleue_sents.txt",
                      "ali/ChatBotte_MasterCat/ChatBotte_sents.txt", "ali/LaDerniereClasse_TheLastLesson/LaDerniereClasse_sents.txt", "ali/LaVision_TheVision/LaVision_sents.txt"]
    eng_sents_paths = ["ali/LAuberge_TheInn/TheInn_sents.txt", "ali/LaBarbeBleue_BlueBeard/BlueBeard_sents.txt", "ali/ChatBotte_MasterCat/MasterCat_sents.txt",
                       "ali/LaDerniereClasse_TheLastLesson/TheLastLesson_sents.txt", "ali/LaVision_TheVision/TheVision_sents.txt"]
    list_stats = []  # every list here will be a row in the df
    for ali_xml_path, ali_w2w_path, fr_sents_path, eng_sents_path in zip(ali_xml_paths, ali_w2w_paths, fr_sents_paths, eng_sents_paths):
        text_stats = []
        text_stats.extend(get_nb_sents_nb_words_ratio(
            fr_sents_path, eng_sents_path))     # returns 'nb_sentences', 'nb_fr_words', 'nb_eng_words', 'ratio_nb_fr/nb_eng'
        text_stats.extend(count_w2w_alignments(
            ali_w2w_path))  # returns 'nb_sure_ali', 'nb_potential_ali'
        # returns 'nb_all_spans', 'nb_leaf_spans', 'mean_nb_fr_words_all_spans', 'mean_nb_eng_words_all_spans', 'mean_nb_fr_words_leaves', 'mean_nb_eng_words_leaves'
        text_stats.extend(analyse_alignments(ali_xml_path))
        list_stats.append(text_stats)
    stats_df = pd.DataFrame(list_stats, columns=[
                            'nb_sentences', 'nb_fr_words', 'nb_eng_words', 'ratio_nb_fr/nb_eng', 'nb_sure_ali', 'nb_potential_ali', 'nb_all_spans', 'nb_leaf_spans', 'mean_nb_fr_words_all_spans', 'mean_nb_eng_words_all_spans', 'mean_nb_fr_words_leaves', 'mean_nb_eng_words_leaves'])
    stats_df.index = text_ids
    print(tabulate(stats_df, tablefmt="pretty"))
    print(stats_df.to_string())
    stats_df.to_csv('stats_df.csv')
