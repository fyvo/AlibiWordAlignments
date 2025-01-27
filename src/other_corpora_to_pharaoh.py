from bs4 import BeautifulSoup

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

if __name__=="__main__":

    input_file = "europarl_ali/en-fr_1-100(1).wa" 
    output_file = "europarl_ali/en-fr_pharaoh.wa"
    process_alignment_file(input_file, output_file)

    input_file = "europarl_ali/1-100-final(1).fr" 
    output_file = "europarl_ali/1-100_pharaoh.fr"
    process_sentence_file(input_file, output_file)

    input_file = "europarl_ali/1-100-final(2).en" 
    output_file = "europarl_ali/1-100_pharaoh.en"
    process_sentence_file(input_file, output_file)


    input_file = "hansard_ali/test.wa.nonullalign" 
    output_file = "hansard_ali/test_pharaoh.wa.nonullalign"
    process_alignment_file(input_file, output_file)

    input_file = "hansard_ali/test.e" 
    output_file = "hansard_ali/test_pharaoh.e"
    process_sentence_file(input_file, output_file)

    input_file = "hansard_ali/test.f" 
    output_file = "hansard_ali/test_pharaoh.f"
    process_sentence_file(input_file, output_file)

