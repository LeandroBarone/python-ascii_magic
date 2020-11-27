from context import ascii_magic

output = ascii_magic.from_clipboard(columns=100, width_ratio=2, char='@')
ascii_magic.to_terminal(output)