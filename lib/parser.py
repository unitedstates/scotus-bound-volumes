#!/usr/bin/env python

import re
import json
from PyPDF2 import PdfFileReader
import pdb
from ftfy import fix_text, explain_unicode

class Opinion:

  def __init__(self, filename):
    self.fname = filename
    self.pdf = PdfFileReader(filename)
    self.opinion = self.getPages()
    self.parse = self.Parser(self)

  def __str__(self):
    return json.dumps(self.opinion, indent=2)

  def getPages(self):
    self.opinion = []
    
    for idx, page in enumerate(self.pdf.pages):
      self.opinion.append({"page": idx, "contents": page.getContents().getData().decode('cp1252')})
    return self.opinion

  class Parser:
    
    def __init__(self, opinion):
      self.opinion = opinion
      self.sizes = [] # This is an array where we're going to put the sizes, then we we discover a size, if it's a known size call it "<div class='style-idx'> " where idx is the index of the sizes array
      self.opinion = self.extractTextByOperator()
      self.html = ''.join(list(map(lambda x: x["results"],self.opinion)))

    def extractTextByOperator(self):
      """
      This is the workhorse
      """
      from PyPDF2.pdf import ContentStream
      from PyPDF2.generic import TextStringObject

      for idx, page in enumerate(self.opinion.pdf.pages):
        self.opinion.opinion[idx]["results"] = ""
        operations = []
        contents = page["/Contents"].getObject()
        contents = ContentStream(contents, page.pdf)
        out = ""
        span = ""
        c = None
        for operands, operator in contents.operations:
          if operator == b'Tf' and operands[1] != " ":
            # pdb.set_trace()
            span = '<span class="font-style-' + str(operands[0])[1:] + '-' + str(operands[1]) + '">'
            out += '</span>' + span
          if operator == b'Tm':
            font_size = operands[3]
            if c != font_size:
              out += '</span></div>\n<div class="font-size-' + str(self.getOrUpdateSize(font_size)) + '">' + span
              c = font_size
          elif operator == b'Tj':
            out += fix_text(operands[0].original_bytes.decode('cp1252'), fix_entities=False, fix_character_width=False)
          elif operator == b'TJ':
            for i in operands[0]:
              if not isinstance(i, int):
                out += fix_text(i.original_bytes.decode('cp1252'), fix_entities=False,fix_character_width=False)

          elif operator == b'T*':
            out += "\n"
          elif operator == b'Td' or operator == b'TD':
            out += "\n"
        out += "</span></div>"  
        self.opinion.opinion[idx]["results"] += out
      return self.opinion.opinion

    def getOrUpdateSize(self, size):
      try:
        return self.sizes.index(size)
      except:
        self.sizes.append(size)
        return len(self.sizes) - 1

if __name__ == "__main__":
  import os
  fname = os.path.dirname(os.path.realpath(__file__)) + '/test_opinion.pdf'
  o = Opinion(fname)
  print(o.parse.html)