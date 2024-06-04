import xml.etree.ElementTree as ET

alignment_xml_path = 'dat\ChatBotte_MasterCat.ali.xml'
tree = ET.parse(alignment_xml_path)
root = tree.getroot()
print(type(tree), type(root))
print(f"Root tag: {root.tag}")
for child in root:
    print(f"Children tags with attrib:{child.tag}, {child.attrib}")
link_list_level_chunk = root[1]
link_list_level_token = root[2]
print(link_list_level_chunk.attrib, link_list_level_token.attrib)


print(root.findall(
    "./linkList/linkGroup/link[@parentID'='ROOT']/"))


def extract_sentences(link_list_level_chunk):
    sentence_tuples = []
    for link_group in link_list_level_chunk:
        for link in link_group:
            if link.get('parentID') == "ROOT":
                sentence_tuples.append((link[0].text, link[1].text))
    return sentence_tuples


sents = extract_sentences(link_list_level_chunk)

path_eng = "scripts/sents_ChatBotte_eng.txt"
path_fr = "scripts/sents_ChatBotte_fr.txt"


def write_eng_fr_to_files(sentences_tuple, path_eng_file, path_fr_file):
    with open(path_eng_file, 'w') as eng_file, open(path_fr_file, 'w') as fr_file:
        for i, sent_pair in enumerate(sentences_tuple):
            fr_file.write(f'{i}    {sent_pair[0]}')
            print(f'{i} {sent_pair[1]}')
            eng_file.write(f'{i}    {sent_pair[1]}')


write_eng_fr_to_files(sents, path_eng, path_fr)
