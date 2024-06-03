import xml.etree.ElementTree as ET

tree = ET.parse('dat\ChatBotte_MasterCat.ali.xml')
root = tree.getroot()
print(type(tree), type(root))
print(f"Root tag: {root.tag}")
for child in root:
    print(child.tag, child.attrib)
link_list_level_chunk = root[1]
link_list_level_token = root[2]
print(link_list_level_chunk.tag, link_list_level_token.tag)
