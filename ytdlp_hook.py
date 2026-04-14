import os, threading, subprocess, re, json, shutil, sys

def _main(vid_url : str, out_dir : str, format : str | None = None, quality : str | None = None, plugin_dir : str = ""):
	cmd = ["yt-dlp"]
	
	# prefer local yt-dlp if available
	local_ytdlp = os.path.join(plugin_dir, "yt-dlp")
	local_ytdlp_win = os.path.join(plugin_dir, "yt-dlp.exe")
	if os.path.exists(local_ytdlp_win):
		cmd = [local_ytdlp_win]
	elif os.path.exists(local_ytdlp):
		if os.access(local_ytdlp, os.X_OK):
			cmd = [local_ytdlp]
		else:
			cmd = [sys.executable, local_ytdlp]
		
	cmd += [vid_url, "-P", out_dir, "--no-mtime"]
	
	# fallback to local ffmpeg to bypass stripped docker versions
	local_ffmpeg = os.path.join(plugin_dir, "ffmpeg")
	local_ffmpeg_win = os.path.join(plugin_dir, "ffmpeg.exe")
	if os.path.exists(local_ffmpeg):
		cmd += ["--ffmpeg-location", local_ffmpeg]
	elif os.path.exists(local_ffmpeg_win):
		cmd += ["--ffmpeg-location", local_ffmpeg_win]
	
	if format in ["mp3", "opus", "flac"]:
		cmd +=["-x", "--audio-format", format]
	else:
		sort_args =[]
		if quality and quality.isdigit():
			sort_args.append(f"res:{quality}")
		
		if format == "mp4":
			sort_args.append("ext:mp4:m4a")
			cmd +=["--merge-output-format", "mp4"]
		elif format:
			cmd +=["--remux-video", format]
		
		if sort_args:
			cmd +=["-S", ",".join(sort_args)]

	try:
		proc = subprocess.Popen(cmd)
		proc.wait()
	except FileNotFoundError:
		print("ytdlp: executable not found")

def main(args):
	if "w" not in args.get("perms", ""):
		return

	prefix = "::ytdlp.exec?"
	
	txt = args.get("txt", "")
	url, fmt, quality = None, None, None

	# require plugin namespace and support json payloads for complex urls
	if not txt.startswith(prefix):
		return

	payload = txt[len(prefix):]
	if payload.startswith("{"):
		try:
			data = json.loads(payload)
			url = data.get("url")
			fmt = data.get("fmt")
			quality = data.get("quality")
		except:
			return
	else:
		# Don't ask me why there's a \n somewhere in there
		match = re.match(r"^::ytdlp\.exec\?(?:fmt=(.+)\n)?url=(.+)$", txt, re.U)
		if not match:
			return
		match_groups = match.groups()
		url = match_groups[-1]
		fmt = None if len(match_groups) == 1 else match_groups[0]
	
	if not url:
		return

	if not shutil.which("yt-dlp"):
		plugin_dir_check = os.path.dirname(os.path.abspath(__file__))
		if not os.path.exists(os.path.join(plugin_dir_check, "yt-dlp")) and not os.path.exists(os.path.join(plugin_dir_check, "yt-dlp.exe")):
			return "no_ytdlp"
		
	base_dir = args["ap"].rstrip("/") + "/"
	
	try:
		plugin_dir = os.path.dirname(os.path.abspath(__file__))
	except:
		plugin_dir = base_dir
		
	threading.Thread(target=_main, args=(url, base_dir, fmt, quality, plugin_dir)).start()