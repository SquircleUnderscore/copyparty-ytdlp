{
	// Insert HTML
	QS("#opdesc").insertAdjacentHTML("beforebegin", `<a href="#" id="opa_yt" tt="yt-dlp">▶️</a>`)
	QS("#op_cfg").insertAdjacentHTML("afterend",
`<div id="op_yt" class="opview opbox opwide">
	<h3>Download video</h3>
	<p>Download a video from youtube using <a href="https://github.com/yt-dlp/yt-dlp/">yt-dlp</a> straight to copyparty. The video will be put in the current directory.</p>
	<form id="op_yt_form" style="display: flex; flex-direction: column;">
		<label>
			Video URL:
			<input type="text" placeholder="any youtube URL" name="url">
		</label>
		<label>
			Output format:
			<label><input type="radio" name="fmt" value="" id="op_yt_def">auto</label>
			<label><input type="radio" name="fmt" value="mp4">mp4</label>
			<label><input type="radio" name="fmt" value="webm">webm</label>
			<label><input type="radio" name="fmt" value="mp3">audio (mp3)</label>
			<label><input type="radio" name="fmt" value="opus">audio (opus)</label>
			<label><input type="radio" name="fmt" value="opus">audio (flac)</label>
		</label>
		<input type="submit" value="Download" style="width: max-content">
	</form>
</div>
`)

	QS("#op_yt_def").checked = true
	
	const button = QS("#opa_yt")
	const page = QS("#op_yt")

	// Add event handlers
	button.addEventListener("click", (e) => {
		let en = !button.classList.contains("act")
		QSA(".opview, #ops > a").forEach((e) => e.classList.remove("act"))

		clmod(button, "act", en)
		clmod(page, "act", en)
		swrite("opmode", en ? "yt" : "")
	})

	QS("#op_yt_form").addEventListener("submit", (e) => {
		e.preventDefault()
		let data = new FormData(e.target)
		let url = data.get("url")
		if (!url)
			return
		let fmt = data.get("fmt")

		let req = new XMLHttpRequest()
		req.open("POST", get_evpath())
		req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
		req.send("msg=::ytdlp.exec?" + (fmt ? `fmt=${fmt}&url=` : "url=") + url_enc(url))
	})

	if (sread("opmode") == "yt") {
		clmod(button, "act", true)
		clmod(page, "act", true)
	}
}