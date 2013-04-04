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
import xml.etree.ElementTree

# --------
# DB Login
# --------
	
a = [host, un, pw, database]
   #[host, un, pw, database]

def wcdb2_login ( host, un, pw, database ) :
	"""takes credentials and logs into DB"""
	login = _mysql.connect(
			host = host,
			user = un,
			passwd = pw,
			db = database)
	assert str(type(login)) == "<type '_mysql.connection'>"
	return login

# --------
# Ask Login, IGNORE THIS FUNCTION, hardcoded credientials above
# --------
def ask ():
	"""Asks for DB login credentials"""
	sys.stdin.read()
	host = input("What is DB Host? ")
	un = input("What is DB Username? ")
	pw = input("What is DB Password? ")
	database = input("What is Database Name?? ")

	a = [host, un, pw, database]
	login = wcdb2_login(*a)
	print("login successful")
	return login

# ----------
# Pose Query
# ---------- 

def query (login, s) :
	"""Logs into DB and runs provided string as query"""
	assert str(type(login)) == "<type '_mysql.connection'>"
	assert type(s) is str
	login.query(s)
	r = login.use_result()
	if r is None :
		return None
	assert str(type(r)) == "<type '_mysql.result'>"
	t = r.fetch_row(maxrows = 0)
	assert type(t) is tuple
	return t

# ----------
# wcdb2_Read
# ---------- 

def wcdb2_Read (r) :
	"""
	reads an input
	creates an element tree from string
	"""
	read = r.read()
	tree = ET.fromstring(read)
	return tree





def createDB(login):

   query(login, "drop table if exists Crisis;")
   query(login, "drop table if exists Organization;")
   query(login, "drop table if exists Person;")
   query(login, "drop table if exists Location;")
   query(login, "drop table if exists Kind;")
   query(login, "drop table if exists ExternalResources;")
   query(login, "drop table if exists PersonRelation;")
   query(login, "drop table if exists CrisisRelation;")
   query(login, "drop table if exists OrganizationRelation;")
   query(login, "drop table if exists HumanImpact;")
   query(login, "drop table if exists ResourcesNeeded;")
   query(login, "drop table if exists WaysToHelp;")
   
   t = query(
		login,
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
		login,
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
		login,
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
		login,
		"""
	create table Location (
	  parentIdent text,
	  Locality text,
	  Region text,
	  Country text
	  );""")

#insert into Location(parentIdent', 'Locality', 'Region', 'PostalCode', 'Country');
   t = query(
		login,
		"""
	create table Kind (
	  parentIdent text,
	  Type text,
	  Name text,
	  Description text
	  );""")
   
#insert into Kind('parentIdent', 'Type', 'Name', 'Description');
   t = query(
		login,
		"""
	create table ExternalResources (
	  parentIdent text,
	  Type text,
	  Value text
	  );""")

#insert into ExternalResources('parentIdent', 'Type', 'Value');
   t = query(
		login,
		"""
	create table PersonRelation (
	  personIdent text,
	  otherIdent text,
	  Type text
	  );""")


#insert into PersonRelation('personIdent', 'otherIdent', 'Type');
   t = query(
		login,
		"""
	create table CrisisRelation (
	  crisisIdent text,
	  otherIdent text,
	  Type text
	  );""")


#insert into CrisisRelation('crisisIdent', 'otherIdent', 'Type');
   t = query(
		login,
		"""
	create table OrganizationRelation (
	  organizationIdent text,
	  otherIdent text,
	  Type text
	  );""")

#insert into OrganizationRelation('organizationIdent', 'otherIdent', 'Type');
   t = query(
		login,
		"""
	create table HumanImpact (
	  parentIdent text,
	  Type text,
	  Number int
	  );""")

#insert into HumanImpact('parentIdent', 'Type', 'Number');
   t = query(
		login,
		"""
	create table ResourcesNeeded (
	  parentIdent text,
	  ResourceNeeded text
	  );""")

#insert into ResourcesNeeded('parentIdent text', 'ResourcesNeeded');
   t = query(
		login,
		"""
	create table WaysToHelp (
	  parentIdent text,
	  WaysToHelp text
	  );""")

#insert into WaysToHelp('parentIdent', 'WaysToHelp');

   #t = query(login, "show tables;") 
	
   return None

	
def process_crisis (login, tree) :

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
		t = query(login,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		
		#QueryBuilding - HumanImpact Table
		s = (parentkey[i], d.get('Type','Null'), d.get('Number', 'Null'))
		s = 'insert into HumanImpact values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		#QueryBuilding - ResourcesNeeded Table
		s = (parentkey[i], d.get('ResourcesNeeded', 'Null'))
		s = 'insert into ResourcesNeeded values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		#QueryBuilding - WaysToHelp Table
		s = (parentkey[i], d.get('WaysToHelp', 'Null'))
		s = 'insert into WaysToHelp values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into CrisisRelation values' + str(s) + ';'
		t = query(login,s)	
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into CrisisRelation values' + str(s) + ';'
		t = query(login,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(login,s)	
	
	#t = query(login,"select * from ExternalResources;")
	#print(t)




def process_org (login, tree) :

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
		t = query(login,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into OrganizationRelation values' + str(s) + ';'
		t = query(login,s)	
	
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into OrganizationRelation values' + str(s) + ';'
		t = query(login,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(login,s)	
	
	
def process_person (login, tree) :

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
		t = query(login,s)
	
		#QueryBuilding - Location Table
		s = (parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into PersonRelation values' + str(s) + ';'
		t = query(login,s)	
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into PersonRelation values' + str(s) + ';'
		t = query(login,s)	
	
	#QueryBuilding - ExternalResources Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResources values' + str(s) + ';'
		t = query(login,s)	
	
	
	
def process_kind(login, tree) :


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
		t = query(login,s)	
		
		
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
		t = query(login,s)	


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
		t = query(login,s)		
	
	t = query(login,"select * from Kind;")
	
# -------------
# wcdb2_import
# -------------

def wcdb2_import(login, tree):

	"""Takes DB login and Element Tree and processes data and and imports into DB"""

	process_crisis(login, tree)
	process_person(login, tree)
	process_org(login, tree)

	process_kind(login, tree)
	
	return None


# -------------
# wcdb2_export
# -------------

def element_builder(tag, content = ''):
	"""builds 1 xml element with attributes"""
	builder = ET.TreeBuilder()
	
	builder.start(tag, {})
	builder.data(content)
	builder.end(tag)
	
	return builder.close()

def attr_builder(tag, attrs = {}):
	"""builds 1 xml element with content"""
	builder = ET.TreeBuilder()
	builder.start(tag, attrs)
	builder.end(tag)
	
	return builder.close()

def wcdb2_export(login, tree):
	"""Generates ElementTree from DB"""



	root = element_builder('WorldCrises')
	
	crises = query(login, 
	""" select *
	from Crisis;
	""")
	organizations = [1]
	people = [1]
	criseskind = [1]
	organizationkind = [1]
	personkind = [1]
	value = 'test'
	

	
	for crisis in crises:
		#Crisis Element
		crisis_element = attr_builder('Crisis', {'crisisIdent': crisis[0]})
		#Name
		crisis_element.append(element_builder('Name', crisis[1]))
		#Kind
		crisis_element.append(attr_builder('Kind', {'crisisKindIdent': crisis[2]}))
		
		root.append(crisis_element)

	for org in organizations:
		org_element = attr_builder('Organization', {'organizationIdent': value})
		root.append(org_element)
	
	for person in people:
		person_element = attr_builder('Person', {'personIdent': value})
		root.append(person_element)
		
	for crisis in criseskind:
		crisis_element = attr_builder('CrisisKind', {'crisisKindIdent': value})
		root.append(crisis_element)
		
	for org in organizationkind:
		org_element = attr_builder('OrganizationKind', {'organizationKindIdent': value})
		root.append(org_element)
	
	for person in personkind:
		person_element = attr_builder('PersonKind', {'personKindIdent': value})
		root.append(person_element)
		
	print(ET.tostring(root))


	


	return tree
		
# ------------
# wcdb2_write
# ------------

def wcdb2_write (w, tree) :
	"""
	reads an input
	builds an element tree from string
	"""
	tree2 = ET.tostring(tree)
	w.write('<?xml version="1.0" ?>\n' + tree2)
	return tree
		
# -------------
# wcdb2_solve
# -------------

def wcdb2_solve (r, w) :
	"""
	r is a reader
	w is a writer
	Logs into DB, Generates Element Tree, Creates Tables in DB,
	Imports data into DB, exports data from DB
	"""

	login = wcdb2_login(*a)
	tree = wcdb2_Read (r)
	output1 = wcdb2_write (w, tree)
	createDB(login)
	#output2 = wcdb2_write (w, output1)
	wcdb2_import(login, tree)
	wcdb2_export(login, tree)
