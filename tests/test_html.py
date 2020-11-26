from context import ascii_magic

ascii_art = ascii_magic.from_image_file('lion.jpg', columns=200, mode=ascii_magic.Modes.HTML)

markup = f"""<!DOCTYPE html>
<html>
<body style="background-color: black; font-size: 8px;">
<pre>
{ascii_art}
</pre>
</body>
</html>"""

with open('output_html.html', 'w') as f:
	f.write(markup)