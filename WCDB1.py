#Create an import/export facility from the XML into Element Tree and back.
#The import facility must import from a file.
#The file is guaranteed to have validated XML.
#The export facility must export to a file.
#Import/export the XML on only the ten crises, ten organizations, and ten people of the group.

#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB1.py
# Copyright (C) 2013
# Taylor McCaslin
# ---------------------------


# -------
# imports
# -------

import sys
import xml.etree.ElementTree as ET


# ------------
# wcdb1_read
# ------------

def wcdb1_read (r) :
    """
    reads an input
    creates an element tree from string
    """
    read = r.read()

    tree = ET.fromstring(read)

    return tree


# ------------
# wcdb1_write
# ------------

def wcdb1_write (w, tree) :
    """
    reads an input
    creates an element tree from string
    """
    tree2 = ET.tostring(tree)
    w.write(tree2)
    return tree

# -------------
# wcdb1_solve
# -------------

def wcdb1_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """

    tree = wcdb1_read (r)
    output1 = wcdb1_write (w, tree)
    #output2 = wcdb1_write (w, output1)
    
