# -------
# imports
# -------

import sys
from WCDB3 import wcdb3_solve

# ----
# main
# ----

r = open('WCDB3.xml', 'r')
w = open('RunWCDB3.xml', 'w')

wcdb3_solve(r,w)

r.close()
w.close()
