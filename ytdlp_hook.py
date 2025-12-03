import os, threading, subprocess, re

def _main(vid_url : str, out_dir : str, format : str | None = None):
	refmt = []
	if format in ["mp3", "opus"]:
		refmt = ["-x", "--audio-format", format]
	elif format:
		refmt = ["--remux-video", format]
	
	proc = subprocess.Popen([
		"python",
		"./yt-dlp",
		vid_url,
		"-P",
		out_dir,
		*refmt
	], stdout=subprocess.PIPE)
	proc.wait()

def main(args):
	# Don't ask me why there's a \n somewhere in there
	match = re.match(r"^::ytdlp\.exec\?(?:fmt=(.+)\n)?url=(.+)$", args["txt"], re.U)
	if not match:
		return
	if "w" not in args["perms"]:
		return
	if not os.path.exists("./yt-dlp"):
		return "no_ytdlp"
	
	match_groups = match.groups()
	url = match_groups[-1]
	fmt = None if len(match.groups()) == 1 else match_groups[0]
	base_dir = args["ap"].rstrip("/") + "/"
	print(url, fmt)
	
	threading.Thread(target=_main, args=(url, base_dir, fmt)).start()