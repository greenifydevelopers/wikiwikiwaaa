import pypandoc
from flask import send_file

def convertODT(url):
    pypandoc.convert('content/' + url + '.md', 'odt', outputfile='content/createdodts/' + url + '.odt',
                    extra_args=['-V geometry:margin=1.5cm'])
    try:
        return send_file('../../content/createdodts/' + url + '.odt')
    except IOError:
        pass