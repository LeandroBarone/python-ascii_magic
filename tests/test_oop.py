from context import ascii_magic

ascii_art = ascii_magic.obj_from_image_file('lion.jpg')
ascii_art.to_terminal(columns=100, char='#')
