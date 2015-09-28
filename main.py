from lib.parser import Opinion
import os
import json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("output")
args = parser.parse_args()

fname = os.path.dirname(os.path.realpath(__file__)) + "/" + args.filename #"/source_documents/14-95.pdf"
# fname = os.path.dirname(os.path.realpath(__file__)) + "/lib/test_opinion.pdf"

o = Opinion(fname)
with open(args.output, 'w') as f:
  f.write(o.parse.html)