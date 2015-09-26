from lib.parser import Opinion
import os
import json

fname = os.path.dirname(os.path.realpath(__file__)) + "/lib/test_opinion.pdf"
o = Opinion(fname)
print(o.parse.html)