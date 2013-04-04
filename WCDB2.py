#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB1.py
# Copyright (C) 2013
# Taylor McCaslin, Holly Hatfield, Mallory Farr, Wilson Bui, Giovanni Monge, Alex Leonard
# ---------------------------s
# -------
# imports
# -------

import sys
import _mysql
import lxml.etree as ET

# --------
# DB Login
# --------

a = [host, un, pw, database] 
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

   query(c, "drop table if exists Crisis;")
   query(c, "drop table if exists Organization;")
   query(c, "drop table if exists Person;")
   query(c, "drop table if exists Location;")
   query(c, "drop table if exists Kind;")
   query(c, "drop table if exists ExternalResources;")
   query(c, "drop table if exists PersonRelation;")
   query(c, "drop table if exists CrisisRelation;")
   query(c, "drop table if exists OrganizationRelation;")
   query(c, "drop table if exists HumanImpact;")
   query(c, "drop table if exists ResourcesNeeded;")
   query(c, "drop table if exists WaysToHelp;")
   
   t = query(
        c,
        """
	create table Crisis (
	  crisisIdent text,
	  Name text,
	  Kind text,
	  StartDateTime dateTime,
	  EndDateTime dateTime,
      EconomicImpact text
	  );""") 
	  
#insert into Crisis values('crisisIdent', 'Name', 'Kind', StartDateTime, EndDateTime, 'EconomicImpact');
   t = query(
        c,
        """
	create table Organization (
	  organizationIdent text,
	  Name text,
	  Kind text,
	  History mediumtext,
	  Telephone text,
	  Fax text,
	  Email text,
	  StreetAddress text,
	  Locality text,
	  Region text,
	  PostalCode text,
	  Country text
	  );""") 
	  
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
	  
#insert into Person('personIdent', 'FirstName', 'MiddleName', 'LastName', 'Suffix', 'Kind');
   t = query(
        c,
        """
	create table Location (
	  parentIdent text,
	  Locality text,
	  Region text,
	  Country text
	  );""")

#insert into Location(parentIdent', 'Locality', 'Region', 'PostalCode', 'Country');
   t = query(
        c,
        """
	create table Kind (
	  parentIdent text,
	  Type text,
	  Name text,
	  Description text
	  );""")
   
#insert into Kind('parentIdent', 'Type', 'Name', 'Description');
   t = query(
        c,
        """
	create table ExternalResources (
	  parentIdent text,
	  Type text,
	  Value text
	  );""")

#insert into ExternalResources('parentIdent', 'Type', 'Value');
   t = query(
        c,
        """
	create table PersonRelation (
	  personIdent text,
	  otherIdent text,
	  Type text
	  );""")


#insert into PersonRelation('personIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table CrisisRelation (
	  crisisIdent text,
	  otherIdent text,
	  Type text
	  );""")


#insert into CrisisRelation('crisisIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table OrganizationRelation (
	  organizationIdent text,
	  otherIdent text,
	  Type text
	  );""")

#insert into OrganizationRelation('organizationIdent', 'otherIdent', 'Type');
   t = query(
        c,
        """
	create table HumanImpact (
	  parentIdent text,
	  Type text,
	  Number int
	  );""")

#insert into HumanImpact('parentIdent', 'Type', 'Number');
   t = query(
        c,
        """
	create table ResourcesNeeded (
	  parentIdent text,
	  ResourceNeeded text
	  );""")

#insert into ResourcesNeeded('parentIdent text', 'ResourcesNeeded');
   t = query(
        c,
        """
	create table WaysToHelp (
	  parentIdent text,
	  WaysToHelp text
	  );""")

#insert into WaysToHelp('parentIdent', 'WaysToHelp');

   #t = query(c, "show tables;") 
    
   return None

	
def process_crisis (c, tree) :

	inserts = []
	parentkey = []
	kind = []
	relatedperson = []
	relatedorg = []
	ExternalResource = []
	i=0
	#iterats over Parents	
	for parent in tree.findall('Crisis'):
	    insert = {}
	    
	    parentkey.append(parent.get('crisisIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.tag == 'Kind':
	        	kind.append(element.get('crisisKindIdent'))
	        if element.tag == 'RelatedOrganization':
	        	relatedorg.append((parentkey[i], element.get('organizationIdent'), 'Organization'))
	        if element.tag == 'RelatedPerson':
	        	relatedperson.append((parentkey[i], element.get('personIdent'), 'Person'))
	        if element.tag == 'ImageURL':
	        	ExternalResource.append((parentkey[i], 'Image' , element.text))
	        if element.tag == 'VideoURL':
	        	ExternalResource.append((parentkey[i], 'Video' , element.text))
	        if element.tag == 'MapURL':
	        	ExternalResource.append((parentkey[i], 'Map' , element.text))
	        if element.tag == 'SocialNetworkURL':
	        	ExternalResource.append((parentkey[i], 'Social' , element.text))
	        if element.tag == 'Citation':
	        	ExternalResource.append((parentkey[i], 'Citation' , element.text))
	        if element.tag == 'ExternalLinkURL':
	        	ExternalResource.append((parentkey[i], 'External' , element.text))
	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    i += 1
	    
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
		
		#QueryBuilding - Crisis Table
		d = inserts[i]	
		s = (parentkey[i], d.get('Name','Null'), kind[i], d.get('Date', 'Null'), 'Null', d.get('EconomicImpact', 'Null'))
		s = 'insert into Crisis values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
		
		#QueryBuilding - HumanImpact Table
		s = (parentkey[i], d.get('Type','Null'), d.get('Number', 'Null'))
		s = 'insert into HumanImpact values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
		#QueryBuilding - ResourcesNeeded Table
		s = (parentkey[i], d.get('ResourcesNeeded', 'Null'))
		s = 'insert into ResourcesNeeded values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
		#QueryBuilding - WaysToHelp Table
		s = (parentkey[i], d.get('WaysToHelp', 'Null'))
		s = 'insert into WaysToHelp values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into CrisisRelation values' + str(s) + ';'
		t = query(c,s)	
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into CrisisRelation values' + str(s) + ';'
		t = query(c,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(c,s)	
	
	#t = query(c,"select * from ExternalResources;")
	#print(t)




def process_org (c, tree) :

	inserts = []
	parentkey = []
	kind = []
	relatedperson = []
	relatedcrisis = []
	ExternalResource = []
	i=0
	#iterats over Parents	
	for parent in tree.findall('Organization'):
	    insert = {}
	    
	    parentkey.append(parent.get('organizationIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.tag == 'Kind':
	        	kind.append(element.get('organizationKindIdent'))
	        if element.tag == 'RelatedPerson':
	        	relatedperson.append((parentkey[i], element.get('personIdent'), 'Person'))
	        if element.tag == 'RelatedCrisis':
	        	relatedcrisis.append((parentkey[i], element.get('crisisIdent'), 'Crisis'))
	        if element.tag == 'ImageURL':
	        	ExternalResource.append((parentkey[i], 'Image' , element.text))
	        if element.tag == 'VideoURL':
	        	ExternalResource.append((parentkey[i], 'Video' , element.text))
	        if element.tag == 'MapURL':
	        	ExternalResource.append((parentkey[i], 'Map' , element.text))
	        if element.tag == 'SocialNetworkURL':
	        	ExternalResource.append((parentkey[i], 'Social' , element.text))
	        if element.tag == 'Citation':
	        	ExternalResource.append((parentkey[i], 'Citation' , element.text))
	        if element.tag == 'ExternalLinkURL':
	        	ExternalResource.append((parentkey[i], 'External' , element.text))
	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    i += 1
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
		
		#QueryBuilding - Organization Table
		d = inserts[i]	
		s = (parentkey[i], d.get('Name','Null'), kind[i], d.get('History', 'Null'), d.get('Telephone', 'Null'), d.get('Fax', 'Null'), d.get('Email', 'Null'),  d.get('StreetAddress', 'Null'), d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('PostalCode', 'Null'), d.get('Country', 'Null') )
		s = 'insert into Organization values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into OrganizationRelation values' + str(s) + ';'
		t = query(c,s)	
	
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into OrganizationRelation values' + str(s) + ';'
		t = query(c,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(c,s)	
	
	
def process_person (c, tree) :

	inserts = []
	parentkey = []
	kind = []
	relatedorg = []
	relatedcrisis = []
	ExternalResource = []
	i=0
	#iterats over Parents	
	for parent in tree.findall('Person'):
	    insert = {}
	    
	    parentkey.append(parent.get('personIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.tag == 'Kind':
	        	kind.append(element.get('personKindIdent'))
	        if element.tag == 'RelatedOrganization':
	        	relatedorg.append((parentkey[i], element.get('organizationIdent'), 'Organization'))
	        if element.tag == 'RelatedCrisis':
	        	relatedcrisis.append((parentkey[i], element.get('crisisIdent'), 'Crisis'))
	        if element.tag == 'ImageURL':
	        	ExternalResource.append((parentkey[i], 'Image' , element.text))
	        if element.tag == 'VideoURL':
	        	ExternalResource.append((parentkey[i], 'Video' , element.text))
	        if element.tag == 'MapURL':
	        	ExternalResource.append((parentkey[i], 'Map' , element.text))
	        if element.tag == 'SocialNetworkURL':
	        	ExternalResource.append((parentkey[i], 'Social' , element.text))
	        if element.tag == 'Citation':
	        	ExternalResource.append((parentkey[i], 'Citation' , element.text))
	        if element.tag == 'ExternalLinkURL':
	        	ExternalResource.append((parentkey[i], 'External' , element.text))
	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    i += 1
	    
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
		
		#QueryBuilding - Person Table
		d = inserts[i]	
		s = (parentkey[i], d.get('FirstName','Null'), d.get('MiddleName', 'Null'), d.get('LastName', 'Null'), d.get('Suffix', 'Null'), kind[i])
		s = 'insert into Person values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(c,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into PersonRelation values' + str(s) + ';'
		t = query(c,s)	
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into PersonRelation values' + str(s) + ';'
		t = query(c,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(c,s)	
	
	
	
def process_kind(c, tree) :


	#Query Building CrisisKind
	inserts = []
	parentkey = []
	#iterats over Parents	
	for parent in tree.findall('CrisisKind'):
	    insert = {}
	    
	    parentkey.append(parent.get('crisisKindIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
	
		#QueryBuilding - Kind Table
		d = inserts[i]	
		s = (parentkey[i], 'Crisis', d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into Kind values' + str(s) + ';'
		t = query(c,s)	
		
		
	#Query Building OrganizationKind
	inserts = []
	parentkey = []
	#iterats over Parents	
	for parent in tree.findall('OrganizationKind'):
	    insert = {}
	    
	    parentkey.append(parent.get('organizationKindIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
	
		#QueryBuilding - Kind Table
		d = inserts[i]	
		s = (parentkey[i], 'Organization', d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into Kind values' + str(s) + ';'
		t = query(c,s)	


	#Query Building PersonKind
	inserts = []
	parentkey = []
	#iterats over Parents	
	for parent in tree.findall('PersonKind'):
	    insert = {}
	    
	    parentkey.append(parent.get('personKindIdent'))
	    
	    #Iterates over Children & Subchildren
	    for element in parent.iterdescendants():

	        if element.getchildren() == []:
	            insert[element.tag] = element.text
	    
	    inserts.append(insert)
	    
	#QueryBuilding Loop    
	for i in xrange(0, len(parentkey)):
	
		#QueryBuilding - Kind Table
		d = inserts[i]	
		s = (parentkey[i], 'Person', d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into Kind values' + str(s) + ';'
		t = query(c,s)		
	
	t = query(c,"select * from Kind;")
    
# -------------
# wcdb2_import
# -------------

def wcdb2_import(c, tree):

    process_crisis(c, tree)
    process_person(c, tree)
    process_org(c, tree)

    process_kind(c, tree)
    
    return None


# -------------
# wcdb2_export
# -------------

def wcdb2_export():
	#I'm going to go cry now.... 
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
    wcdb2_import(c, tree)
