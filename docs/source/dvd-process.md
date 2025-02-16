# Direct DVD processing

When working with DVDs,
you have two main options:
remuxing the content into separate files
(as covered in the [DVD remuxing guide](./dvd-remux.md)),
or parsing and processing the ISO directly.

Using `vs-source` to parse ISOs directly
lets you load [DVD components](./dvd-remux.md#understanding-dvd-structure)
like titles, angles and chapters
straight into VapourSynth,
skipping the remuxing process entirely.
This is the ideal approach
if you only need to process the video
and don't require the remuxed files.

Note that this method is strictly for processing.
You cannot use it to remux titles into separate files.
If you need remuxed files,
please refer to the [DVD remuxing guide](./dvd-remux.md) instead.

To install it,
run the following command:

```bash
pip install vssource
```

Once you have installed it,
you can use the following code
to parse a DVDISO:

```python
from vssource import IsoFile

iso = IsoFile('./src/ゼロの使い魔_01.ISO')
```

Printing this IsoFile object
will give you all the information
it was able to parse.

??? example "Example IsoFile output"

    ```py
    Path: C:\Users\light\Encoding\Kaleido-subs\Zero no Tsukaima\S01\src\ゼロの使い魔_01.ISO
    Mount: None
    Title: 01
      nbr vobid start localstart localend duration
      01 (1, 1) start=0:00:00 local=0:00:00 end=0:00:46 duration=0:00:46
      02 (1, 2) start=0:00:46 local=0:00:46 end=0:02:15 duration=0:01:29
      03 (1, 3) start=0:02:15 local=0:02:15 end=0:12:46 duration=0:10:31
      04 (1, 4) start=0:12:46 local=0:12:46 end=0:21:52 duration=0:09:06
      05 (1, 5) start=0:21:52 local=0:21:52 end=0:23:21 duration=0:01:29
      06 (1, 6) start=0:23:21 local=0:23:21 end=0:23:37 duration=0:00:16
      07 (1, 7) start=0:23:37 local=0:23:37 end=0:24:32 duration=0:00:55
      08 (1, 8) start=0:24:32 local=0:24:32 end=0:26:01 duration=0:01:29
      09 (1, 9) start=0:26:01 local=0:26:01 end=0:37:18 duration=0:11:17
      10 (1, 10) start=0:37:18 local=0:37:18 end=0:45:29 duration=0:08:11
      11 (1, 11) start=0:45:29 local=0:45:29 end=0:46:58 duration=0:01:29
      12 (1, 12) start=0:46:58 local=0:46:58 end=0:47:13 duration=0:00:15
      13 (1, 19) start=0:47:13 local=0:47:13 end=0:47:14 duration=0:00:01
    Title: 02
      nbr vobid start localstart localend duration
      01 (1, 13) start=0:00:00 local=0:00:00 end=0:00:05 duration=0:00:05
      02 (1, 14) start=0:00:05 local=0:00:05 end=0:02:05 duration=0:02:00
      03 (1, 15) start=0:02:05 local=0:02:05 end=0:03:34 duration=0:01:29
      04 (1, 16) start=0:03:34 local=0:03:34 end=0:05:03 duration=0:01:29
      05 (1, 17) start=0:05:03 local=0:05:03 end=0:05:33 duration=0:00:30
      06 (1, 18) start=0:05:33 local=0:05:33 end=0:06:04 duration=0:00:31
      07 (1, 19) start=0:06:04 local=0:06:04 end=0:06:05 duration=0:00:01
    Title: 03
      nbr vobid start localstart localend duration
      01 (1, 1) start=0:00:00 local=0:00:00 end=0:00:05 duration=0:00:05
      02 (1, 2) start=0:00:05 local=0:00:05 end=0:00:12 duration=0:00:07
      03 (1, 3) start=0:00:12 local=0:00:12 end=0:00:19 duration=0:00:07
      04 (1, 4) start=0:00:19 local=0:00:19 end=0:00:26 duration=0:00:07
      05 (1, 5) start=0:00:26 local=0:00:26 end=0:00:33 duration=0:00:07
      06 (1, 6) start=0:00:33 local=0:00:33 end=0:00:40 duration=0:00:07
      07 (1, 7) start=0:00:40 local=0:00:40 end=0:00:47 duration=0:00:07
      08 (1, 8) start=0:00:47 local=0:00:47 end=0:00:54 duration=0:00:07
      09 (1, 9) start=0:00:54 local=0:00:54 end=0:01:01 duration=0:00:07
      10 (1, 10) start=0:01:01 local=0:01:01 end=0:01:16 duration=0:00:15
      11 (1, 11) start=0:01:16 local=0:01:16 end=0:01:31 duration=0:00:15
      12 (1, 12) start=0:01:31 local=0:01:31 end=0:01:46 duration=0:00:15
      13 (1, 13) start=0:01:46 local=0:01:46 end=0:02:01 duration=0:00:15
      14 (1, 14) start=0:02:01 local=0:02:01 end=0:02:16 duration=0:00:15
      15 (1, 15) start=0:02:16 local=0:02:16 end=0:02:31 duration=0:00:15
      16 (1, 16) start=0:02:31 local=0:02:31 end=0:02:46 duration=0:00:15
      17 (1, 17) start=0:02:46 local=0:02:46 end=0:03:01 duration=0:00:15
      18 (1, 18) start=0:03:01 local=0:03:01 end=0:03:16 duration=0:00:15
      19 (1, 19) start=0:03:16 local=0:03:16 end=0:03:31 duration=0:00:15
      20 (1, 20) start=0:03:31 local=0:03:31 end=0:04:02 duration=0:00:31
      21 (1, 21) start=0:04:02 local=0:04:02 end=0:04:03 duration=0:00:01
    ```

You can get a specific title
using the following method:

```python
title = iso.get_title(1)
```

This will return a `Title` dataclass,
which contains a `vs.VideoNode`
of the title,
as well as a list of integers
representing the chapter points
in frames.

```python
@dataclass
class Title:
    video: vs.VideoNode
    chapters: list[int]
    ...
```

You can preview a title
using `vs-preview`
as you would normally.
Every `Title` object
has a `preview` method
that will set an output
for both the video
and the audio track.

```py
from vssource import IsoFile

iso = IsoFile('src/ゼロの使い魔_01.ISO')
title = iso.get_title(1)
title.preview()
```

![Preview of the first title](./img/dvd-process/isofile/preview-full-title.png)

You can also split a title
at chapter points
using the `split_at` method
and preview each split
using the same `preview` method.
This will be most useful
for titles that contain multiple episodes.

```py
from vssource import IsoFile

iso = IsoFile('src/ゼロの使い魔_01.ISO')
title = iso.get_title(1)
title.preview(title.split_at([7]))
```

![Dropdown menu with output nodes](./img/dvd-process/isofile/preview-split-title-nodes.png)

!!! info "Documentation"

    For more in-depth information
    on the `IsoFile` class
    and how to use it,
    please refer to
    the [vs-source source code](https://github.com/Jaded-Encoding-Thaumaturgy/vs-source/blob/master/vssource/formats/dvd/IsoFile.py).


