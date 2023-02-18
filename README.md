# ASCII Magic

Python package that converts images into ASCII art for terminals and HTML. Thanks to [Colorama](https://github.com/tartley/colorama) it's compatible with the Windows terminal.

Code based on [ProfOak's Ascii Py](https://github.com/ProfOak/Ascii_py/).

# Changelog

### v2.0
- Complete rewrite, only supports OOP, no longer compatible with 1.x
- Added support for foreground color
- Test suite compatible with PyTest

### v1.6
- OOP functionality
- to_file()

# How to install

    pip install ascii_magic

# Quickstart

```python
import ascii_magic

my_art = ascii_magic.from_image('images/moon.jpg')
my_art.to_terminal()
```

Result:

![ASCII Magic example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_moon.png)


# Available functions

## quick_test()

Loads a random Unsplash picture with the default parameters and prints it to the terminal, allowing you to verify in a single line of code that everything is running O.K.

```python
ascii_magic.quick_test() -> None
```

## from_image()

Creates an ```AsciiArt``` object from an image file.

```python
from_image(path: str) -> AsciiArt
```

Parameters:

- ```path```: an image file compatible with Pillow, such as a jpeg or png

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_art.to_terminal(columns=200, back=ascii_magic.Back.BLUE)
```

Result:

![ASCII Magic TERMINAL mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_blue.png)

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_art.to_html_file('ascii_art.html', columns=200, width_ratio=2)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_html.png)

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_art.to_terminal(columns=200, monochrome=True)

```

Result:

![ASCII Magic ASCII mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_ascii.png)

## from_url()

Creates an ```AsciiArt``` object from an image URL. Raises an ```urllib.error.URLError``` if something goes wrong while requesting the image, but you can also catch it as an ```OSError``` if you don't want to import ```urllib``` into your project.

```python
from_url(url: str) -> AsciiArt
```

Parameters:

- ```url```: an URL which will be loaded via urllib (supports redirects)

Example:

```python
import ascii_magic

try:
    my_art = ascii_magic.from_url('https://source.unsplash.com/800x600?nature')
except OSError as e:
    print(f'Could not load the image, server said: {e.code} {e.msg}')
```

## from_clipboard()

Creates an ```AsciiArt``` object from the contents of the clipboard. Raises a ```OSError``` if the clipboard doesn't contain an image. Requires [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) under Linux.

```python
from_clipboard() -> AsciiArt
```

Example:

```python
import ascii_magic

try:
    my_art = ascii_magic.from_clipboard()
except OSError:
    print('The clipboard does not contain an image')
```

## from_pillow_image()

Creates an ```AsciiArt``` object from an image object created with Pillow. This allows you to handle the image loading yourself.

```python
from_pillow_image(img: PIL.Image) -> AsciiArt
```

Parameters:

- ```img```: an image object created with Pillow

Example:

```python
import ascii_magic
from PIL import Image

img = Image.open('images/lion.jpg')
my_art = ascii_magic.from_pillow_image(img)
```


# The AsciiArt object

An ```AsciiArt``` object created by the functions explained above has the following methods: ```to_ascii()```, ```to_terminal()```, ```to_file()```, ```to_html()``` and ```to_html_file()```. These methods allow you to display the ASCII art in different ways.


## AsciiArt.to_ascii()

Returns a string containing the art and, by default, control characters that allows most terminals (also known as shells) to display color.

```python
AsciiArt.to_ascii(
    columns: int = 120,
    width_ratio: float = 2.2,
    char: Optional[str] = None,
    monochrome: bool = False,
    back: Optional[Back] = None,
    front: Optional[Front] = None
) -> str
```

Parameters:

- ```columns (int, optional)```: the number of characters per row, more columns = wider art
- ```width_ratio (float, optional)```: ASCII characters are not squares, so this adjusts the width to height ratio during generation
- ```char (str, optional)```: instead of using many different ASCII glyphs, you can use a single one, such as '#'
- ```monochrome (bool, optional)```: if set to True, disables the usage of control characters that display color
- ```back (enum, optional)```: sets the background color to one of:
  - ```ascii_magic.Back.BLACK```
  - ```ascii_magic.Back.RED```
  - ```ascii_magic.Back.GREEN```
  - ```ascii_magic.Back.YELLOW```
  - ```ascii_magic.Back.BLUE```
  - ```ascii_magic.Back.MAGENTA```
  - ```ascii_magic.Back.CYAN```
  - ```ascii_magic.Back.WHITE```
- ```front (enum, optional)```: overrides the foreground color with one of:
  - ```ascii_magic.Front.BLACK```
  - ```ascii_magic.Front.RED```
  - ```ascii_magic.Front.GREEN```
  - ```ascii_magic.Front.YELLOW```
  - ```ascii_magic.Front.BLUE```
  - ```ascii_magic.Front.MAGENTA```
  - ```ascii_magic.Front.CYAN```
  - ```ascii_magic.Front.WHITE```

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_output = my_art.to_ascii(columns=200, back=ascii_magic.Back.BLUE)
print(my_output)
```

Result:

![ASCII Magic TERMINAL mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_blue.png)


## AsciiArt.to_terminal()

Identical to ```AsciiArt.to_ascii()```, but it also does a ```print()``` of the result, saving you one line of code ;)

## AsciiArt.to_file()

Identical to ```AsciiArt.to_ascii()```, but it also saves the result to a text file.

```python
AsciiArt.to_file(
    path: str,
    # ... same parameters as AsciiArt.to_ascii()
) -> str
```
Parameters:

- ```path (str)```: the output file path

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_art.to_file('lion.txt', monochrome=True)
```

## AsciiArt.to_html()

Generates HTML markup of the ASCII art. Uses the same parameters as ```AsciiArt.to_ascii()```, except ```back``` and ```front``` colors. By default the HTML ASCII art is generated with a 16-bit palette (16 million colors).

```python
AsciiArt.to_html(
    full_color: bool = True,
    # ... same parameters as AsciiArt.to_ascii(), except back and front colors
) -> str
```

Parameters:

- ```full_color (bool, optional)```: if set to False, limits color palette to 8 colors

Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
my_html_markup = ascii_magic.to_html(columns=200)
```

Result:

![ASCII Magic HTML mode example](https://raw.githubusercontent.com/LeandroBarone/python-ascii_magic/master/example_lion_html.png)


## AsciiArt.to_html_file()

Identical to ```AsciiArt.to_html()```, but it also saves the markup to a barebones HTML file inside a ```<pre>``` tag with a bunch of default CSS styles.

```python
AsciiArt.to_html(
    path: str,
    styles: str = '...',  # See description below
    additional_styles: str = '',
    auto_open: bool = False
    # ... same parameters as AsciiArt.to_html()
) -> str
```

Parameters:

- ```path (str)```: the output file path
- ```styles (str)```: a string with a bunch of CSS styles for the ```<pre>``` element, by default:
  - display: inline-block;
  - border-width: 4px 6px;
  - border-color: black;
  - border-style: solid;
  - background-color: black;
  - font-size: 8px;
- ```additional_styles (optional)```: use this to add your own CSS styles without removing the default ones
- ```auto_open (optional)```: if True, ```webbrowser.open()``` will be called on the HTML file


Example:

```python
import ascii_magic

my_art = ascii_magic.from_image('images/lion.jpg')
ascii_magic.to_html_file('lion.html', columns=200, additional_styles='background: #222;', auto_open=True)
```

# Licence

Copyright (c) 2020 Leandro Barone.

Usage is provided under the MIT License. See LICENSE for the full details.