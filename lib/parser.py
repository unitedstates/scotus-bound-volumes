#!/usr/bin/env python

import re
from PyPDF2 import PdfFileReader

class Opinion:
  
  def __init__(self, filename):
    self.fname = filename
    self.pdf = PdfFileReader(filename)
    self.opinion = self.getPages()

  def getPages(self):
    self.opinion = []
    for page in self.pdf.pages:
      self.opinion.append(page.getContents().getData().decode(encoding="utf-8",errors="strict"))
    return self.opinion

  def splitMCIDs(self):
    pattern = "<</MCID \d+ >>"
    self.MCIDs = re.compile(pattern).split(str(self))
    return self.MCIDs
  
  def __str__(self):
    return ''.join(self.opinion)

if __name__ == "__main__":
  fname = 'test_opinion.pdf'
  o = Opinion(fname)
  print(o)
  #print(o.isplitMCIDs())
