import xml.etree.ElementTree as ET
import glob
import pickle


list_of_fragments = []

#### The Hamta corpus should be located in the same directory
#### The data could be downloaded from following link
#### http://ictrc.ac.ir/plagdet/PersianPlagdet2016-text-alignment-corpus.rar

xml_files = glob.glob('dataset/04-simulated-obfuscation/*.xml')

for files in xml_files:
    tree = ET.parse(files)
    root = tree.getroot()
    sus_file = root.attrib["reference"]
    for child in root:
        sus_start = int(child.attrib["this_offset"])
        sus_end = sus_start + int(child.attrib["this_length"])
        source_file = child.attrib["source_reference"]
        source_start = int(child.attrib["source_offset"])
        source_end = source_start + int(child.attrib["source_length"])
        with open("src/"+source_file,'r') as f:
            source_text = f.read()
        with open("susp/"+sus_file,'r') as f:
            sus_text = f.read()
        list_of_fragments.append((source_text[source_start:source_end+1],sus_text[sus_start:sus_end+1]))

with open("data/list_of_fragments.LIST", 'wb') as f:
    pickle.dump(list_of_fragments, f)

