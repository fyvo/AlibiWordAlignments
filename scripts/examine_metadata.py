import re
import pandas as pd
from bs4 import BeautifulSoup
from extract_leaves import extract_leaves_with_span_info
from extract_all_spans import extract_all_spans


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


def count_w2w_alignments(path_ali_w2w):
    with open(path_ali_w2w) as w2w_filehandle:
        w2w_string = w2w_filehandle.read()
    print(
        f"nb of w2w alignments created: {w2w_string.count('-')} sure, {w2w_string.count('p')} potential")


def analyse_alignments(path_ali_xml, path_ali_w2w):
    with open(path_ali_xml, 'r') as ali_filehandle:
        soup = BeautifulSoup(ali_filehandle, 'xml')

    list_dicts_all_spans_by_sentence, dict_all_spans = extract_all_spans(
        soup, separate_by_sentence=True)

    list_dicts_leaf_spans_by_sentence, dict_all_leaves = extract_leaves_with_span_info(
        soup, separate_by_sentence=True)
    df_all_spans = pd.DataFrame.from_dict(
        dict_all_spans, orient='index').reset_index()
    df_all_spans.columns = ['link_id', 'fr_span', 'eng_span']

    df_leaf_spans = pd.DataFrame.from_dict(
        dict_all_leaves, orient='index').reset_index()

    df_leaf_spans.columns = ['link_id', 'fr_span', 'eng_span']

    df_all_spans['fr_text'] = df_all_spans['fr_span'].map(lambda span: span[2])
    df_all_spans['eng_text'] = df_all_spans['eng_span'].map(
        lambda span: span[2])
    # print(df_all_spans)
    df_all_spans['nb_chars_fr_span'] = df_all_spans['fr_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_all_spans['nb_chars_eng_span'] = df_all_spans['eng_span'].map(
        lambda span: int(span[1])-int(span[0])+1)

    df_leaf_spans['fr_text'] = df_leaf_spans['fr_span'].map(
        lambda span: span[2])
    df_leaf_spans['eng_text'] = df_leaf_spans['eng_span'].map(
        lambda span: span[2])
    df_leaf_spans['nb_chars_fr_span'] = df_leaf_spans['fr_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_leaf_spans['nb_chars_eng_span'] = df_leaf_spans['eng_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    print(f"number of all spans: {len(df_all_spans)}")
    print(f"number of leaf spans: {len(df_leaf_spans)}")
    df_all_spans['nb_words_span'] = df_all_spans['link_id'].map(
        extract_nb_words_in_span)
    df_all_spans[['nb_words_fr_span', 'nb_words_eng_span']] = pd.DataFrame(
        df_all_spans.nb_words_span.tolist(), index=df_all_spans.index)
    df_leaf_spans['nb_words_span'] = df_leaf_spans['link_id'].map(
        extract_nb_words_in_span)
    df_leaf_spans[['nb_words_fr_span', 'nb_words_eng_span']] = pd.DataFrame(
        df_leaf_spans.nb_words_span.tolist(), index=df_leaf_spans.index)
    df_leaf_spans['tree_depth'] = df_leaf_spans['link_id'].map(
        check_tree_depth)
    print(
        f'Max depth of an alignment tree: {df_leaf_spans["tree_depth"].max()}')
    print(
        f"Mean number of words in all fr spans: {df_all_spans['nb_words_fr_span'].mean():.3f}\nMean number of words in all eng spans: {df_all_spans['nb_words_eng_span'].mean():.3f}")
    print(
        f"Mean number of words in fr leaf spans: {df_leaf_spans['nb_words_fr_span'].mean(): .3f}\nMean number of words in eng leaf spans: {df_leaf_spans['nb_words_eng_span'].mean(): .3f}")
    print(
        f"Mean number of characters in all fr spans: {df_all_spans['nb_chars_fr_span'].mean():.3f}\nMean number of characters in all eng spans: {df_all_spans['nb_chars_eng_span'].mean():.3f}")
    print(
        f"Mean number of characters in fr leaf spans: {df_leaf_spans['nb_chars_fr_span'].mean(): .3f}\nMean number of characters in eng leaf spans: {df_leaf_spans['nb_chars_eng_span'].mean(): .3f}")

    print


# TODO:
# load two files to get_nb_sents_nb_words and print both lengths and ratio DONE
# extract second number in the id and find max tree depth
# get number of sure and potential w2w alis from the second path in analyse_alignments
# write the stats in a file for all texts
# keep in mind that the number of words is a bit strange as sometimes punctuation is separated
if __name__ == "__main__":

    ali_xml_path = "dat\BarbeBleue_BlueBeard.ali.xml"
    ali_w2w_path = "data_processed/ali+_w2w_ChatBotte_MasterCat.txt"
    fr_sents_path = "data_processed\LAuberge_sents.txt"
    eng_sents_path = "data_processed\TheInn_sents.txt"
    fr_html_path = ""
    eng_html_path = ""

    eng_sents = pd.read_csv(eng_sents_path, sep="\t", header=None)
    fr_sents = pd.read_csv(fr_sents_path, sep="\t", header=None)

    get_nb_sents_nb_words_ratio(fr_sents_path, eng_sents_path)
    count_w2w_alignments(
        "data_processed/ali+_w2w_LaVision_TheVision.txt")
    analyse_alignments(ali_xml_path, ali_w2w_path)
