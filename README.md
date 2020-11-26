# ASCII Magic

Python package that converts images into ASCII art. Requires colorama and PIL.

## Basic usage

```python
import ascii_magic
output = ascii_magic.from_image_file('picture.jpg')
ascii_magic.to_terminal(output)
```

## Available functions

### from_image_file()

Converts an image file into ASCII art with terminal color codes.

```python
from_image_file(
    path:str,
    columns:int=120,
    width_ratio:float=2.5,
    char:str=None
) -> str
```

- path => a PIL-compatible file, such as picture.jpg
- columns (optional) => the number of characters per row, more columns = wider art
- pixel_width (optional) => ASCII characters are not square, so this adjusts the width to height ratio
- char (optional) => instead of using many different ASCII glyphs, you can use a single one, such as '#'

Example:

```python
from_image_file('images/1.jpg', columns=100, width_ratio=2.6, char='@')
```

### from_image()

As above, but using an image loaded with Pillow.

```python
from_image(
    img:Image,
    # ... as above
) -> str
```

- img => PIL image

Example:

```python
import ascii_magic
from PIL import Image
img = Image.open('images/1.jpg')
ascii_art = ascii_magic.from_image_file(img, columns=100)
img.close()
```

### to_terminal()

Initializes colorama (which is required on Windows) and prints ASCII art to the terminal. It's the same as doing ```colorama.init()``` before printing normally.

```python
to_terminal(ascii_art:str) -> None
```

## Licence

Copyright (c) 2020 Leandro Barone.

Usage is provided under the MIT License. See LICENSE for the full details.