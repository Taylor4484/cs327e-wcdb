#!/usr/bin/env python

# ---------------------------
# projects/WCDB1/WCDB3.py
# Copyright (C) 2013
# Taylor McCaslin
# ---------------------------


"""
To test the program:
% TestWCDB3.py >& TestWCDB3.out
"""

# -------
# imports
# -------

import StringIO
import unittest
import sys
from cStringIO import StringIO
import xml.etree.ElementTree as ET
import _mysql

from WCDB3 import *

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
          user = "Us3r",
          passwd = "BaNaNa",
          db = "cs327e_taylor")
  self.assert_(str(type(c)) == "<type '_mysql.connection'>")

  def test_wcdb3_login2 (self) :
        c = _mysql.connect(
          host = "z",
          user = "OscarMyer",
          passwd = "b0lOgN4",
          db = "cs327e_taylor")
        self.assert_(str(type(c)) != "<type '_mysql.connection'>")
        
  def test_wcdb3_login3 (self) :
        c = _mysql.connect(
          host = "z",
          user = "hazard",
          passwd = "AbcdefG",
          db = "cs327e_taylor")
        self.assert_(str(type(c)) != "<type '_mysql.connection'>")

  #-----------
  # test query
  #-----------

  def test_query1(c, s):
    login = "<type '_mysql.connection'>"
    s = "select * from cs327e_taylor"
    r = login.use_result()
    self.assert_(str(type(login))) == "<type '_mysql.connection'>"
    self.assert_(type(s)) is str
    self.assert_(r) != None
    
  def test_query2(c, s):
      login = "<type '_mysql.connection'>"
      s = ""
      r = None
      self.assert_(str(type(login))) == "<type '_mysql.connection'>"
      self.assert_(type(s)) == ""
      self.assert_(r) == None
    
  def test_query3(c, s):
      login = "<type '_mysql.connection'>"
      s = "select * from wrongtable"
      r = login.use_result()
      self.assert_(str(type(login))) == "<type '_mysql.connection'>"
      self.assert_(type(s)) == "select * from wrongtable"
      self.assert_(r) != None

# -------
# test read 
# -------

  def test_wcdb3_read_1(self):
      file1 = ["Bonsai.xml"]
      root = element_builder("WorldCrises")
      tree = wcdb3_Read(file1)
      self.assert_(tree.getroot() == root)

  def test_wcdb3_read_2(self):
      file2 = ["Bonsai.xml"]
      root = wcdb3_Read(file2)
      cparent = tree.findall("Crisis")
      for element in cparent:
          element_list.append(element.attrib['crisisIdent'])
      assert element_list == ['HU_Katrina_2005', 'WB', 'Cuba_WP_1962', 'Africare', 'HT_0001', 'WBG', 'USCG', 'AHitler', 'Mexico_Drug_WAR_2006', 'WHO', 'NATO', 'HTAP', 'Eyjafjallajokull_VO_2010', 'MHuckabee', 'FCastro', 'AI', 'DWB', 'Bono', 'Africa_DI_1970', 'BHObama', 'JFKennedy', 'MG', 'GWBush', 'NMandela', 'BHGates', 'Egypt_WAR_2011', 'ARC', 'SLavrov', 'Syrian_WAR_2011', 'Holocaust_GC_1933', 'Vietnam_WAR_1955']

  def test_wcdb3_read_3(self):
      file3 = ["Bonsai.xml"]
      root = wcdb3_Read(file3)
      for element in cparent:
          x = element.attrib['crisisIdent']
          if (x == "Surian_WAR_2011"):
              assert type(x) == str 

  #-----------
  # test createDB
  #-----------

  def test_createDB1(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    curs=c.cursor()
    curs.execute('SELECT * from Crisis')
    self.assert_(curs.fetchone() == None)

  def test_createDB2(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    curs=c.cursor()
    curs.execute('SELECT * from Person')   
    self.assert_(curs.fetchone() == None)

  def test_createDB3(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    curs=c.cursor()
    curs.execute('SELECT * from Organization')
    self.assert_(curs.fetchone() == None)

  # ----------
  # wcdb_merge
  # ----------

  def test_wcdb_merge1 (self):
    tree = wcdb3_Read (["Bonsai.xml"])
    newtree = wcdb3_merge(tree)
    assert tree.getroot().tag == newtree.getroot().tag
    
  def test_wcdb_merge2 (self):
    tree = wcdb3_Read (["Bonsai.xml"])
    newtree = wcdb3_merge(tree)
    tparent = tree.finall("Crisis")
    ntparent = newtree.findall("Crisis")
    i = 0
    for element in tparent):
      if(tparent[i] == ntparent[i]):
        tparent.remove(i)
        ntparent.remove(i)
        i = i + 1
    assert  tparent== []
    assert ntparent == []
    
    
  def test_wcdb_merge3 (self):
    tree = wcdb3_Read (["Bonsai.xml", "Miner.xml"])
    newtree = wcdb3_merge(tree)
    tparent = tree.finall("Crisis")
    ntparent = newtree.findall("Crisis")
    i = 0
    for element in tparent):
      if(tparent[i] == ntparent[i]):
        tparent.remove(i)
        ntparent.remove(i)
        i = i + 1
    assert  tparent== []
    assert ntparent != []


  #----------
  # test import
  #----------

  def test_wcdb3_import1(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    tree = ET.parse(StringIO("<WorldCrisis></WorldCrisis"))
    wcdb3_import(login, tree)
    self.assert_(len(query(c, "select * from Crisis;")) == 0)

  def test_wcdb3_import2(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    s = "<WorldCrisis><Crisis crisisIdent= "+"SY2011"+" ><Name>Syrian Civil War </Name><Kind crisisKindIdent= "+"WAR"+" /><Location><Country>Syria </Country></Location><StartDateTime><Date>2011-03-15</Date></StartDateTime><HumanImpact><Type>Death </Type><Number>70000 </Number></HumanImpact><EconomicImpact></EconomicImpact><ExternalResources><ImageURL> http://inapcache.boston.com/universal/site_graphics/blogs/bigpicture/syria_nov_2012/bp11.jpg </ImageURL><ImageURL> http://en.wikipedia.org/wiki/File:Bombed_out_vehicles_Aleppo.jpg </ImageURL><VideoURL>http://www.bbc.co.uk/news/world-middle-east-21504390</VideoURL><MapURL>http://goo.gl/maps/PWJKM</MapURL><SocialNetworkURL>https://www.facebook.com/SyrianDayOfRage</SocialNetworkURL><ExternalLinkURL>http://www.crisisgroup.org</ExternalLinkURL></ExternalResources><RelatedPersons><RelatedPerson personIdent = "+"SLavrov"+"/></RelatedPersons><RelatedOrganizations><RelatedOrganization organizationIdent = "+"NATO"+"/><RelatedOrganization organizationIdent = "+"AI"+" /></RelatedOrganizations></Crisis><CrisisKind crisisKindIdent="+"WAR"+"><Name>War</Name><Description>An organized and often prolonged conflict that is carried out by states and/or non-state actors.</Description></CrisisKind></WorldCrisis"
    tree = ET.parse(s)
    wcdb3_import(login, tree)
    self.assert_(len(query(c, "select * from Crisis;")) == 1)

  def test_wcdb3_import3(self):
    h = "localhost"
    u = "admin"
    p = "admin"
    db = "WCDB"
    c = login(h, u, p, db)
    result = createDB(c)
    s = "<WorldCrisis><Crisis crisisIdent= "+"SY2011"+" ><Name>Syrian Civil War </Name><Kind crisisKindIdent= "+"WAR"+" /><Location><Country>Syria </Country></Location><StartDateTime><Date>2011-03-15</Date></StartDateTime><HumanImpact><Type>Death </Type><Number>70000 </Number></HumanImpact><EconomicImpact></EconomicImpact><ExternalResources><ImageURL> http://inapcache.boston.com/universal/site_graphics/blogs/bigpicture/syria_nov_2012/bp11.jpg </ImageURL><ImageURL> http://en.wikipedia.org/wiki/File:Bombed_out_vehicles_Aleppo.jpg </ImageURL><VideoURL>http://www.bbc.co.uk/news/world-middle-east-21504390</VideoURL><MapURL>http://goo.gl/maps/PWJKM</MapURL><SocialNetworkURL>https://www.facebook.com/SyrianDayOfRage</SocialNetworkURL><ExternalLinkURL>http://www.crisisgroup.org</ExternalLinkURL></ExternalResources><RelatedPersons><RelatedPerson personIdent = "+"SLavrov"+"/></RelatedPersons><RelatedOrganizations><RelatedOrganization organizationIdent = "+"NATO"+"/><RelatedOrganization organizationIdent = "+"AI"+" /></RelatedOrganizations></Crisis><CrisisKind crisisKindIdent="+"WAR"+"><Name>War</Name><Description>An organized and often prolonged conflict that is carried out by states and/or non-state actors.</Description></CrisisKind></WorldCrisis"
    tree = ET.parse(s)
    wcdb3_import(login, tree)
    self.assert_(len(query(c, "select * from CrisisRelation;")) == 3)

  #---------
  # test export
  #---------

  def test_wcdb3_export1(self):
    c = _mysql.connect(
      host = "z",
      user = "Us3r",
      passwd = "BaNaNa",
      db = "cs327e_taylor")
    result = createDB(c)
    tree = WCDB3_export(c)
    self.assert_(str(type(a))=="<class 'xml.etree.ElementTree.Element'>")
        
  def test_wcdb3_export2(self):
    c = _mysql.connect(
      host = "z",
      user = "Us3r",
      passwd = "BaNaNa",
      db = "cs327e_taylor")
    result = createDB(c)
    tree = WCDB3_export(c)
    self.assert_(str(type(tree)) == type(lxml.etree._Element))

  def test_wcdb3_export3(self):
    c = _mysql.connect(
      host = "z",
      user = "Us3r",
      passwd = "BaNaNa",
      db = "cs327e_taylor")
    result = createDB(c)
    tree = WCDB3_export(c)
    self.assert_(len(ET.getroot(tree)) > 0 )

  # -------
  # write
  # -------

  def test_wcdb3_write_1(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    wcdb1_write(w, a)
    self.assert_(w.getvalue() == "<a />")

  def test_wcdb3_write_2(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    wcdb1_write(w, a)
    self.assert_(w.getvalue() == "<a><b /></a>")

  def test_wcdb3_write_3(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    a.text = "hello world"
    wcdb1_write(w, a)
    self.assert_(w.getvalue() == "<a>hello world</a>")

  # -------
  # solve 
  # -------

  def test_wcdb3_solve(self):
    w1 = StringIO.StringIO()
    r = StringIO.StringIO("<WorldCrisis><Crisis crisisIdent= "+"SY2011"+" ><Name>Syrian Civil War </Name><Kind crisisKindIdent= "+"WAR"+" /><Location><Country>Syria </Country></Location><StartDateTime><Date>2011-03-15</Date></StartDateTime><HumanImpact><Type>Death </Type><Number>70000 </Number></HumanImpact><EconomicImpact></EconomicImpact><ExternalResources><ImageURL> http://inapcache.boston.com/universal/site_graphics/blogs/bigpicture/syria_nov_2012/bp11.jpg </ImageURL><ImageURL> http://en.wikipedia.org/wiki/File:Bombed_out_vehicles_Aleppo.jpg </ImageURL><VideoURL>http://www.bbc.co.uk/news/world-middle-east-21504390</VideoURL><MapURL>http://goo.gl/maps/PWJKM</MapURL><SocialNetworkURL>https://www.facebook.com/SyrianDayOfRage</SocialNetworkURL><ExternalLinkURL>http://www.crisisgroup.org</ExternalLinkURL></ExternalResources><RelatedPersons><RelatedPerson personIdent = "+"SLavrov"+"/></RelatedPersons><RelatedOrganizations><RelatedOrganization organizationIdent = "+"NATO"+"/><RelatedOrganization organizationIdent = "+"AI"+" /></RelatedOrganizations></Crisis><CrisisKind crisisKindIdent="+"WAR"+"><Name>War</Name><Description>An organized and often prolonged conflict that is carried out by states and/or non-state actors.</Description></CrisisKind></WorldCrisis")
    wcdb3_solve(r, w1)
    self.assert_(w1.getvalue() == w2.getvalue())

  def test_wcdb3_solve_2(self):
    w1 = StringIO.StringIO()
    w2 = StringIO.StringIO()
    r = StringIO.StringIO("""
    <Bookstore>
      <Book ISBN="ISBN-0-13-713526-2" Price="100">
        <Title>A First Course in Database Systems</Title>
        <Authors>
          <Auth authIdent="JU" />
          <Auth authIdent="JW" />
        </Authors>
      </Book>
      <Book ISBN="ISBN-0-13-815504-6" Price="85">
        <Title>Database Systems: The Complete Book</Title>
        <Authors>
          <Auth authIdent="HG" />
          <Auth authIdent="JU" />
          <Auth authIdent="JW" />
        </Authors>
        <Remark>
          Amazon.com says: Buy this book bundled with
          <BookRef book="ISBN-0-13-713526-2" /> - a great deal!
        </Remark>
      </Book>
      <Author Ident="HG">
        <First_Name>Hector</First_Name>
        <Last_Name>Garcia-Molina</Last_Name>
      </Author>
      <Author Ident="JU">
        <First_Name>Jeffrey</First_Name>
        <Last_Name>Ullman</Last_Name>
      </Author>
      <Author Ident="JW">
        <First_Name>Jennifer</First_Name>
        <Last_Name>Widom</Last_Name>
      </Author>
    </Bookstore>
    """)
    wcdb3_solve(r, w1)
    r2 = StringIO.StringIO(w1.getvalue())
    wcdb3_solve(r2, w2)
    self.assert_(w1.getvalue() == w2.getvalue())

  def test_wcdb1_solve_3(self):
    w1 = StringIO.StringIO()
    w2 = StringIO.StringIO()
    r = StringIO.StringIO("""
    <Bookstore>
      <Book ISBN="ISBN-0-13-713526-2" Price="100" Authors="JU JW">
        <Title>A First Course in Database Systems</Title>
      </Book>
      <Book ISBN="ISBN-0-13-815504-6" Price="85" Authors="HG JU JW">
        <Title>Database Systems: The Complete Book</Title>
        <Remark>
          Amazon.com says: Buy this book bundled with
          <BookRef book="ISBN-0-13-713526-2" /> - a great deal!
        </Remark>
      </Book>
      <Author Ident="HG">
        <First_Name>Hector</First_Name>
        <Last_Name>Garcia-Molina</Last_Name>
      </Author>
      <Author Ident="JU">
        <First_Name>Jeffrey</First_Name>
        <Last_Name>Ullman</Last_Name>
      </Author>
      <Author Ident="JW">
        <First_Name>Jennifer</First_Name>
        <Last_Name>Widom</Last_Name>
      </Author>
    </Bookstore>
    """)
    wcdb3_solve(r, w1)
    r2 = StringIO.StringIO(w1.getvalue())
    wcdb3_solve(r2, w2)
    self.assert_(w1.getvalue() == w2.getvalue())


# ----
# main
# ----

print "TestWCDB3.py"
unittest.main()
print "Done."



