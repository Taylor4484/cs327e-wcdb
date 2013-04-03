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
	  crisisIdent text,
	  Name text,
	  Kind text,
	  Location text,
	  StartDateTime dateTime,
	  EndDateTime dateTime,
          EconomicImpact int
			);
	""") 

    t = Query.query(
        c,
        """
	create table Organization (
	  organizationIdent text,
	  Name text,
	  Kind text,
	  History text,
	  Telephone text,
	  Fax text,
	  Email text,
	  StreetAddress text,
	  Locality text,
	  Region text,
	  PostalCode text,
	  Country text
	  );
	""") 

    t = Query.query(
        c,
        """
	create table Person (
	  personIdent text,
	  FirstName text,
	  MiddleName text,
	  LastName text,
	  Suffix text,
	  Kind text
	  );
	""")

    t = Query.query(
        c,
        """
	create table Location (
	  lkey text,
	  parentIdent text,
	  Locality text,
	  Region text,
	  PostalCode text,
	  Country text
	);""")

    t = Query.query(
        c,
        """
	create table Kind (
	  kkey text,
	  parentIdent text,
	  Type text,
	  Name text,
	  Description text
	);""")

    t = Query.query(
        c,
        """
	create table ExternalResources (
	  ekey text,
	  parentIdent text,
	  Type text,
	  Value text
	);""")
    t = Query.query(
        c,
        """
	create table PersonRelation (
	  personIdent text,
	  otherIdent text,
	  Type text
	);""")
    t = Query.query(
        c,
        """
	create table CrisisRelation (
	  crisisIdent text,
	  otherIdent text,
	  Type text
	);""")

    t = Query.query(
        c,
        """
	create table OrganizationRelation (
	  organizationIdent text,
	  otherIdent text,
	  Type text
	);""")

    t = Query.query(
        c,
        """
	create table HumanImpact (
	  parentIdent text,
	  Type text,
	  Number int
	);""")

    t = Query.query(
        c,
        """
	create table ResourcesNeeded (
	  parentIdent text,
	  ResourceNeeded text,
	);""")

    t = Query.query(
        c,
        """
	create table WaysToHelp (
	  parentIdent text,
	  WaysToHelp text
	);""")




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
    
