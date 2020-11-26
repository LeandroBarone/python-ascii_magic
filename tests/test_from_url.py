from context import ascii_magic

from_url = ascii_magic.from_url('https://source.unsplash.com/800x600?nature', columns=50, char='@')
ascii_magic.to_terminal(from_url)