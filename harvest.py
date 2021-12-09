import toolforge
from datetime import datetime
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

def dayselapsed(timestamp):
	created = datetime.fromisoformat(timestamp[:4]+'-'+timestamp[4:6]+'-'+timestamp[6:8]+'T'+timestamp[8:10]+':'+timestamp[10:12]+':'+timestamp[12:14])
	now = datetime.now()
	return (now - created).days

honap = {1:'január', 2:'február', 3:'március', 4:'április', 5:'május', 6:'június', 7:'július', 8:'augusztus', 9:'szeptember', 10:'október', 11:'november', 12:'december'};

conn = toolforge.connect('huwiki','analytics') # conn is a pymysql.connection object.
print('Database connection established. Executing query...')
query = "SELECT CONCAT('[[',page1.page_title,']]'), MIN(revision1.rev_timestamp) FROM page as page1 INNER JOIN revision AS revision1 ON page1.page_id = revision1.rev_page LEFT OUTER JOIN flaggedpages ON flaggedpages.fp_page_id = page1.page_id WHERE page1.page_namespace = 0 AND flaggedpages.fp_page_id IS NULL AND page1.page_is_redirect = 0 GROUP BY page1.page_title ORDER BY MIN(revision1.rev_timestamp) ASC LIMIT 500;"
query_redir = "SELECT CONCAT('{{plainlinks|1=[https://hu.wikipedia.org/w/index.php?title=',page1.page_title,'&redirect=no ',page1.page_title,']}}'), MIN(revision1.rev_timestamp) FROM page as page1 INNER JOIN revision AS revision1 ON page1.page_id = revision1.rev_page LEFT OUTER JOIN flaggedpages ON flaggedpages.fp_page_id = page1.page_id WHERE page1.page_namespace = 0 AND flaggedpages.fp_page_id IS NULL AND page1.page_is_redirect = 1 GROUP BY page1.page_title ORDER BY MIN(revision1.rev_timestamp) ASC LIMIT 500;"
n0 = 0
n30 = 0
n100 = 0
n200 = 0
n365 = 0
with conn.cursor() as cur: # querying articles
	rows = cur.execute(query) # number of affected rows
	output = open('result.csv', 'w')
	print('Query executed, result: '+str(rows)+' rows')
	for i in range(rows):
		row = cur.fetchone()
		days = dayselapsed(row[1].decode('utf-8'))
		output.write('# '+row[0].decode('utf-8')+' '+str(days)+' nap\n')
		if days < 30:
			n0 += 1
		elif days < 100:
			n30 += 1
		elif days < 200:
			n100 += 1
		elif days < 365:
			n200 += 1
		else:
			n365 += 1
	output.close()
with conn.cursor() as cur: # querying redirects
	rows = cur.execute(query_redir) # number of affected rows
	output = open('result_redir.csv', 'w')
	print('Query executed, result: '+str(rows)+' rows')
	for i in range(rows):
		row = cur.fetchone()
		days = dayselapsed(row[1].decode('utf-8'))
		output.write('# '+row[0].decode('utf-8')+' '+str(days)+' nap\n')
	output.close()
with open('data.csv', 'w') as output:
	now = datetime.now()
	output.write(str(now.year)+'. '+honap[now.month]+' '+str(now.day)+'.,'+str(n365)+','+str(n200)+','+str(n100)+','+str(n30)+','+str(n0)+','+str(n0+n30+n100+n200+n365))
conn.close()
