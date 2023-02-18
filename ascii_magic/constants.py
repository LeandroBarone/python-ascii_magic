import colorama


_COLOR_DATA = [
    [(0, 0, 0), colorama.Fore.LIGHTBLACK_EX, '#222'],
    [(0, 0, 255), colorama.Fore.BLUE, '#00F'],
    [(0, 255, 0), colorama.Fore.GREEN, '#0F0'],
    [(255, 0, 0), colorama.Fore.RED, '#F00'],
    [(255, 255, 255), colorama.Fore.WHITE, '#FFF'],
    [(255, 0, 255), colorama.Fore.MAGENTA, '#F0F'],
    [(0, 255, 255), colorama.Fore.CYAN, '#0FF'],
    [(255, 255, 0), colorama.Fore.YELLOW, '#FF0']
]

PALETTE = [[[(v/255.0)**2.2 for v in x[0]], x[1], x[2]] for x in _COLOR_DATA]

CHARS_BY_DENSITY = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q'

DEFAULT_STYLES = 'display: inline-block; border-width: 4px 6px; border-color: black; border-style: solid; background-color:black; font-size: 8px;'
