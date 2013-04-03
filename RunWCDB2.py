# -------
# imports
# -------

import sys
from WCDB2 import login
from WCDB2 import query

from WCDB2 import wcdb2_solve

# ----
# main
# ----

r = open('WCDB2.xml', 'r')
w = open('RunWCDB2.out.xml', 'w')

wcdb2_solve(r,w)

r.close()
w.close()
