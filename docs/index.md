# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.


## Codeblock

```py
from NKCommon import *

no_filter = []
credit = []


AMZN = FileInfo(GlobSearch(f"Ninja*S01E{ep}*AMZN CBR*.mkv"), trim=(96, None))
HMAX = FileInfo(GlobSearch(f"Ninja*S01E{ep}*.HMAX*VARYG*.mkv"), force_bs=True)
src: vs.VideoNode = HMAX.init().std.AssumeFPS(fpsnum=24000, fpsden=1001)[98:]
```

## Tabs

=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b

## File embed sample

Also see [this documentation](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/) on more features related to this.

```py title="test.py"
--8<-- "./docs/code/test.py"
```