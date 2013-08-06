from html import parser
from urllib.request import urlopen, Request
from urllib import error

import sys
sys.setrecursionlimit( 10000 )

# wikipedia's host url
url_addr = 'http://www.en.wikipedia.org';
counter = 100
term = '/wiki/'
end = False
start = input( "Type in starting conception: " )
term += start

def make_url( wiki, term ):
	'''	Creates an url for wiki site 
		with a term description. 	 '''
		
	return wiki + term

	
def get_attr( name, attrs ):
	''' returns given attribute's value '''

	for n, v in attrs:
		if n == name:
			return v
	return None

class ParserExClass( parser.HTMLParser ):
	''' Parser extension which is supposed to 
		extract first link from the inside of
		wiki article, skipping unimportant stuff. '''
		
	def handle_starttag( self, tag, attrs ):
		if tag == 'div' and get_attr("id", attrs) == 'mw-content-text':
			self.disambig = True
		elif self.disambig and  tag == 'p':
			self.section = True
		elif self.section and tag == 'a':
			global url_addr, term, addr, end
			temp = get_attr( "href", attrs )
			if temp[0:5] == '/wiki':
				if temp.find( ':' ) == -1:
					term = temp
					if not self.level:
						self.level = True
					else:
						end = True
				
		pass
	def handle_endtag( self, tag ):
		pass
	def handle_data( self, data ):
		pass
		
		
P = ParserExClass( strict=False )
for i in range( counter ):
	addr = url_addr+term
	print( addr )
	req = Request( addr, headers={'User-Agent' : "Magic Browser"} )
	source = urlopen( req )
	P.section, P.disambig, P.level = False, False, False
	for line in source.read().decode( 'utf-8' ):
		P.feed( line )
		if end:
			break
	end = False
	
	