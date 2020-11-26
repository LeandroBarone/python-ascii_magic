import ascii_magic

output = ascii_magic.from_image_file('picture.jpg', columns=100, width_ratio=2.6, char='#')
ascii_magic.to_terminal(output)