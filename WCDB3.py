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
#import _mysql
#import lxml.etree as ET

# --------
# DB Login
# --------
	
a = ["z","taylor","nVZV4bLhpG","cs327e_taylor"] 
   #[host, un, pw, database]

def wcdb3_login ( host, un, pw, database ) :
	"""takes credentials and logs into DB"""
	login = _mysql.connect(
			host = host,
			user = un,
			passwd = pw,
			db = database)
	assert str(type(login)) == "<type '_mysql.connection'>"
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
# wcdb3_Read
# ---------- 

def wcdb3_Read (xml_files) :
	"""
	reads an input
	creates an element tree from string
	"""
	
	new_tree = 	element_builder('WorldCrisis')
	cparent = []
	oparent = []
	pparent = []
	ckind = []
	okind = []
	pkind = []
	
	for u in xml_files:
		r = open(u, 'r')
		read = r.read()
		tree = ET.fromstring(read)
		
		cparent += tree.findall("Crisis")
		oparent += tree.findall("Organization")
		pparent += tree.findall("Person")
		ckind += tree.findall("CrisisKind")
		okind += tree.findall("OrganizationKind")
		pkind += tree.findall("PersonKind")
		
		r.close()
		
	#add element idents to list of idents
	for element in cparent:
		new_tree.append(element)
	for element in oparent:
		new_tree.append(element)
	for element in pparent:
		new_tree.append(element)
	for element in ckind:
		new_tree.append(element)
	for element in okind:
		new_tree.append(element)			
	for element in pkind:
		new_tree.append(element)
			
	return new_tree


# ----------
# Creat Database
# ---------- 


def createDB(login):
	"""Create Needed Databases, dropping if needed"""
	query(login, "drop table if exists Crisis;")
	query(login, "drop table if exists Organization;")
	query(login, "drop table if exists Person;")
	query(login, "drop table if exists Location;")
	query(login, "drop table if exists HumanImpact;")
	query(login, "drop table if exists ResourceNeeded;")
	query(login, "drop table if exists WaysToHelp;")
	query(login, "drop table if exists ExternalResource;")
	query(login, "drop table if exists CrisisOrganization;")
	query(login, "drop table if exists OrganizationPerson;")
	query(login, "drop table if exists PersonCrisis;")
	query(login, "drop table if exists CrisisKind;")
	query(login, "drop table if exists OrganizationKind;")
	query(login, "drop table if exists PersonKind;")
	

	
	t = query(
		login,
		"""
	CREATE TABLE Crisis (
	id char(100) NOT NULL
	PRIMARY KEY,
	name text NOT NULL,
	kind char(100) NOT NULL
	REFERENCES CrisisKind(id),
	start_date date NOT NULL,
	start_time time,
	end_date date,
	end_time time,
	economic_impact char(100) NOT NULL
	);""") 
	  
#insert into Crisis values('crisisIdent', 'Name', 'Kind', StartDateTime, EndDateTime, 'EconomicImpact');


	t = query(
		login,
		"""
	CREATE TABLE Organization (
	id char(100) NOT NULL
	PRIMARY KEY,
	name char(100) NOT NULL,
	kind char(100) NOT NULL
	REFERENCES OrganizationKind(id),
	history text NOT NULL,
	telephone char(100) NOT NULL,
	fax char(100) NOT NULL,
	email char(100) NOT NULL,
	street_address char(100) NOT NULL,
	locality char(100) NOT NULL,
	region char(100) NOT NULL,
	postal_code char(100) NOT NULL,
	country char(100) NOT NULL
	);""")
	  
#insert into Organization('organizationIdent', 'Name', 'Kind', 'History','Telephone', 'Fax', 'Email', 'StreetAddress', 'Locality', 'Region', 'PostalCode', 'Country');



	t = query(
		login,
		"""
	CREATE TABLE Person (
	id char(100) NOT NULL
	PRIMARY KEY,
	first_name char(100) NOT NULL,
	middle_name char(100),
	last_name char(100) NOT NULL,
	suffix char(100),
	kind char(100) NOT NULL
	REFERENCES PersonKind(id)
	);""")
	  
#insert into Person('personIdent', 'FirstName', 'MiddleName', 'LastName', 'Suffix', 'Kind');


	t = query(
		login,
		"""
	CREATE TABLE Location (
	id int NOT NULL AUTO_INCREMENT
	PRIMARY KEY,
	entity_type ENUM('C', 'O', 'P') NOT NULL,
	entity_id char(100) NOT NULL,
	locality char(100),
	region char(100),
	country char(100)
	);""")

#insert into Location(parentIdent', 'Locality', 'Region', 'PostalCode', 'Country');



	t = query(
		login,
		"""
	CREATE TABlE HumanImpact (
	id int NOT NULL AUTO_INCREMENT
	PRIMARY KEY,
	crisis_id char(100) NOT NULL
	REFERENCES Crisis(id),
	type char(100) NOT NULL,
	number int NOT NULL
	);""")

#insert into HumanImpact('parentIdent', 'Type', 'Number');
	t = query(
		login,
		"""
	CREATE TABLE ResourceNeeded (
	id int NOT NULL AUTO_INCREMENT
	PRIMARY KEY,
	crisis_id char(100) NOT NULL
	REFERENCES Crisis(id),
	description text
	);""")

#insert into ResourceNeeded('parentIdent text', 'ResourceNeeded');
	t = query(
		login,
		"""
	CREATE TABLE WaysToHelp (
	id int NOT NULL AUTO_INCREMENT
	PRIMARY KEY,
	crisis_id char(100) NOT NULL
	REFERENCES Crisis(id),
	description text
	);""")

#insert into WaysToHelp('parentIdent', 'WaysToHelp');

	#t = query(login, "show tables;") 


		
	t = query(
		login,
		"""
	CREATE TABLE ExternalResource (
	id int NOT NULL AUTO_INCREMENT
	PRIMARY KEY,
	entity_type ENUM('C', 'O', 'P') NOT NULL,
	entity_id char(100) NOT NULL,
	type ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
	link text NOT NULL
	);""")

#insert into ExternalResource('parentIdent', 'Type', 'Value');	
	


	t = query(
		login,
		"""
	CREATE TABlE CrisisOrganization (
	id_crisis char(100) NOT NULL
	REFERENCES Crisis(id),
	id_organization char(100) NOT NULL
	REFERENCES Organization(id),
	PRIMARY KEY (id_crisis, id_organization)
	);""")


#insert into PersonRelation('personIdent', 'otherIdent', 'Type');
	t = query(
		login,
		"""
	CREATE TABLE OrganizationPerson (
	id_organization char(100) NOT NULL
	REFERENCES Organization(id),
	id_person char(100) NOT NULL
	REFERENCES Person(id),
	PRIMARY KEY (id_organization, id_person)
	);""")


#insert into CrisisRelation('crisisIdent', 'otherIdent', 'Type');
	t = query(
		login,
		"""
	CREATE TABLE PersonCrisis (
	id_person char(100) NOT NULL
	REFERENCES Person(id),
	id_crisis char(100) NOT NULL
	REFERENCES Crisis(id),
	PRIMARY KEY (id_person, id_crisis)
	);""")

#insert into OrganizationRelation('organizationIdent', 'otherIdent', 'Type');

	t = query(
		login,
		"""
	CREATE TABLE CrisisKind (
	id char(100) NOT NULL
	PRIMARY KEY,
	name char(100) NOT NULL,
	description text NOT NULL
	);""")
	
	
	t = query(
		login,
		"""
	CREATE TABLE OrganizationKind (
	id char(100) NOT NULL
	PRIMARY KEY,
	name char(100) NOT NULL,
	description text NOT NULL
	);""")
	
	
	
	
	t = query(
		login,
		"""
	CREATE TABLE PersonKind (
	id char(100) NOT NULL
	PRIMARY KEY,
	name char(100) NOT NULL,
	description text NOT NULL
	);""")	
	return None

	
def process_crisis (login, tree) :
	"""Iterate through Crisis XML and import into DB"""

	inserts = []
	parentkey = []
	kind = []
	relatedperson = []
	relatedorg = []
	ExternalResource = []
	StartDateTime = []
	EndDateTime = []
	i=0
	#iterats over Parents	
	for parent in tree.findall('Crisis'):
		insert = {}
		starts = {}
		ends = {}
		
		parentkey.append(parent.get('crisisIdent'))
		
		#Iterates over Children & Subchildren
		for element in parent.iterdescendants():

			if element.tag == 'Kind':
				kind.append(element.get('crisisKindIdent'))
			if element.tag == 'RelatedOrganization':
				relatedorg.append((parentkey[i], element.get('organizationIdent')))
			if element.tag == 'RelatedPerson':
				relatedperson.append((element.get('personIdent'), parentkey[i]))
			if element.tag == 'StartDateTime':
				for child in element:
					starts[child.tag] = child.text
			if element.tag == 'EndDateTime':
				for child in element:
					starts[child.tag] = child.text						
			if element.tag == 'ImageURL':
				ExternalResource.append(('Null', 'C', parentkey[i], 'IMAGE' , element.text))
			if element.tag == 'VideoURL':
				ExternalResource.append(('Null', 'C', parentkey[i], 'VIDEO' , element.text))
			if element.tag == 'MapURL':
				ExternalResource.append(('Null', 'C', parentkey[i], 'MAP' , element.text))
			if element.tag == 'SocialNetworkURL':
				ExternalResource.append(('Null', 'C', parentkey[i], 'SOCIAL_NETWORK' , element.text))
			if element.tag == 'Citation':
				ExternalResource.append(('Null', 'C', parentkey[i], 'CITATION' , element.text))
			if element.tag == 'ExternalLinkURL':
				ExternalResource.append(('Null', 'C', parentkey[i], 'EXTERNAL_LINK' , element.text))
			if element.getchildren() == [] and element.text != None:
				insert[element.tag] = element.text
		
		inserts.append(insert)
		StartDateTime.append(starts)
		EndDateTime.append(ends)
		i += 1
		
		
	#QueryBuilding Loop	
	for i in xrange(0, len(parentkey)):
		
		#QueryBuilding - Crisis Table
		d = inserts[i]	
		s = StartDateTime[i]
		e = EndDateTime[i]		
		
		s = (parentkey[i], d.get('Name'), kind[i], s.get('Date'), s.get('Time', 'Null'), e.get('Date', 'Null'), e.get('Time', 'Null'), d.get('EconomicImpact', 'No Economic Impact Provided'))
		s = 'insert into Crisis values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
	
		#QueryBuilding - Location Table
		s = ( 'Null', 'C', parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		
		#QueryBuilding - HumanImpact Table
		s = ('Null', parentkey[i], d.get('Type','Null'), d.get('Number', 'Null'))
		s = 'insert into HumanImpact values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		#QueryBuilding - ResourceNeeded Table
		s = ('Null', parentkey[i], d.get('ResourceNeeded', 'Null'))
		s = 'insert into ResourceNeeded values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
		#QueryBuilding - WaysToHelp Table
		s = ('Null', parentkey[i], d.get('WaysToHelp', 'Null'))
		s = 'insert into WaysToHelp values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into CrisisOrganization values' + str(s) + ';'
		t = query(login,s)	
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into PersonCrisis values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass	
		
	
	#QueryBuilding - ExternalResource Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		#s.insert(0,'Null')
		s = 'insert into ExternalResource values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass		
	#t = query(login,"select * from ExternalResource;")
	#print(t)




def process_org (login, tree) :
	"""Iterate through Organization XML and import into DB"""

	inserts = []
	parentkey = []
	kind = []
	relatedperson = []
	relatedcrisis = []
	ExternalResource = []
	i = 0
	
	#iterats over Parents	
	for parent in tree.findall('Organization'):
		insert = {}
		
		parentkey.append(parent.get('organizationIdent'))
		
		#Iterates over Children & Subchildren
		for element in parent.iterdescendants():

			if element.tag == 'Kind':
				kind.append(element.get('organizationKindIdent'))
			if element.tag == 'RelatedPerson':
				relatedperson.append((parentkey[i], element.get('personIdent')))
			if element.tag == 'RelatedCrisis':
				relatedcrisis.append((element.get('crisisIdent'), parentkey[i]))
			if element.tag == 'ImageURL':
				ExternalResource.append(('Null', 'O', parentkey[i], 'IMAGE' , element.text))
			if element.tag == 'VideoURL':
				ExternalResource.append(('Null', 'O', parentkey[i], 'VIDEO' , element.text))
			if element.tag == 'MapURL':
				ExternalResource.append(('Null', 'O', parentkey[i], 'MAP' , element.text))
			if element.tag == 'SocialNetworkURL':
				ExternalResource.append(('Null', 'O', parentkey[i], 'SOCIAL_NETWORK' , element.text))
			if element.tag == 'Citation':
				ExternalResource.append(('Null', 'O', parentkey[i], 'CITATION' , element.text))
			if element.tag == 'ExternalLinkURL':
				ExternalResource.append(('Null', 'O', parentkey[i], 'EXTERNAL_LINK' , element.text))
			if element.getchildren() == [] and element.text != None:
				insert[element.tag] = element.text
		
		inserts.append(insert)
		i += 1
		
	#QueryBuilding Loop	
	for i in xrange(0, len(parentkey)):
		
		#QueryBuilding - Organization Table
		d = inserts[i]	
		s = (parentkey[i], d.get('Name','Null'), kind[i], d.get('History', 'Null'), d.get('Telephone', 'Null'), d.get('Fax', 'Null'), d.get('Email', 'Null'),	 d.get('StreetAddress', 'Null'), d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('PostalCode', 'Null'), d.get('Country', 'Null') )
		s = 'insert into Organization values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
	
		#QueryBuilding - Location Table
		s = ('Null', 'O', parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedperson)):
		s = relatedperson[i]
		s = 'insert into OrganizationPerson values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass		
		
	#QueryBuilding - OrganizationRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into CrisisOrganization values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass		
	#QueryBuilding - ExternalResource Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResource values' + str(s) + ';'
		t = query(login,s)	
	
	
def process_person (login, tree) :
	"""Iterate through Person XML and import into DB"""

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
				relatedorg.append((element.get('organizationIdent'), parentkey[i]))
			if element.tag == 'RelatedCrisis':
				relatedcrisis.append((parentkey[i], element.get('crisisIdent')))
			if element.tag == 'ImageURL':
				ExternalResource.append(('Null', 'P', parentkey[i], 'IMAGE' , element.text))
			if element.tag == 'VideoURL':
				ExternalResource.append(('Null', 'P', parentkey[i], 'VIDEO' , element.text))
			if element.tag == 'MapURL':
				ExternalResource.append(('Null', 'P', parentkey[i], 'MAP' , element.text))
			if element.tag == 'SocialNetworkURL':
				ExternalResource.append(('Null', 'P', parentkey[i], 'SOCIAL_NETWORK' , element.text))
			if element.tag == 'Citation':
				ExternalResource.append(('Null', 'P', parentkey[i], 'CITATION' , element.text))
			if element.tag == 'ExternalLinkURL':
				ExternalResource.append(('Null', 'P', parentkey[i], 'EXTERNAL_LINK' , element.text))
			if element.getchildren() == [] and element.text != None:
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
		s = ( 'Null', 'P', parentkey[i], d.get('Locality', 'Null'), d.get('Region', 'Null'), d.get('Country', 'Null'))
		s = 'insert into Location values' + str(s) + ';'
		s = s.replace('None', 'Null')
		t = query(login,s)
		
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedorg)):
		s = relatedorg[i]
		s = 'insert into OrganizationPerson values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass			
	#QueryBuilding - CrisisRelation Table

	for i in xrange(0, len(relatedcrisis)):
		s = relatedcrisis[i]
		s = 'insert into PersonCrisis values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass	
				
	#QueryBuilding - ExternalResource Table		
	for i in xrange(0, len(ExternalResource)):
		s = ExternalResource[i]
		s = 'insert into ExternalResource values' + str(s) + ';'
		t = query(login,s)	
	
	
	
def process_kind(login, tree) :
	"""Iterate through Kind XML and import into DB"""

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
		s = (parentkey[i], d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into CrisisKind values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass			
		
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
		s = (parentkey[i], d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into OrganizationKind values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass	

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
		s = (parentkey[i], d.get('Name', 'Null'), d.get('Description', 'Null'))
		s = 'insert into PersonKind values' + str(s) + ';'
		try:
			t = query(login,s)
		except:
			pass		
	
# -------------
# wcdb3_import
# -------------

def wcdb3_import(login, tree):

	"""Takes DB login and Element Tree and processes data and and imports into DB"""

	process_crisis(login, tree)
	process_person(login, tree)
	process_org(login, tree)

	process_kind(login, tree)
	
	return None


# -------------
# wcdb3_export
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

def wcdb3_export(login):
	"""Generates ElementTree from DB"""

	root = element_builder('WorldCrises')
	
	crises = query(login, 
	""" select *
	from Crisis;
	""")
	organizations = query(login, 
	""" select *
	from Organization;
	""")
	people = query(login, 
	""" select *
	from Person;
	""")
	
	crisiskind = query(login, 
	""" select *
	from CrisisKind;
	""")
	organizationkind = query(login, 
	""" select *
	from OrganizationKind;
	""")
	personkind = query(login, 
	""" select *
	from PersonKind;
	""")
	
# -------------
# Crisis Export
# -------------
	
	for crisis in crises:
		#Crisis Element
		crisis_element = attr_builder('Crisis', {'crisisIdent': crisis[0]})
		#Name
		crisis_element.append(element_builder('Name', crisis[1]))
		#Kind
		crisis_element.append(attr_builder('Kind', {'crisisKindIdent': crisis[2]}))
		
		#Location
		s = 'select * from Location where Location.entity_id = "' + str(crisis[0]) + '";'
		locationlist = query(login, s)
		locationlist = locationlist[0]
		location = element_builder('Location')
			
		#Locality
		if locationlist[3] not in ['Null',None]:
			location.append(element_builder('Locality',locationlist[3]))
		#Region
		if locationlist[4] not in ['Null',None]:
			location.append(element_builder('Region',locationlist[4]))
		#Country
		if locationlist[5] not in ['Null',None]:
			location.append(element_builder('Country',locationlist[5]))
		
		crisis_element.append(location)	
		
		#StateDateTime
		datetime = element_builder('StartDateTime')

		if crisis[3] != '0000-00-00':
			datetime.append(element_builder('Date', crisis[3]))
			
		if crisis[4] != '00:00:00':
			datetime.append(element_builder('Time', crisis[4]))
		
		crisis_element.append(datetime)	

		#EndDateTime
		datetime = element_builder('EndDateTime')
		
		if crisis[5] != '0000-00-00':
			datetime.append(element_builder('Date', crisis[5]))
			
		if crisis[6] != '00:00:00':
			datetime.append(element_builder('Time', crisis[6]))
			
		if len(datetime) >= 1:		
			crisis_element.append(datetime)	

		#HumanImpact
		s = 'select * from HumanImpact where HumanImpact.crisis_id = "' + str(crisis[0]) + '";'
		humanimpactlist = query(login, s)
		humanimpactlist = humanimpactlist[0]
		humanimpact = element_builder('HumanImpact')		

		#Type
		
		if humanimpactlist[1] != 'Null':
			humanimpact.append(element_builder('Type', humanimpactlist[2]))	
			humanimpact.append(element_builder('Number', humanimpactlist[3]))	
		
		crisis_element.append(humanimpact)	
		
		#EconomicImpact
		if crisis[7]:		
			crisis_element.append(element_builder('EconomicImpact', crisis[7]))
		
		
		#ExternalResource
		s = 'select * from ExternalResource where ExternalResource.entity_id = "' + str(crisis[0]) + '";'
		external = query(login, s)

		external_element = element_builder('ExternalResource')
		i = 0
		
		for x in xrange(0, len(external)):
			#Image
			if external[i][3] == 'IMAGE':
				external_element.append(element_builder('ImageURL',external[i][4]))
			#Video
			elif external[i][3] == 'VIDEO':
				external_element.append(element_builder('VideoURL',external[i][4]))
			#Map
			elif external[i][3] == 'MAP':
				external_element.append(element_builder('MapURL',external[i][4]))
			#Social
			elif external[i][3] == 'SOCIAL_NETWORK':
				external_element.append(element_builder('SocialURL',external[i][4]))
			
			#Citation
			elif external[i][3] == 'CITATION':
				external_element.append(element_builder('CitationURL',external[i][4]))		
			#ExternalLink
			elif external[i][3] == 'EXTERNAL_LINK':
				external_element.append(element_builder('ExternalURL',external[i][4]))	
			i += 1
		
		crisis_element.append(external_element)	


		#RelatedPersons
		s = 'select * from PersonCrisis where PersonCrisis.id_crisis = "' + str(crisis[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedPersons')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedPerson',{'personIdent':related[j][0]}))	
			j += 1
				
		crisis_element.append(related_element)	
		
		#RelatedOrgs
		s = 'select * from CrisisOrganization where CrisisOrganization.id_crisis = "' + str(crisis[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedOrganizations')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedOrganization',{'organizationIdent':related[j][1]}))	
			j += 1
				
		crisis_element.append(related_element)		

		root.append(crisis_element)

# -------------
# Organizations Export
# -------------

	for organization in organizations:

		#Organization Element
		org_element = attr_builder('Organization', {'OrganizationIdent': organization[0]})
		
		#Name
		org_element.append(element_builder('Name', organization[1]))
		
		#Kind
		org_element.append(attr_builder('Kind', {'organizationKindIdent': organization[2]}))
		
		#Location		
		s = 'select * from Location where Location.entity_id = "' + str(organization[0]) + '";'		
		locationlist = query(login, s)
		locationlist = locationlist[0]
		location = element_builder('Location')
			
		#Locality
		if locationlist[3] not in ['Null',None]:
			location.append(element_builder('Locality',locationlist[3]))
		#Region
		if locationlist[4] not in ['Null',None]:
			location.append(element_builder('Region',locationlist[4]))
		#Country
		if locationlist[5] not in ['Null',None]:
			location.append(element_builder('Country',locationlist[5]))
		
		org_element.append(location)	
		
		#History
		if organization[6]:
			org_element.append(element_builder('History', organization[3]))


		#ContactInfo
		contact = element_builder('ContactInfo')
		postal = element_builder('PostalAddress')
	
		#Telephone
		if organization[4]:
			contact.append(element_builder('Telephone',organization[4]))

		#Fax
		if organization[5]:
			contact.append(element_builder('Fax',organization[5]))

		#Email
		if organization[6]:
			contact.append(element_builder('Email',organization[6]))

		#Street Address
		if organization[7]:
			postal.append(element_builder('StreetAddress',organization[7]))
		
		#Locality
		if organization[8]:
			postal.append(element_builder('Locality',organization[8]))

		#Region
		if organization[9]:
			postal.append(element_builder('Region',organization[9]))
			
		#PostalCode
		if organization[10]:
			postal.append(element_builder('PostalCode',organization[10]))
			
		#Country
		if organization[11]:
			postal.append(element_builder('Country',organization[11]))

		org_element.append(contact)	
		org_element.append(postal)	


		#ExternalResource
		s = 'select * from ExternalResource where ExternalResource.entity_id = "' + str(organization[0]) + '";'
		external = query(login, s)

		external_element = element_builder('ExternalResource')
		i = 0
		
		for x in xrange(0, len(external)):
			#Image
			if external[i][3] == 'IMAGE':
				external_element.append(element_builder('ImageURL',external[i][4]))
			#Video
			elif external[i][3] == 'VIDEO':
				external_element.append(element_builder('VideoURL',external[i][4]))
			#Map
			elif external[i][3] == 'MAP':
				external_element.append(element_builder('MapURL',external[i][4]))
			#Social
			elif external[i][3] == 'SOCIAL_NETWORK':
				external_element.append(element_builder('SocialURL',external[i][4]))
			
			#Citation
			elif external[i][3] == 'CITATION':
				external_element.append(element_builder('CitationURL',external[i][4]))		
			#ExternalLink
			elif external[i][3] == 'EXTERNAL_LINK':
				external_element.append(element_builder('ExternalURL',external[i][4]))	
			i += 1
		
		org_element.append(external_element)	



		#RelatedCrisis
		s = 'select * from CrisisOrganization where CrisisOrganization.id_organization = "' + str(organization[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedCrises')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedCrisis',{'crisisIdent':related[j][0]}))	
			j += 1
				
		org_element.append(related_element)	


		#RelatedPersons
		s = 'select * from OrganizationPerson where OrganizationPerson.id_organization = "' + str(organization[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedPersons')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedPerson',{'personIdent':related[j][1]}))	
			j += 1
				
		org_element.append(related_element)	

		root.append(org_element)		

# -------------
# Person Export
# -------------

	for person in people:
		person_element = attr_builder('Person', {'personIdent': person[0]})

		
		#Name
		name = element_builder('Name')
		
		#First
		if person[1]:
			name.append(element_builder('FirstName',person[1]))

		#Middle
		if person[2]:
			name.append(element_builder('MiddleName',person[2]))

		#Last
		if person[3]:
			name.append(element_builder('LastName',person[3]))

		#Suffix
		if person[4]:
			name.append(element_builder('Suffix',person[4]))
			
		person_element.append(name)
		
		#Kind
		person_element.append(attr_builder('Kind', {'organizationKindIdent': person[5]}))
		
		#Location		
		s = 'select * from Location where Location.entity_id = "' + str(person[0]) + '";'		
		locationlist = query(login, s)
		locationlist = locationlist[0]
		location = element_builder('Location')
			
		#Locality
		if locationlist[3] != 'Null':
			location.append(element_builder('Locality',locationlist[3]))
		#Region
		if locationlist[4]:
			location.append(element_builder('Region',locationlist[4]))
		#Country
		if locationlist[5] != 'Null':
			location.append(element_builder('Country',locationlist[5]))
		
		person_element.append(location)	
		


		#ExternalResource
		s = 'select * from ExternalResource where ExternalResource.entity_id = "' + str(person[0]) + '";'
		external = query(login, s)

		external_element = element_builder('ExternalResource')
		i = 0
		
		for x in xrange(0, len(external)):
			#Image
			if external[i][3] == 'IMAGE':
				external_element.append(element_builder('ImageURL',external[i][4]))
			#Video
			elif external[i][3] == 'VIDEO':
				external_element.append(element_builder('VideoURL',external[i][4]))
			#Map
			elif external[i][3] == 'MAP':
				external_element.append(element_builder('MapURL',external[i][4]))
			#Social
			elif external[i][3] == 'SOCIAL_NETWORK':
				external_element.append(element_builder('SocialURL',external[i][4]))
			
			#Citation
			elif external[i][3] == 'CITATION':
				external_element.append(element_builder('CitationURL',external[i][4]))		
			#ExternalLink
			elif external[i][3] == 'EXTERNAL_LINK':
				external_element.append(element_builder('ExternalURL',external[i][4]))	
			i += 1

		person_element.append(external_element)	


		#RelatedCrisis
		s = 'select * from PersonCrisis where PersonCrisis.id_person = "' + str(person[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedCrises')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedCrisis',{'crisisIdent':related[j][1]}))
			j += 1
				
		person_element.append(related_element)	


		#RelatedOrgs
		s = 'select * from OrganizationPerson where OrganizationPerson.id_person = "' + str(person[0]) + '";'
		related = query(login, s)
		related_element = element_builder('RelatedOrganizations')
		
		j = 0
		for i in related:
			related_element.append(attr_builder('RelatedOrganization',{'organizationIdent':related[j][0]}))	
			j += 1
				
		person_element.append(related_element)	

		root.append(person_element)
		
		
	# -------------
	# Kind Export
	# -------------
	i = 0
	j = 0
	k = 0
	
	for crisis in crisiskind:
	
		crisis_element = attr_builder('CrisisKind', {'crisisKindIdent': str(crisiskind[i][0])})
		
		#Name
		crisis_element.append(element_builder('Name',crisiskind[i][1]))
		
		#Description
		crisis_element.append(element_builder('Description',crisiskind[i][2]))
		i+=1


		root.append(crisis_element)

		
	for org in organizationkind:
		org_element = attr_builder('OrganizationKind', {'organizationKindIdent': str(organizationkind[j][0])})
		
		#Name
		org_element.append(element_builder('Name',organizationkind[j][1]))
		
		#Description
		org_element.append(element_builder('Description',organizationkind[j][2]))
		j+=1
		
		root.append(org_element)


	for person in personkind:
		person_element = attr_builder('PersonKind', {'personKindIdent': str(personkind[k][0])})
		
		#Name
		person_element.append(element_builder('Name',personkind[k][1]))
		
		#Description
		person_element.append(element_builder('Description',personkind[k][2]))
		k+=1
		
		root.append(person_element)
	

	return root
	

# ------------
# wcdb3_merge
# -----------

def wcdb3_merge(tree):
	"""tree is ElementTree,
		contains duplicate nodes
		"""
	#Create a new Root
	new_root = element_builder('WorldCrises')


	#Build lists of elemets		
	cparent = tree.findall("Crisis")
	oparent = tree.findall("Organization")
	pparent = tree.findall("Person")
	ckind = tree.findall("CrisisKind")
	okind = tree.findall("OrganizationKind")
	pkind = tree.findall("PersonKind")

	#Create list holder for idents
	element_list = []
	kind_list = []
	
	for element in cparent:
		x = element.attrib['crisisIdent']
		element_list.append(x)
	for element in oparent:
		x = element.attrib['organizationIdent']
		element_list.append(x)
	for element in pparent:
		x = element.attrib['personIdent']
		element_list.append(x)
		
	for element in ckind:
		x = element.attrib['crisisKindIdent']
		kind_list.append(x)
	for element in okind:
		x = element.attrib['organizationKindIdent']
		kind_list.append(x)
	for element in pkind:
		x = element.attrib['personKindIdent']
		kind_list.append(x)
		
	#Turn list into set to remove duplicates	
	element_list = set(element_list)
	kind_list = set(kind_list)
	assert type(element_list) == set
	assert type(kind_list) == set

	#Turn set back into list for iteration
	element_list = list(element_list)
	kind_list = list(kind_list)
	assert type(element_list) == list
	assert type(kind_list) == list
	
	#Iterate Again Pushing to New Root
	for element in cparent:
		#get the ident
		x = element.attrib['crisisIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in element_list):
			new_root.append(element)
			element_list.remove(x)
			
	for element in oparent:
		#get the ident
		x = element.attrib['organizationIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in element_list):
			new_root.append(element)
			element_list.remove(x)
			
	for element in pparent:
		#get the ident
		x = element.attrib['personIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in element_list):
			new_root.append(element)
			element_list.remove(x)

	for element in ckind:
		#get the ident
		x = element.attrib['crisisKindIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in kind_list):
			new_root.append(element)
			kind_list.remove(x)
			
	for element in okind:
		#get the ident
		x = element.attrib['organizationKindIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in kind_list):
			new_root.append(element)
			kind_list.remove(x)
			
	for element in pkind:
		#get the ident
		x = element.attrib['personKindIdent']
		#if ident in unique list, append to new root, remove ident from list to prevent duplication
		if(x in kind_list):
			new_root.append(element)
			kind_list.remove(x)
	
	
	
	#pass back the merged tree
	print(ET.dump(new_root))
	return new_root
			
		
# ------------
# wcdb3_write
# ------------

def wcdb3_write (w, tree) :
	"""
	reads an input
	builds an element tree from string
	"""
	#push tree from ET to a string
	tree = ET.tostring(tree)
	#re-input from string (needed for pretty print)
	tree = ET.fromstring(tree)
	tree2 = ET.tostring(tree, pretty_print=True)

	w.write('<?xml version="1.0" ?>\n' + tree2)
	return tree
		
# -------------
# wcdb3_solve
# -------------

def wcdb3_solve (xml_files, w) :
	"""
	xml_files is a list of XML files to be imported
	w is a writer
	Logs into DB, Generates Element Tree, Creates Tables in DB,
	Imports data into DB, exports data from DB
	"""

	login = wcdb3_login(*a)
	tree = wcdb3_Read (xml_files)
	unique_tree = wcdb3_merge(tree)
	wcdb3_write (w, unique_tree)
	createDB(login)
	wcdb3_import(login, unique_tree)
	export = wcdb3_export(login)
	#wcdb3_write (w, export)
	wcdb3_write (w, unique_tree)

