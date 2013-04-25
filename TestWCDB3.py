#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB3.py
# Copyright (C) 2013
# Taylor McCaslin
# ---------------------------



# -------
# imports
# -------

import StringIO
import unittest
import sys
from cStringIO import StringIO
import xml.etree.ElementTree as ET
import _mysql
import tempfile
from WCDB3 import *

#Database Creds for Testing
a = ["z","taylor","nVZV4bLhpG","cs327e_taylor"] 
   #[host, un, pw, database]


# -----------
# TestWCDB3
# -----------

class TestWCDB3(unittest.TestCase):
  # -----------
  # Test login
  # -----------

	def test_wcdb3_login1 (self):
		c = _mysql.connect(
			host = "z",
			user = "taylor",
			passwd = "nVZV4bLhpG",
			db = "cs327e_taylor")
		self.assert_(str(type(c)) == "<type '_mysql.connection'>")

	def test_wcdb3_login2 (self) :
		try:
			c = _mysql.connect(
				host = "z",
				user = "OscarMyer",
				passwd = "b0lOgN4",
				db = "cs327e_taylor")
		except:
			c = 'no user exists'
			
		self.assert_(c == 'no user exists')
		
	def test_wcdb3_login3 (self) :
		try:
			c = _mysql.connect(
			host = "z",
			user = "hazard",
			passwd = "AbcdefG",
			db = "cs327e_taylor")
		except:
			c = 'no user exists'
			
		self.assert_(c == 'no user exists')

  #-----------
  # test query
  #-----------

	def test_query1(self):
		login = wcdb3_login(*a)
		t = query(login, "select * from cs327e_taylor")
		self.assert_(str(type(login))) == "<type '_mysql.connection'>"
		self.assert_(type(t)) is list
	
	def test_query2(self):
		login = wcdb3_login(*a)
		t = query(login, "select * from cs327e_taylor")
		self.assert_(str(type(login))) == "<type '_mysql.connection'>"
		self.assert_(type(t)) == None
	
	def test_query3(self):
		login = wcdb3_login(*a)
		t = query(login, "select * from wrongtable")
		self.assert_(str(type(login))) == "<type '_mysql.connection'>"
		self.assert_(type(t)) == None

# -------
# test read 
# -------

	def test_wcdb3_read_1(self):
		file1 = ["Bonsai-WCDB3.xml"]
		tree = wcdb3_Read(file1)
		self.assert_(tree != None)

	def test_wcdb3_read_2(self):
		file2 = ["Bonsai-WCDB3.xml"]
		root = wcdb3_Read(file2)
		cparent = root.findall("Crisis")
		element_list = []
		for element in cparent:
			element_list.append(element.attrib['crisisIdent'])
		self.assert_(element_list != None)

	def test_wcdb3_read_3(self):
		file3 = ["Bonsai-WCDB3.xml"]
		root = wcdb3_Read(file3)
		oparent = root.findall("Organization")
		element_list = []

		for element in oparent:
			element_list.append(element.attrib['organizationIdent'])
		self.assert_(element_list != None)
		self.assert_(type(element_list) is list)

  #-----------
  # test createDB
  #-----------

	def test_createDB1(self):
		h = "localhost"
		u = "admin"
		p = "admin"
		db = "WCDB"
		c = wcdb3_login(*a)
		result = createDB(c)
		t = query(c,'SELECT * from Crisis')
		self.assert_(t == ())

	def test_createDB2(self):
		h = "localhost"
		u = "admin"
		p = "admin"
		db = "WCDB"
		c = wcdb3_login(*a)
		result = createDB(c)
		t = query(c,'SELECT * from Person')
		self.assert_(t == ())

	def test_createDB3(self):
		h = "localhost"
		u = "admin"
		p = "admin"
		db = "WCDB"
		c = wcdb3_login(*a)
		result = createDB(c)
		t = query(c,'SELECT * from Organization')
		self.assert_(t == ())

  # ----------
  # wcdb_merge
  # ----------

	def test_wcdb_merge1 (self):
		tree = wcdb3_Read (["Bonsai-WCDB3.xml"])
		newtree = wcdb3_merge(tree)
		self.assert_(tree.tag == newtree.tag)
	
	def test_wcdb_merge2 (self):
		tree = wcdb3_Read (["Bonsai-WCDB3.xml"])
		newtree = wcdb3_merge(tree)
		tparent = tree.findall("Crisis")
		ntparent = newtree.findall("Crisis")
		i = 0
		for element in tparent:
			if(tparent[i] == ntparent[i]):
				tparent.remove(i)
				ntparent.remove(i)
				i = i + 1
		self.assert_(tparent == [])
	
	
	def test_wcdb_merge3 (self):
		tree = wcdb3_Read (["Bonsai-WCDB3.xml", "Miner-WCDB3.xml"])
		newtree = wcdb3_merge(tree)
		tparent = tree.findall("Crisis")
		ntparent = newtree.findall("Crisis")
		i = 0
		for element in tparent:
			if(tparent[i] == ntparent[i]):
				tparent.remove(i)
				ntparent.remove(i)
				i = i + 1
		self.assert_(ntparent != [])


  #----------
  # test import
  #----------

	def test_wcdb3_import1(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		tree = ET.parse(StringIO("<WorldCrisis></WorldCrisis>"))
		wcdb3_import(c, tree)
		self.assert_(len(query(c, "select * from Crisis;")) == 0)

	def test_wcdb3_import2(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		tree = []
		try:
			tree += ET.parse(StringIO(''))
			wcdb3_import(c, tree)
		except:
			self.assert_(tree == [])

	def test_wcdb3_import3(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		s = '<WorldCrises><Crisis crisisIdent="Syrian_WAR_2011"><Name>Syrian Civil War </Name><Kind crisisKindIdent="WAR"/><Location><Country>Syria </Country></Location><StartDateTime><Date>2011-03-15</Date></StartDateTime><HumanImpact><Type>Death </Type><Number>70000 </Number></HumanImpact><EconomicImpact/><ExternalResources><ImageURL>http://en.wikipedia.org/wiki/File:Bombed_out_vehicles_Aleppo.jpg</ImageURL><VideoURL>http://www.bbc.co.uk/news/world-middle-east-21504390</VideoURL><MapURL>http://goo.gl/maps/PWJKM</MapURL><ExternalLinkURL>http://www.crisisgroup.org/en/regions/middle-east-north-africa/egypt-syria-lebanon-syria.aspx/</ExternalLinkURL></ExternalResources><RelatedPersons><RelatedPerson personIdent="SLavrov"/></RelatedPersons><RelatedOrganizations><RelatedOrganization organizationIdent="NATO"/><RelatedOrganization organizationIdent="AI"/></RelatedOrganizations></Crisis></WorldCrises>'
		tree = ET.parse(StringIO(s))
		wcdb3_import(c, tree)
		t = query(c, "select * from Crisis;")
		self.assert_(len(t) == 1 )

  #---------
  # test export
  #---------

	def test_wcdb3_export1(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		tree = wcdb3_export(c)
		self.assert_(type(a) == list)
		
	def test_wcdb3_export2(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		tree = wcdb3_export(c)
		self.assert_(str(type(tree)) != 'lxml.etree._Element')

	def test_wcdb3_export3(self):
		c = wcdb3_login(*a)
		result = createDB(c)
		tree = wcdb3_export(c)
		self.assert_(tree.tag == 'WorldCrises')

  # -------
  # write
  # -------

	def test_wcdb3_write_1(self):
		w = tempfile.TemporaryFile()
		a = element_builder('a')
		wcdb3_write(w, a)
		self.assert_(w.read() != '<?xml version="1.0" ?>\n<a />')

	def test_wcdb3_write_2(self):
		w = tempfile.TemporaryFile()
		a = ET.Element('a')
		b = ET.SubElement(a, 'b')
		wcdb3_write(w, a)
		self.assert_(w.read() != "<a><b /></a>")

	def test_wcdb3_write_3(self):
		w = tempfile.TemporaryFile()
		a = ET.Element('a')
		a.text = "hello world"
		wcdb3_write(w, a)
		self.assert_(w.read() != "<a>hello world</a>")

  # -------
  # Escape Characters
  # -------
	
	def test_escape_1(self):
		text = "I want to type a single quote like this: \\'"
		x = escapeSpecialCharacters (text)
		y = "I want to type a single quote like this: \\\\'"
		self.assert_(x == y)
		
	def test_escape_2(self):
		text = "I want to type a comma like this: \\,"
		x = escapeSpecialCharacters (text)
		y = "I want to type a comma like this: \\\\,"
		self.assert_(x == y)  

	def test_escape_3(self):
		text = "A string with no escape characters"
		x = escapeSpecialCharacters (text)
		self.assert_(x == text)  

# ----
# main
# ----

print ("TestWCDB3.py")
unittest.main()
print ("Done.")



