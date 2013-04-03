#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB1.py
# Copyright (C) 2013
# Taylor McCaslin, Holly Hatfield, Mallory Farr, Wilson Bui, Giovanni Monge, Alex Leonard
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

   #[host, un, pw, database]

def login ( host, un, pw, database ) :
    c = _mysql.connect(
            host = host,
            user = un,
            passwd = pw,
            db = database)
    assert str(type(c)) == "<type '_mysql.connection'>"
    return c

# --------
# Ask Login, IGNORE THIS FUNCTION, hardcoded a
# --------
def ask ():
    sys.stdin.read()
    host = input("What is DB Host? ")
    un = input("What is DB Username? ")
    pw = input("What is DB Password? ")
    database = input("What is Database Name?? ")

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

# ----------
# wcdb2_TRead
# ---------- 

def wcdb2_TRead (r) :
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
  
    return tree

    #NOT VALID CODE, just the idea. Needf to get the file name from w
    #opens file, w, and loads the xml into the WCDB
#    t = query(c, """LOAD XML LOCAL INFILE 'w' 
#			     into table WCDB
#                             rows identified by '<Crisis>' OR '<Organization>' OR '<Person>'
#			""")


def createDB(c):
   t = query(c, "drop table if exists Crisis;")
   t = query(c, "drop table if exists Organization;")
   t = query(c, "drop table if exists Person;")
   t = query(c, "drop table if exists Location;")
   t = query(c, "drop table if exists Kind;")
   t = query(c, "drop table if exists ExternalResources;")
   t = query(c, "drop table if exists PersonRelation;")
   t = query(c, "drop table if exists CrisisRelation;")
   t = query(c, "drop table if exists OrganizationRelation;")
   t = query(c, "drop table if exists HumanImpact;")
   t = query(c, "drop table if exists ResourcesNeeded;")
   t = query(c, "drop table if exists WaysToHelp;")
   print(t)
   
   t = query(
        c,
        """
	create table Crisis (
	  crisisIdent text,
	  Name text,
	  Kind text,
	  StartDateTime dateTime,
	  EndDateTime dateTime,
          EconomicImpact int
	  );""") 
	  
   print("Crisis ",t)
#insert into Crisis values('crisisIdent', 'Name', 'Kind', StartDateTime, EndDateTime, 'EconomicImpact');
   t = query(
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
	  );""") 
	  
   print("Org ",t)
#insert into Organization('organizationIdent', 'Name', 'Kind', 'History','Telephone', 'Fax', 'Email', 'StreetAddress', 'Locality', 'Region', 'PostalCode', 'Country');
   t = query(
        c,
        """
	create table Person (
	  personIdent text,
	  FirstName text,
	  MiddleName text,
	  LastName text,
	  Suffix text,
	  Kind text
	  );""")
	  
   print("Person ",t)
#insert into Person('personIdent', 'FirstName', 'MiddleName', 'LastName', 'Suffix', 'Kind');
   t = query(
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
   print("Location ",t)

#insert into Location('lkey, 'parentIdent', 'Locality', 'Region', 'PostalCode', 'Country');
   t = query(
        c,
        """
	create table Kind (
	  kkey text,
	  parentIdent text,
	  Type text,
	  Name text,
	  Description text
	  );""")
   print("Kind ",t)
   
#insert into Kind('kkey', 'parentIdent', 'Type', 'Name', 'Description');
   t = query(
        c,
        """
	create table ExternalResources (
	  ekey text,
	  parentIdent text,
	  Type text,
	  Value text
	  );""")
   print("External ",t)


#insert into ExternalResources('ekey', 'parentIdent', 'Type', 'Value');
   t = query(
        c,
        """
	create table PersonRelation (
	  personIdent text,
	  otherIdent text,
	  Type text
	  );""")
   print("PersonRelation ",t)


#insert into PersonRelation('personIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table CrisisRelation (
	  crisisIdent text,
	  otherIdent text,
	  Type text
	  );""")
   print("Crisis Relation ",t)


#insert into CrisisRelation('crisisIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table OrganizationRelation (
	  organizationIdent text,
	  otherIdent text,
	  Type text
	  );""")
   print("OrgRelation ",t)


#insert into OrganizationRelation('organizationIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table HumanImpact (
	  parentIdent text,
	  Type text,
	  Number int
	  );""")
   print("HumanImpact ",t)

#insert into HumanImpact('parentIdent', 'Type', 'Number');
   t = query(
        c,
        """
	create table ResourcesNeeded (
	  parentIdent text,
	  ResourceNeeded text
	  );""")
   print("ResroucesNeeded ",t)

#insert into ResourcesNeeded('parentIdent text', 'ResourcesNeeded');
   t = query(
        c,
        """
	create table WaysToHelp (
	  parentIdent text,
	  WaysToHelp text
	  );""")
   print("WaystoHelp ",t)

#insert into WaysToHelp('parentIdent', 'WaysToHelp');

   #t = query(c, "show tables;") #show WCDB2?

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

    c = login(*a)
    tree = wcdb2_TRead (r)
    output1 = wcdb2_write (c, w, tree)
    createDB(c)
    #output2 = wcdb2_write (w, output1)
