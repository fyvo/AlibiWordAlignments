
from bs4 import BeautifulSoup
from treelib import Node, Tree

def get_link_depth(link_id):
    # extract the second digit which represents the depth
    parts = link_id.split('_')
    return int(parts[0].split('.')[1])

def get_span_ranges_fr_eng(link_id):
    parts = link_id.split('_')
    range_fr = parts[1]
    range_eng = parts[2]
    return range_fr, range_eng

def sort_links(path_ali_xml):
    with open(path_ali_xml, 'r') as ali_filehandle:
        soup = BeautifulSoup(ali_filehandle, 'xml')
    # the first linkList contains linkGroups with all the alignments (linkList level='chunk')
    sorted_linkGroups = []
    linkGroups = soup.linkList.find_all('linkGroup')
    for linkGroup in linkGroups:
        links = linkGroup.find_all('link')
        if not links:
            continue
        sorted_links = sorted(links,key=lambda link: get_link_depth(link['id']))
        sorted_linkGroups.append(sorted_links)
    return sorted_linkGroups

def build_trees_of_all_spans(sorted_linkGroups):
    all_trees = []
    for linkGroup in sorted_linkGroups:
        sentence_tree = Tree()
        for link in linkGroup:
            spans = link.find_all('docSpan')
            range_fr, range_eng = get_span_ranges_fr_eng(link['id'])
            if link['parentID'] == "ROOT":
                sentence_tree.create_node((spans[0].string, spans[1].string,(range_fr,range_eng)),link['id'])  # (range_fr,range_eng) for the content
            else:
                sentence_tree.create_node((spans[0].string, spans[1].string,(range_fr,range_eng)),link['id'],parent=link['parentID'])            
        all_trees.append(sentence_tree)
    return all_trees


if __name__=="__main__":
    sor = sort_links("dat/ChatBotte_MasterCat.ali.xml")
    # print(sor,len(sor))
    all_trees = build_trees_of_all_spans(sor)
    print([(len(tree),tree.depth()) for tree in all_trees])    # .show()
    all_trees[0].to_graphviz()