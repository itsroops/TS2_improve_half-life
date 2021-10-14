#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing necessary packages
import yasara
from yasara import *
import os


# Only using text mode, change to 'gra' for graphics
#info.mode = "txt"

# Turn the yasara console off
Console("On")


# Mapping the three-letter amino acid too one-letter amino-acid
amino_dict = {'C':'Cys', 'D':'Asp', 'S':'Ser', 'Q':'Gln', 'K':'Lys',
     'I':'Ile', 'P':'Pro', 'T':'Thr', 'F':'Phe', 'N':'Asn', 
     'G':'Gly', 'H':'His', 'L':'Leu', 'R':'Arg', 'W':'Trp',
     'A':'Ala', 'V':'Val', 'E':'Glu', 'Y':'Tyr', 'M':'Met'}


def SwapAndMinimize(loci, ff, struct_path, macro_path, output_path):
    print(list(loci.split(" "))) 
    print(ff)
    print(struct_path)
    print(macro_path)
    print(output_path)

if __name__ == "__main__":
    SwapAndMinimize(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    

