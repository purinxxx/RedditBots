import praw
import time

r = praw.Reddit(user_agent = 'RemoveModLog')
r.login()
houkoku = r.get_submission('https://www.reddit.com/r/newsokurMod/comments/2zz4a5/')

cache = []
f = open('cache.txt','r')
for line in f:
	cache.append(line.rstrip("\n"))
f.close()
print(cache)


def run_bot(target_subreddit):
	removecomment = r.get_mod_log(target_subreddit, mod=None, action='removecomment')
	removelink = r.get_mod_log(target_subreddit, mod=None, action='removelink')

	for comment in removecomment:
		#print(comment.target_permalink)
		#s = r.get_submission('http://www.reddit.com/' + comment.target_permalink)
		#print(s.comments[0])
		#print(dir(comment))
		if comment.target_permalink not in cache:
			h = '/u/' + comment.mod + ' が /u/' + comment.target_author + ' の ' + comment.target_permalink + ' のコメントを削除しました  \n'
			s = r.get_submission('https://www.reddit.com' + comment.target_permalink)
			if len(s.comments) > 0:
				text = str(s.comments[0])
				if len(text) > 200:
					h += 'comment : ' + text[:200] + '…  \n'
				else:
					h += 'comment : ' + text + '  \n'
				print(h)
				houkoku.add_comment(h)
			write_cache(comment.target_permalink)
		
	for link in removelink:
		#print(link.target_permalink)
		#print(dir(link))
		if link.target_permalink not in cache:
			h = '/u/' + link.mod + ' が /u/' + link.target_author + ' の ' + link.target_permalink + ' のスレを削除しました  \n'
			s = r.get_submission('https://www.reddit.com' + link.target_permalink)
			text = str(s.selftext)
			if len(text) > 200:
				h += 'url : ' + str(s.url) + '  \n'
				h += 'selftext : ' + text[:200] + '…  \n'
			else:
				h += 'url : ' + str(s.url) + '  \n'
				h += 'selftext : ' + text + '  \n'
			print(h)
			houkoku.add_comment(h)
			write_cache(link.target_permalink)


def write_cache(id):
	cache.append(id)
	print(cache)
	f = open('cache.txt','a')
	f.write(str(id) + '\n')
	f.close()


while True:
	try:
		run_bot('newsokur')
		time.sleep(60)
	except Exception as e:
		print(e)
		#f = open('error.txt','a')
		#f.write(str(e) + '\n')
		#f.close()

