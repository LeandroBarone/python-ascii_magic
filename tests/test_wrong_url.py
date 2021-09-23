from context import ascii_magic

try:
	output = ascii_magic.from_url('https://images2.alphacoders.com/902/thumb-1920-902946.png')
	ascii_magic.to_terminal(output)
except OSError as e:
	print(f'Could not load the image, server said: {e.code} {e.msg}')