from mwclient import Site
import re
from datetime import date

#pagename = 'User:FoBe/Legrégebbi'
pagename = 'Wikipédia:Járőrök üzenőfala/Legrégebbi'

def update_list(list): # deprecated
	page = site.pages[pagename]
	text = page.text()
	m = re.search('(?s).*{{hasáb eleje}}', text)
	page.edit(m.group(0) + list + '\n{{hasáb vége}}', 'Bot: Lista frissítése')

def update_list_with_redir(list,list_redir):
	page = site.pages[pagename]
	text = page.text()
	m = re.search('(?s).*== Lista ==', text)
	page.edit(m.group(0) + list + list_redir, 'Bot: Lista frissítése')

ua = 'Bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
with open('my.credentials', 'r') as input:
	password = input.readline().split('\n')[0]
	site.login('FoBeBot', password)

new_list = '\n{{hasáb eleje}}\n'
with open('result.csv', 'r') as stream:
	lines = stream.readlines();
	for line in lines:
		new_list += line.replace('_',' ');
new_list += '\n{{hasáb vége}}\n'
new_list_redir = '=== Átirányítások ===\n{{hasáb eleje}}\n'
with open('result_redir.csv', 'r') as stream:
	lines = stream.readlines();
	for line in lines:
		match = re.search('\?title=([^&]+)&', line);
		if match:
			new_list_redir += line.replace('=no '+match.group(1),'=no '+match.group(1).replace('_',' '));
new_list_redir += '\n{{hasáb vége}}'

update_list_with_redir(new_list, new_list_redir);
