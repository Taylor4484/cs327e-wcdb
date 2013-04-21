# -------
# imports
# -------

import sys
from WCDB3 import wcdb2_solve

# ----
# main
# ----

r = open('WCDB2.xml', 'r')
w = open('RunWCDB3.xml', 'w')

wcdb2_solve(r,w)

r.close()
w.close()
