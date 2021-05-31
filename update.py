from mwclient import Site
import re
from datetime import date
import os
from pathlib import Path

pagename = 'Wikipédia:Járőrök üzenőfala/Legrégebbi'

def update_list(list):
	page = site.pages[pagename]
	text = page.text()
	m = re.search('(?s).*{{hasáb eleje}}', text)
	page.edit(m.group(0) + list + '\n{{hasáb vége}}', 'Bot: Lista frissítése')

def update_both(data, list):
	page = site.pages[pagename]
	text = page.text()
	top = '(.*összesen\n \|-\n)'
	line = '( \| [^|]* \| [^|]* \|[^|]* \|[^|]* \|[^|]* \|[^|]* \|[^|]* \|-\n)'
	m = re.search('(?s)'+top+line+line+line+line+' \|}', text)
	page.edit(m.group(1) + data + m.group(2) + m.group(3) + m.group(4) + ' |}\n== Lista ==\n{{hasáb eleje}}'  + list + '\n{{hasáb vége}}', 'Bot: Táblázat és lista frissítése')

ua = 'Bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
site.login('', '')

with open('result.csv', 'r') as stream:
	lines = stream.readlines();
	new_list = '\n\n'
	for line in lines:
		new_list += line.replace('_',' ');

path = Path('monday.dat')
if date.today().weekday() == 0: # if today is a Monday
	if path.exists(): # if the file already exists, then the table has already been updated, so update only the list
		update_list(new_list);
	else: # if the file does not exist, update table and list, then create file
		with open('data.csv', 'r') as stream:
			data = ' | ' + stream.readline().replace(',','\n | ') + '\n |-\n'
		update_both(data, new_list);
		with open('monday.dat', 'w') as output:
			output.write('1');
else: # if today is not a Monday
	try: # if the file exists, delete it
		os.remove(path);
	except: # if the file does not exist, do nothing
		pass;
	finally: # update list
		update_list(new_list);
