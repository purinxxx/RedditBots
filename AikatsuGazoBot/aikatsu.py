import praw
import time
import random
import datetime
import locale

r = praw.Reddit(user_agent = 'Ozora Akari')
#r.login()
r.login()

match = ['アイカツ']
cache = []
f = open('cache.txt','r')
for line in f:
	cache.append(line.rstrip("\n"))
f.close()
print('キャッシュ読み込み成功')
print(cache)

gazo = []
f = open('gazo.txt','r')
for line in f:
	gazo.append(line.rstrip("\n"))
f.close()
print('アイカツ画像読み込み成功')
print(gazo)

def run_bot(target_subreddit):
	subreddit = r.get_subreddit(target_subreddit)
	comments = subreddit.get_comments(limit=25)
	for comment in comments:
		comment_text = comment.body.lower()
		isMatch = any(string in comment_text for string in match)
		if comment.id not in cache and isMatch:
			print('アイカツ発見！')
			reply_aikatsu(comment)
			print(str(target_subreddit) + '　で　アイカツ画像を送りつけてやったぜ')
			cache.append(comment.id)
			print(cache)
			f = open('cache.txt','a')
			f.write(str(comment.id) + '\n')
			f.close()
			print('キャッシュ書き込み成功')

def reply_aikatsu(target_comment):
	gazo_kazu = len(gazo) - 1
	target_comment.reply(gazo[random.randint(0,gazo_kazu)])

while True:
	try:
		print(datetime.datetime.today().strftime("%x %X"))
		print('yarou')
		run_bot('yarou')
		time.sleep(20)
		print('newsokur')
		run_bot('newsokur')
		time.sleep(20)
		print('japan_anime')
		run_bot('japan_anime')
		time.sleep(20)
		print('BakaNewsJP')
		run_bot('BakaNewsJP')
		time.sleep(20)
		print('newsokuvip')
		run_bot('newsokuvip')
		time.sleep(20)
	except Exception as e:
		print(e)
		f = open('error.txt','a')
		f.write(str(e) + '\n')
		f.close()
		print('エラー書き込み成功')

#/u/AikatsuGazoBot
#['cttsokw', 'cttpe7x', 'cttonby']