# ASCII Magic

Python package that converts images into ASCII art for terminals and HTML. Thanks to Colorama it's compatible with the Windows terminal. Code based on [ProfOak's Ascii Py](https://github.com/ProfOak/Ascii_py/).

## Basic usage

```python
import ascii_magic
output = ascii_magic.from_image_file('images/moon.jpg')
ascii_magic.to_terminal(output)
```

Result:

![ASCII Magic example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_moon.png)

# Available functions

## from_image_file()

Converts an image file into ASCII art.

```python
ascii_magic.from_image_file(
    path: str,
    columns: int = 120,
    width_ratio: float = 2,
    char: str = None,
    back: Back = None,
    mode: Modes = Modes.TERMINAL,
) -> str
```

- path => a PIL-compatible file, such as a jpeg or png
- columns (optional) => the number of characters per row, more columns = wider art
- width_ratio (optional) => ASCII characters are not squares, so this adjusts the width to height ratio
- char (optional) => instead of using many different ASCII glyphs, you can use a single one, such as '#'
- back (optional) => In terminal mode, sets the background color with one of:
  - ```ascii_magic.Back.BLACK```
  - ```ascii_magic.Back.RED```
  - ```ascii_magic.Back.GREEN```
  - ```ascii_magic.Back.YELLOW```
  - ```ascii_magic.Back.BLUE```
  - ```ascii_magic.Back.MAGENTA```
  - ```ascii_magic.Back.CYAN```
  - ```ascii_magic.Back.WHITE```
- mode (optional) => one of:
  - ```ascii_magic.Modes.TERMINAL```  => outputs ASCII with terminal color codes (8 tones)
  - ```ascii_magic.Modes.ASCII```  => outputs pure ASCII with no color codes, resulting in a "grayscale" image
  - ```ascii_magic.Modes.HTML_TERMINAL``` => outputs HTML simulating terminal colors; wrap it in a ```<pre>```
  - ```ascii_magic.Modes.HTML``` => as above, but with full color

Example:

```python
output = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    back=ascii_magic.Back.BLUE
)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_blue.png)

Example:

```python
output = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    width_ratio=2,
    mode=ascii_magic.Modes.HTML
)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_html.png)

Example:

```python
output = ascii_magic.from_image_file(
    'images/lion.jpg',
    columns=200,
    mode=ascii_magic.Modes.ASCII
)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_ascii.png)

## from_url()

As above, but using the URL of an image.

```python
ascii_magic.from_url(
    url: str,
    # ... as above
) -> str
```

- url => an URL which will be loaded via urllib (supports redirects)

Example:

```python
img_url = 'https://source.unsplash.com/800x600?nature'
output = ascii_magic.from_url(img_url, columns=100)
```

## from_clipboard()

As above, but with the contents of the clipboard. Raises ValueError if the clipboard doesn't contain an image.

```python
ascii_magic.from_clipboard(
    # ... as above
) -> str
```

Example:

```python
output = ascii_magic.from_clipboard(columns=100)
```

## from_image()

As above, but using an image loaded with Pillow.

```python
ascii_magic.from_image(
    img: Image,
    # ... as above
) -> str
```

- img => PIL image object

Example:

```python
from PIL import Image
with Image.open('images/1.jpg') as img:
    output = ascii_magic.from_image(img, columns=100)
```

## to_terminal()

Initializes Colorama, which is required on Windows for displaying art in terminal mode, and prints the input. It's the same as doing ```colorama.init()``` before running ```print()```.

```python
ascii_magic.to_terminal(input: str) -> None
```

## quick_test()

Runs ascii_magic with a random Unsplash picture with the default parameters and prints it to the terminal.

```python
ascii_magic.quick_test() -> None
```

# Licence

Copyright (c) 2020 Leandro Barone.

Usage is provided under the MIT License. See LICENSE for the full details.