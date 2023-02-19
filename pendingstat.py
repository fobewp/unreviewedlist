import toolforge
from mwclient import Site
import re

ua = 'Bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
pagename = 'Wikipédia:Járőrök üzenőfala/Statisztika'
with open('my.credentials', 'r') as input:
	password = input.readline().split('\n')[0]
	site.login('FoBeBot', password)

def update_stat(data):
	page = site.pages[pagename]
	text = page.text()
	m = re.search('(?s)(.*)( \|-\n \|\})', text)
	insert = ' |-\n | {{subst:LOCALYEAR}}-{{subst:LOCALMONTH}}-{{subst:LOCALDAY2}}\n'
	for i in data:
		insert += ' | {{szám|'+str(i)+'}}\n'
	print(insert)
	page.edit(m.group(1) + insert + m.group(2), 'Bot: Táblázat  frissítése')


conn = toolforge.connect('huwiki','analytics')
queries = [
	"SELECT COUNT(rev_id) FROM revision INNER JOIN page ON rev_page = page_id INNER JOIN flaggedpage_pending ON page_id = fpp_page_id WHERE rev_id > fpp_rev_id;",
	"SELECT COUNT(DISTINCT rev_id) FROM revision INNER JOIN page ON rev_page = page_id INNER JOIN flaggedpage_pending ON page_id = fpp_page_id INNER JOIN actor ON actor_id = rev_actor LEFT OUTER JOIN user_groups ON ug_user = actor_user WHERE rev_id > fpp_rev_id AND ug_group IN ('editor','trusted','sysop','bot');",
	"SELECT COUNT(*) FROM flaggedpage_pending",
	"SELECT COUNT(DISTINCT page_id) FROM revision INNER JOIN page ON rev_page = page_id INNER JOIN flaggedpage_pending ON page_id = fpp_page_id INNER JOIN actor ON actor_id = rev_actor LEFT OUTER JOIN user_groups ON ug_user = actor_user WHERE rev_id > fpp_rev_id AND ug_group IN ('editor','trusted','sysop','bot');"
]
num = [None] * 4;
with conn.cursor() as cur:
	for i in range(4):
		print("Query "+str(i)+"...", end="")
		rows = cur.execute(queries[i])
		print(" executed", end="")
		num[i] = cur.fetchone()[0]
		print(": "+str(num[i]))
	update_stat(num)
conn.close()
