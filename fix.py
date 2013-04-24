import xml.etree.ElementTree as ET

def main():
    r = open ('test.xml')
    read = r.read()
    tree = ET.fromstring(read)
    merge(tree)


def merge(tree):
    """tree is what export returns, an ElementTree"""
    #print ET.dump(tree)
    
    new_root = element_builder('WorldCrisis')
    #print ET.dump(new_root), "\n\n"
    element_list = ['DG6345','BLAH']
    kind_list = ["WAR", "blah"]
#    iiter = tree.getiterator(["Crisis"])
    cparent = tree.findall("Crisis")
    for element in cparent:
        x = element.attrib
        #print x["crisisIdent"]
        new_root.append(element)
        #print ET.dump(new_root)

def element_builder(tag, content = ''):
	"""builds 1 xml element with attributes"""
	builder = ET.TreeBuilder()
	
	builder.start(tag, {})
	builder.data(content)
	builder.end(tag)

	print ET.dump(builder.close())
	return builder.close()

main()
