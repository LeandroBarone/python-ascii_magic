from context import ascii_magic

output = ascii_magic.from_image_file('kid.jpg', columns=200, mode=ascii_magic.Modes.HTML)
ascii_magic.to_html_file('kid.html', output)