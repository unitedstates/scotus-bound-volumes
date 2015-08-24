#!/usr/bin/env python

import re
from PyPDF2 import PdfFileReader

class Opinion:

  def __init__(self, filename):
    self.fname = filename
    self.pdf = PdfFileReader(filename)
    self.opinion = self.getPages()
    self.parse = self.Parser(str(self))

  def getPages(self):
    self.opinion = []
    for page in self.pdf.pages:
      self.opinion.append(page.getContents().getData().decode(encoding="utf-8",errors="strict"))
    return self.opinion

  def splitMCIDs(self):
    pattern = "<</MCID \d+ >>"
    self.MCIDs = re.compile(pattern).split(str(self))
    return self.MCIDs

  class Parser:
    
    def __init__(self, opinion):
      self.opinion = opinion
      self.parseArray = self.splitMCIDs()
      self.parseArray = self.removeBDC()
'''
# Break Point

At this point, you have an array (self.parseArray) which needs to be interpreted. To do this, we'll create an arrray of objects with the following key-value pairs:

text
text_size

After that, we'll come back and clean up the text to deal with the character conversions.
'''


    def splitMCIDs(self):
      pattern = "<</MCID \d+ >>"
      self.MCIDs = re.compile(pattern).split(self.opinion)
      return self.MCIDs

    # This gets you to a clean array, where the first thing is either a number (font size) or a font description.
    def removeBDC(self):
      del self.parseArray[0]  # This is an imperfect hack, because it contains the page number and some other information, but we'll work with it.

      for idx, elem in enumerate(self.parseArray):
        self.parseArray[idx] = elem[5:]

      return self.parseArray

  def __str__(self):
    return ''.join(self.opinion)

if __name__ == "__main__":
  fname = 'test_opinion.pdf'
  o = Opinion(fname)
  print(o.parse.parseArray)
  #print(o.splitMCIDs())
