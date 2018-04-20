import pypandoc
from flask import send_file
import os

def onePDF(url):
    outfile = open("content/workmd/testfile.md", "w")
    for filename in os.listdir('content/'):
       if filename.endswith(".md"):
           f = open('content/' + filename, 'r')
           outfile.write(f.read())
           outfile.write('\n\n')
    outfile.close()
    pypandoc.convert('content/workmd/testfile.md', 'pdf', outputfile='content/createdpdfs/fullWiki.pdf',
                    extra_args=['-V geometry:margin=1.5cm'])
    try:
        return send_file('../../content/createdpdfs/fullWiki.pdf')
    except IOError:
        pass