# -*- coding: utf-8 -*-
"""Art utilities library
"""
from HTMLParser import HTMLParser, HTMLParseError

#~ def uniEncode(data):
    #~ """uniencode data
    #~ """
    #~ encodings = ('ascii', 'cp1252', 'iso-8859-1', 'utf-8', 'euc-jp', 'sjis', 'utf-16-le', 'utf-16-be')
#~
    #~ for i in encodings:
	#~ try:
	    #~ return unicode(data, i)
	#~ except:
	    #~ pass
#~
    #~ return data


def reverseDict (dictionary):
    return dict([(val, key) for (key, val) in dictionary.items()])


def decodeHtmlSpecialChars(s):
    import re
    def decodeEntity(matchObj):
	entity = matchObj.group(3)
	if matchObj.group(1) == '#':
	    # decoding by number
            if matchObj.group(2) == 'x':
                # number is hex
                return unichr(int(entity, 16))
            else:
                # number is decimal
                return unichr(int(entity))
	else:
	    # decoding by name
	    import htmlentitydefs
            codePoint = htmlentitydefs.name2codepoint[entity]
            if codePoint:
		return unichr(codePoint)
            else:
		return matchObj.group()

    return re.sub(r'&(#?)(x?)(\w+);', decodeEntity, s)


class HTMLToXHTMLConverter(HTMLParser):
    """ Convert HTML to XHTML

	Example:

	f = open("elenco.html")
	data = f.read()

	converter = HTMLToXHTMLConverter()
	data = converter.get(data)

	print data

    """
    def get(self, data):
        self.convertedXHTML = ''

	try:
	    self.feed(data)
	except HTMLParseError:
	    pass

        return self.convertedXHTML

    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'hr', 'img', 'input', 'link'):
            self.convertedXHTML += self.get_starttag_text()[:-1] + ' />'
        else:
            self.convertedXHTML += self.get_starttag_text()

    def handle_endtag(self, tag):
        self.convertedXHTML += '</' + tag + '>'

    def handle_startendtag(self, tag, attrs):
        self.convertedXHTML += self.get_starttag_text()

    def handle_data(self, data):
        self.convertedXHTML += data

    def handle_charref(self, name):
        self.convertedXHTML += '&#' + name + ';'

    def handle_entityref(self, name):
        self.convertedXHTML += '&' + name + ';'


class HTMLExtractor(HTMLParser):
    """ Extract HTML fragment

	Example:

	f = open("elenco.html")
	data = f.read()

	extractor = HTMLExtractor()
	data = extractor.get('<div id="fragment">', data)

	print data

    """
    def get(self, HTMLTag, data):
        self.HTMLTag = HTMLTag
        self.appendHTML = False
        self.targetTag = ''
        self.tagDeepth = 0
        self.extractedHTML = ''

	try:
	    self.feed(data)
	except HTMLParseError:
	    pass

        return self.extractedHTML

    def handle_starttag(self, tag, attrs):
        #~ print dict(attrs).keys()
        #~ if tag == 'div' and dict(attrs).has_key('style'):
        if self.appendHTML:
            self.extractedHTML += self.get_starttag_text()
            if tag == self.targetTag:
                self.tagDeepth += 1
        else:
            if self.get_starttag_text() == self.HTMLTag:
                self.extractedHTML += self.HTMLTag
                self.appendHTML = True
                self.targetTag = tag
                self.tagDeepth += 1

    def handle_endtag(self, tag):
        if self.appendHTML:
            self.extractedHTML += '</' + tag + '>'

            if tag == self.targetTag:
                self.tagDeepth -= 1

            if self.tagDeepth == 0:
                self.appendHTML = False

    def handle_startendtag(self, tag, attrs):
        if self.appendHTML:
            self.extractedHTML += self.get_starttag_text()

    def handle_data(self, data):
        if self.appendHTML:
            self.extractedHTML += data

    def handle_charref(self, name):
        if self.appendHTML:
            self.extractedHTML += '&#' + name + ';'

    def handle_entityref(self, name):
        if self.appendHTML:
            self.extractedHTML += '&' + name + ';'


class XMLParser(HTMLParser):
    """ Extract XML data
    """
    results = {}
    element = {}
    extract = False
    extractElement = False
    extractTag = False
    extracted = ''

    def get(self, data, containerTag, elementTag='', tagsToExtract=[]):
	self.containerTag = containerTag
	self.elementTag = elementTag
	self.tags = tagsToExtract

	try:
	    self.feed(data)
	except HTMLParseError:
	    pass
	except Exception as e:
	    self.results = str(e)

        return self.results

    def handle_starttag(self, tag, attrs):
        if tag == self.containerTag:
            self.results = {}
	    self.extract = True
        elif tag == self.elementTag:
	    if tag not in self.results:
		self.results[tag] = []
            self.element = {}
	    self.extractElement = True
        elif self.extract and (self.tags == [] or tag in self.tags):
            self.extractTag = True
            self.extracted = ''

    def handle_endtag(self, tag):
        if tag == self.containerTag:
	    self.extract = False
        elif tag == self.elementTag:
	    self.extractElement = False
            self.results[tag].append(self.element)
        elif self.extractTag and (self.tags == [] or tag in self.tags):
	    self.extractTag = False
	    if self.extractElement:
		self.element[tag] = self.extracted
	    else:
		self.results[tag] = self.extracted

    def handle_data(self, data):
        if self.extract:
            self.extracted += data

    def handle_charref(self, name):
        if self.extract:
            self.extracted += '&#' + name + ';'

    def handle_entityref(self, name):
        if self.extract:
	    if name == 'amp':
		self.extracted+= '&'
	    elif name == 'lt':
		self.extracted+= '<'
	    elif name == 'gt':
		self.extracted+= '>'
	    elif name == 'quot':
		self.extracted+= '"'
	    else:
		self.extracted+= '&' + name + ';'

def toTxt(html):
    """
    Convert html to text
    """

    import htmlentitydefs
    import xml.sax.saxutils
    import re

    txt = ''

    #~ dict(('&'+k+';', v) for k,v in htmlentitydefs.entitydefs.iteritems())
    #~ dict((unichr(v), '&'+k+';') for k,v in htmlentitydefs.name2codepoint.iteritems())

	#~ $revTransTable=get_html_translation_table(HTML_ENTITIES);
	#~ $revTransTable=array_flip($revTransTable);
	#~ $text=$HTML;
	#~ $text=strip_tags($text, "<style><title><h1><h2><h3><h4><h5><h6><p><a><br><b><strong><ol><ul><li>");
	#~ $text=putHTMLEnts($text, true);
	#~ $text=preg_replace('/[\r\n]+/', "", $text);
	#~ $text=preg_replace('/[\t]+/', "  ", $text);
	#~ $text=preg_replace('/<style[^>]*>[^<]*<\/style>|<h[1-6][^>]*>|<p[^>]*>/i', "", $text);
	#~ $text=preg_replace('/<br[^>]*>|<br[^>]* \/>|<ol[^>]*>|<\/ol>|<ul[^>]*>|<\/ul>|<\/li>/i', $GLOBALS["EOL"], $text);
	#~ $text=preg_replace('/<\/h[1-6]>|<\/p>/i', $GLOBALS["EOL"].$GLOBALS["EOL"], $text);
	#~ $text=preg_replace('/<b[^>]*>|<strong[^>]*>|<\/b>|<\/strong>/i', "*", $text);
	#~ $text=preg_replace('/<title[^>]*>([^<]*)<\/title>/i', "# # "."$1"." # #".$GLOBALS["EOL"].$GLOBALS["EOL"], $text);
	#~ $text=preg_replace('/<a[^>]+href="?([^"\s>]+)"?([^>]*)>([^<]*?)<\/a>/i', "$3"." ["."$1"."]", $text);
	#~ $text=preg_replace('/<li[^>]*>/i', " - ", $text);
#~
	#~ return $text;
    return txt