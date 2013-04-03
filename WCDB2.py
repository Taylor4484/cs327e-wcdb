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
import _mysql
import xml.etree.ElementTree as ET

# --------
# DB Login
# --------

import _mysql

def login ( host, un, pw, database ) :
    c = _mysql.connect(
            host = host,
            user = un,
            passwd = pw,
            db = database)
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

# --------
# Ask Login
# --------
def ask ():
    sys.stdin.read()
    host = input("What DB Host? ")
    un = input("What DB Username? ")
    pw = input("What DB Password? ")
    database = input("What Database Name?? ")

    a = [host, un, pw, database]
    c = login(*a)
    print("login successful")
    return c

# ----------
# Pose Query
# ---------- 

def query (c, s) :
    assert str(type(c)) == "<type '_mysql.connection'>"
    assert type(s) is str
    c.query(s)
    r = c.use_result()
    if r is None :
        return None
    assert str(type(r)) == "<type '_mysql.result'>"
    t = r.fetch_row(maxrows = 0)
    assert type(t) is tuple
    return t



def wcdb2_TRead (c, r) :
    """
    reads an input
    creates an element tree from string
    """
    read = r.read()

    tree = ET.fromstring(read)


    return tree


# ------------
# wcdb2_write
# ------------

def wcdb2_write (c, w, tree) :
    """
    reads an input
    creates an element tree from string
    """
    tree2 = ET.tostring(tree)
    w.write(tree2)
  

    #NOT VALID CODE, just the idea. Needf to get the file name from w
    #opens file, w, and loads the xml into the WCDB
    t = Query.query(c, """LOAD XML LOCAL INFILE 'w' 
    		     into table WCDB
                             rows identified by '<Crisis>' OR '<Organization>' OR '<Person>'
			""")


    return tree


def createDB()
   t = Query.query(c, "drop table if exists WCDB2")

   t = Query.query(
        c,
        """

	create table Crisis (
	  Name text,
	  Kind text,
	  Location text,
	  StartDateTime dateTime,
	  EndDateTime dateTime,
	  HumanImpact DICT,
          EconomicImpact text,
          ResourcesNeeded text,
          WaysToHelp text,
          ExternalResources ARRAY,
          RelatedPersons ARRAY,
	  RelatedOrganizations ARRAY
			);
	""") 

    t = Query.query(
        c,
        """
	create table Organization (
	  Name text,
	  Kind text,
	  Location text,
	  Historytext,
	  ContactInfo ARRAY OF DICT,
	  ExternalResources ARRAY,
	  RelatedCrisis ARRAY,
          RelatedPersons ARRAY
	  );
	""") 

    t = Query.query(
        c,
        """
	create table People (
	  Name text,
	  Kind text,
	  Location text,
	  RelatedCrisis ARRAY,
	  RelatedOrganizations ARRAY
	  );
	""")

    t = Query.query(c, "show databases") #show WCDB2?

    print "WCDB2 created!"
    return None

# -------------
# wcdb2_solve
# -------------

def wcdb2_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """

    c = ask()
    tree = wcdb2_TRead (c,r)
    output1 = wcdb2_write (c, w, tree)
    #output2 = wcdb2_write (w, output1)
