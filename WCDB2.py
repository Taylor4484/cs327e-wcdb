#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB1.py
# Copyright (C) 2013
# Taylor McCaslin
# ---------------------------

#CHANGE THE BELOW CREDITIALS TO YOUR DESIRED DATABASE
# creds = [host, username, password, database]


# -------
# imports
# -------

import sys
import xml.etree.ElementTree as ET

# --------
# DB Login
# --------

import _mysql

def login ( host, un, pw, database ) :
    c = _mysql.connect(
            host   = host,
            user   = un,
            passwd = pw,
            db     = database)
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

# --------
# Ask Login
# --------
def ask ():
    host = input("What DB Host? ")
    un = input("What DB Username? ")
    pw = input("What DB Password? ")
    database = input("What Database Name?? ")

    a = [host, un, pw, database]
    login(*a)
    print("login successful")
    return a
    
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
    login(*creds)
    tree = wcdb1_read (r)
    output1 = wcdb1_write (w, tree)
    #output2 = wcdb1_write (w, output1)
    
