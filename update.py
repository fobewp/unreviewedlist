from mwclient import Site
import re
from datetime import date

#pagename = 'User:FoBe/Legrégebbi'
pagename = 'Wikipédia:Járőrök üzenőfala/Legrégebbi'

def update_list(list):
	page = site.pages[pagename]
	text = page.text()
	m = re.search('(?s).*{{hasáb eleje}}', text)
	page.edit(m.group(0) + list + '\n{{hasáb vége}}', 'Bot: Lista frissítése')

ua = 'Bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
with open('my.credentials', 'r') as input:
	password = input.readline().split('\n')[0]
	site.login('FoBeBot', password)

with open('result.csv', 'r') as stream:
	lines = stream.readlines();
	new_list = '\n\n'
	for line in lines:
		new_list += line.replace('_',' ');
	update_list(new_list);
