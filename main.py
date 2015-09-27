from lib.parser import Opinion
import os
import json

fname = os.path.dirname(os.path.realpath(__file__)) + "/source_documents/14-95.pdf"
# fname = os.path.dirname(os.path.realpath(__file__)) + "/lib/test_opinion.pdf"

o = Opinion(fname)
with open('test.html', 'w') as f:
  f.write(o.parse.html)