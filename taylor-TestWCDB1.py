#!/usr/bin/env python

"""
To test the program:
% TestWCDB1.py >& TestWCDB1.out
"""

# -------
# imports
# -------

import StringIO
import unittest
import xml.etree.ElementTree as ET

from WCDB1 import *

# -----------
# TestWCDB1
# -----------

class TestWCDB1 (unittest.TestCase) :
  # -------
  # read
  # -------
  
  def test_wcdb1_read_1(self):
    r = StringIO.StringIO("<a />")
    root = wcdb1_read(r)
    self.assert_(root.tag == "a")


  def test_wcdb1_read_2(self):
    r = StringIO.StringIO("<a> <b></b> </a>")
    root = wcdb1_read(r)
    self.assert_(root.tag == "a")
    self.assert_(root[0].tag == "b")

  def test_wcdb1_read_3(self):
    r = StringIO.StringIO("<a>hello world</a>")
    root = wcdb1_read(r)
    self.assert_(root.tag == "a")
    self.assert_(root.text == "hello world")

  # -------
  # write
  # -------

  def test_wcdb1_write_1(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    wcdb1_write(a, w)
    self.assert_(w.getvalue() == "<a />")

  def test_wcdb1_write_2(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    wcdb1_write(a, w)
    self.assert_(w.getvalue() == "<a><b /></a>")

  def test_wcdb1_write_3(self):
    w = StringIO.StringIO()
    a = ET.Element('a')
    a.text = "hello world"
    wcdb1_write(a, w)
    self.assert_(w.getvalue() == "<a>hello world</a>")

  # -------
  # solve 
  # -------

  def test_wcdb1_solve(self):
    w1 = StringIO.StringIO()
    w2 = StringIO.StringIO()
    r = StringIO.StringIO("<a><b></b></a>")
    wcdb1_solve(r, w1)
    r2 = StringIO.StringIO(w1.getvalue())
    wcdb1_solve(r2, w2)
    self.assert_(w1.getvalue() == w2.getvalue())

  def test_wcdb1_solve_2(self):
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
    wcdb1_solve(r, w1)
    r2 = StringIO.StringIO(w1.getvalue())
    wcdb1_solve(r2, w2)
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
    wcdb1_solve(r, w1)
    r2 = StringIO.StringIO(w1.getvalue())
    wcdb1_solve(r2, w2)
    self.assert_(w1.getvalue() == w2.getvalue())

# ----
# main
# ----

print "TestWCDB1.py"
unittest.main()
print "Done."
