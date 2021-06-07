from mwclient import Site
import re
from datetime import date

pagename = 'Wikipédia:Járőrök üzenőfala/Legrégebbi/táblázat'

def update_table(data):
	page = site.pages[pagename]
	text = page.text()
	top = '(.*összesen\n \|-\n)'
	line = '( \| [^|]* \| [^|]* \|[^|]* \|[^|]* \|[^|]* \|[^|]* \|[^|]* \|-\n)'
	m = re.search('(?s)'+top+line+line+line+line+' \|}', text)
	page.edit(m.group(1) + data + m.group(2) + m.group(3) + m.group(4) + ' |}\n', 'Bot: Táblázat  frissítése')

ua = 'Bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
with open('my.credentials', 'r') as input:
	password = input.readline().split('\n')[0]
	site.login('FoBeBot', password)

with open('data.csv', 'r') as stream:
	data = ' | ' + stream.readline().replace(',','\n | ') + '\n |-\n'
	update_table(data);
