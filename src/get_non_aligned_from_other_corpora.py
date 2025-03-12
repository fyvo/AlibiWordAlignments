from bs4 import BeautifulSoup
import re

def process_sentence_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as infile, open(output_file, 'w') as outfile:
        content = infile.read()
        soup = BeautifulSoup(content, 'html.parser')
        for s_tag in soup.find_all('s'):
            sent_id = str(int(s_tag.get('snum'))-1) # minus one to start counting ids from 0
            sentence = s_tag.get_text().strip()
            outfile.write(f"{sent_id}\t{sentence}\n")


def process_alignment_file(input_file, output_file):
    alignment_data = {}

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            sentence_id, word_id_en, word_id_fr, link_type = line.strip().split()
            word_id_en = str(int(word_id_en)-1)  # minus one to start counting ids from 0
            word_id_fr = str(int(word_id_fr)-1)
            sentence_id = str(int(sentence_id)-1)
            if link_type == "S":
                link = f"{word_id_en}-{word_id_fr}"
            elif link_type == "P":
                link = f"{word_id_en}p{word_id_fr}"

            if sentence_id not in alignment_data:
                alignment_data[sentence_id] = []
            alignment_data[sentence_id].append(link)

    with open(output_file, 'w') as outfile:
        for sentence_id, links in sorted(alignment_data.items(), key=lambda x: int(x[0])):
            outfile.write(f"{sentence_id}\t{' '.join(links)}\n")



def get_lens_of_sents(input_path):
    lens = []
    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile.readlines():
            sent = line.split('\t')[1]
            lens.append(len(sent.split()))
            print(sent, len(sent.split()))
    # print(lens)
    return lens


def get_ids_of_aligned_words(ali_path):
    list_enid_frid = []
    with open(ali_path, 'r', encoding='utf-8') as alifile:
        for line in alifile.readlines():
            alis = line.split('\t')[1].split()
            iden_idfr = [re.split('p|-', ali) for ali in alis]
            set_en = set([int(ali[0]) for ali in iden_idfr])
            set_fr = set([int(ali[1]) for ali in iden_idfr])
            print(set_en, set_fr)
            list_enid_frid.append((set_en, set_fr))
    return list_enid_frid

def get_nb_of_words_ali_non_ali(lens_en, lens_fr, sets_ids_ali):
    n_all_words_en = 0
    n_all_words_fr = 0
    n_non_aligned_en = 0
    n_non_aligned_fr = 0
    n_aligned_en = 0
    n_aligned_fr = 0
    for en_len, fr_len, ids_en_fr in zip(lens_en, lens_fr, sets_ids_ali):
        all_en = set(range(en_len))
        all_fr = set(range(fr_len))
        aligned_en = ids_en_fr[0]
        aligned_fr = ids_en_fr[1]
        non_aligned_en = all_en-aligned_en
        non_aligned_fr = all_fr-aligned_fr
    
        n_all_words_en+=len(all_en)
        n_all_words_fr+=len(all_fr)

        n_aligned_en += len(aligned_en)
        n_aligned_fr += len(aligned_fr)

        n_non_aligned_en += len(non_aligned_en)
        n_non_aligned_fr += len(non_aligned_fr)
    print(f"{n_all_words_en=}, {n_all_words_fr=}, {n_aligned_en=}, {n_aligned_fr=}, {n_non_aligned_en=}, {n_non_aligned_fr=}")
    return n_all_words_en, n_all_words_fr, n_aligned_en, n_aligned_fr, n_non_aligned_en, n_non_aligned_fr

if __name__=='__main__':
   
    en_lens = get_lens_of_sents("hansard_ali/test_pharaoh.e")
    fr_lens = get_lens_of_sents("hansard_ali/test_pharaoh.f")
    list_ids_en_fr = get_ids_of_aligned_words('hansard_ali/test_pharaoh.wa.nonullalign')
    get_nb_of_words_ali_non_ali(en_lens, fr_lens, list_ids_en_fr)
   