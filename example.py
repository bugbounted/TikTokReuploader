from youtubesearchpython import VideosSearch
import youtube_dl
from tiktok import *

''' 

# Upload TikTok Trendings
# trendings doesn't work..

trendings = get_trendings()
for video in trendings:
	path = download_video(video['video'])

	upload_video(
		path = path,
		description = video['desc'],
		tags = [
			get_tags_from_desc(video['desc'])
		]
	)
'''

# read used tags
with open("used_tags.txt", "r") as f:
	used_tags = f.read().split("\n")

# search for some videos
videos = VideosSearch('respect tiktok videos shorts', limit = 50).result()['result']

# how many videos should be uploaded
upload_video_count = 5

# this value is only for counting, don't change it
current_video_count = 0

for video in videos:

	# if the count is greater than the count
	if current_video_count > upload_video_count:
		break

	# if the video has been already uploaded
	if video['id'] in used_tags:
		continue

	# get the time 
	times = video['duration'].split(":")

	if len(times) == 2:
		minutes, seconds = times

	else: # 3
		hours, minutes, seconds = times

	# if the video length is more than 1 minute, you can't remove this if you want, tiktok doesn't have time limit only file size limit
	if int(minutes) > 1:
			continue

	# get the youtube url
	url = f"https://www.youtube.com/watch?v={video['id']}"

	# get new path for file
	path = f"{DIR}\\videos\\{video['id']}.mp4"

	print("Downloading video from youtube..")

	# download video only if the video wasn't downloaded already
	if not os.path.exists(path):
		# ydl options
		ytdl_opts = {
			"outtmpl" : path,
			'forcefilename' : True
		}

		try:
			with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
				ytdl.download([url])
		except:
			# if there were some errors, skip
			continue

	# rename file if neccesary
	if not os.path.exists(path):

		if os.path.exists(path + ".mkv"):
			os.rename(path + ".mkv", path)

		elif os.path.exists(path + ".webm"):
			os.rename(path + ".webm", path)

		elif os.path.exists(path + ".mk4"):
			os.rename(path + ".mk4", path)

		else:
			print("Invalid file extension.. Ignoring")
			continue

	# add current tag to used tags
	used_tags.append(video['id'])

	# save used tags to file
	with open("used_tags.txt", "w") as f:
		f.write('\n'.join(used_tags))

	# increate current video count
	current_video_count += 1

	# upload video to tiktok
	upload_video(
		path = path,
		description = video['title'],
		tags = [
			"foryou", "funny"
		]
	)