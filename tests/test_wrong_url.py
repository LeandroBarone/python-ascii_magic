from context import ascii_magic

try:
	output = ascii_magic.from_url('https://wow.zamimg.com/uploads/blog/images/20516-afterlives-ardenweald-4k-desktop-wallpapers.jpg')
	ascii_magic.to_terminal(output)
except OSError as e:
	print(f'Could not load the image, server said: {e.code} {e.msg}')