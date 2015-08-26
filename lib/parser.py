#!/usr/bin/env python


import re
import json
import pdb
from PyPDF2 import PdfFileReader

class Opinion:

  def __init__(self, filename):
    self.fname = filename
    self.pdf = PdfFileReader(filename)
    self.opinion = self.getPages()
    self.parse = self.Parser(self)

  def getPages(self):
    self.opinion = []
    for idx, page in enumerate(self.pdf.pages):
      self.opinion.append({"page": idx, "contents": page.getContents().getData().decode(encoding="utf-8",errors="strict")})
    return self.opinion

  class Parser:
    
    def __init__(self, opinion):
      self.opinion = opinion
      self.opinion = self.extractText()
      pdb.set_trace()

    # So, here's the magic. First, split based on style (e.g., italicized and whatnot) (assign a class="style-1" or class="style-2"). Then, look for the first instance of r"(([\d|.]+)(\s)){6}" within the split. The first float in that regex is actually the font size (assign class=". So, grab the first float, note its size, grab all of the internal text and look for the next instance. If it's the same size, append. If not, group into another bucket.

    # Note, I haven't done the _first_ part yet here, which is to split based on style... more TK.


    def splitText(self):
      for idx, page in enumerate(self.opinion.opinion):
        self.opinion.opinion[idx]["contents"] = page["contents"].split("/T1_")
        self.opinion.opinion[idx]["text"] = {}
        for i, block in enumerate(self.opinion.opinion[idx]["contents"]):
          self.opinion.opinion[idx]["text"][i] = {}
          self.opinion.opinion[idx]["text"][i]["text"] = self.extractText(block)
          self.opinion.opinion[idx]["text"][i]["style"] = block[0]
      return self.opinion.opinion

    def extractText(self):
      text_pattern = "(?<=\().*?(?=\))"  
      match_pattern = "(([\d|.]+\s){6}Tm)(.*?)(?=([\d|.]+\s){6})"
      for idx, page in enumerate(self.opinion.opinion):
        r = re.findall(match_pattern, page["contents"]) #Note, this will likely miss the last words of the opinion.... 
        self.opinion.opinion[idx]["results"] = ""
        for m in r:
          size = re.match('([\d|.]+)', m[0]).group(0)
          text = re.findall(text_pattern, ''.join(m))
          out = "<span class='size-" + size + "'>" + ''.join(text) + "</span>"
          self.opinion.opinion[idx]["results"] += out
      return self.opinion.opinion

  def __str__(self):
    return json.dumps(self.opinion, indent=2)

if __name__ == "__main__":
  fname = 'test_opinion.pdf'
  o = Opinion(fname)
  print(o.parse.opinion)
