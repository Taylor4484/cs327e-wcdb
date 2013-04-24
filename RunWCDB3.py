# -------
# imports
# -------

import sys
from WCDB3 import wcdb3_solve

# ----
# main
# ----

#r = open('WCDB3.xml', 'r')

#Files to be Read
xml_files = ['Bonsai-WCDB3.xml', 'Miner-WCDB3.xml', 'Poseidon-WCDB3.xml', 'Virus-WCDB3.xml', 'Byte-Me-WCDB3.xml', 'IsYuchenHereToday-WCDB3.xml', 'Tech-Knuckle-Support-WCDB3.xml', 'Better-Late-Than-Never-WCDB3.xml']
#Missing File
#'Nameless-WCDB3.xml',

#OutFile
w = open('RunWCDB3.xml', 'w')


wcdb3_solve(xml_files, w)

w.close()
