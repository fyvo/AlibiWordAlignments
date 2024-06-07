import re
import pandas as pd
from bs4 import BeautifulSoup
from extract_leaves import extract_leaves_with_span_info
from extract_all_spans import extract_all_spans

ali_xml_path = "dat/ChatBotte_MasterCat.ali.xml"
ali_w2w_path = "data_processed/ali+_w2w_ChatBotte_MasterCat.txt"
fr_sents_path = "data_processed/ChatBotte_sents.txt"
eng_sents_path = "data_processed/MasterCat_sents.txt"
fr_html_path = ""
eng_html_path = ""

eng_sents = pd.read_csv(eng_sents_path, sep="\t", header=None)
fr_sents = pd.read_csv(fr_sents_path, sep="\t", header=None)
print(eng_sents.head())


# def get_nb_sents(df_all_spans):
#     return nb_sents

# def get_nb_words(df_all_spans):
#     return nb_words

# def get_mean_span_length()
# print(dict_all_spans)
def extract_word_span_length(link_id):
    # regex matching (one or more) digits preceded by underscore, separated by a dash, representing ranges of token ids
    pattern = r"_(\d+-\d+)"
    fr_span, eng_span = re.findall(pattern, link_id)
    fr_begin, fr_end = fr_span.split('-')
    eng_begin, eng_end = eng_span.split('-')
    return {'len_word_span_fr': int(fr_end)-int(fr_begin)+1, 'len_word_span_eng': int(eng_end)-int(eng_begin)+1}


def analyse_alignments(path_ali_xml, path_ali_w2w):
    with open(path_ali_xml, 'r') as filehandle:
        soup = BeautifulSoup(filehandle, 'xml')
    dict_all_spans_by_sentence, dict_all_spans = extract_all_spans(
        soup, separate_by_sentence=True)

    dict_all_leaves_by_sentence, dict_all_leaves = extract_leaves_with_span_info(
        soup, separate_by_sentence=True)
    df_all_spans = pd.DataFrame.from_dict(
        dict_all_spans, orient='index').reset_index()
    df_all_spans.columns = ['link_id', 'fr_span', 'eng_span']
    df_all_spans['fr_text'] = df_all_spans['fr_span'].map(lambda span: span[2])
    df_all_spans['eng_text'] = df_all_spans['eng_span'].map(
        lambda span: span[2])
    df_all_spans['len_fr_span'] = df_all_spans['fr_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_all_spans['len_eng_span'] = df_all_spans['eng_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    print(df_all_spans)
    # mean span len for fr, for eng, for both,
    # mean span len for leaves only
    # max level of imbrication

    df_leaf_spans = pd.DataFrame.from_dict(dict_all_leaves, orient='index', columns=[
        'fr_span', 'eng_span'])
    df_leaf_spans['fr_text'] = df_leaf_spans['fr_span'].map(
        lambda span: span[2])
    df_leaf_spans['eng_text'] = df_leaf_spans['eng_span'].map(
        lambda span: span[2])
    df_leaf_spans['len_fr_span'] = df_leaf_spans['fr_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    df_leaf_spans['len_eng_span'] = df_leaf_spans['eng_span'].map(
        lambda span: int(span[1])-int(span[0])+1)
    print(df_leaf_spans)
    print(
        f"{df_all_spans['len_eng_span'].mean():.3f}, {df_all_spans['len_fr_span'].mean():.3f}")
    print(
        f"{df_leaf_spans['len_eng_span'].mean(): .3f},{df_leaf_spans['len_fr_span'].mean(): .3f}")

    df_all_spans = df_all_spans['link_id'].apply(
        extract_word_span_length)
    print(df_all_spans)


analyse_alignments(ali_xml_path, ali_w2w_path)
