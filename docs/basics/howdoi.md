# How do I ...?

This page collects examples on how to perform simple tasks in VapourSynth.
It's mostly about how to shuffle clips around and how to convert between formats,
not about actual filtering.

Many of the things here can also be found on their respective documentation pages
(e.g. VapourSynth's [Python Reference](http://www.vapoursynth.com/doc/pythonreference.html)
and [Function Reference](http://www.vapoursynth.com/doc/functions.html)), so go there
if you need more details on any function.
The point of this page is to make the barrier to entry lower.

Some of the entries here list more than one way to achieve a certain goal.
For example, they may show both a way using only standard VapourSynth functions,
and a way using JET wrappers.
Apart from just providing multiple options, this is also done to show that many
of the wrappers around simple operations are not magic, and really just call
standard functions under the hood.
In the end, which method you use is up to you.
Unless otherwise stated, there isn't any relevant difference between them,
except for one option being easier to write than the other.

### How do I cut off frames at the beginning/end of a clip?


=== "Python Syntax"
    Clips can be cut by simply slicing them like Python lists:

    ```py3
    clip_cut = clip[10:]    # Cut off 10 frames at the start
    clip_cut = clip[:-10]   # Cut off 10 frames at the end

    # Start at frame 10 of the clip, and go up until frame 999.
    # Frame 1000 is not included.
    clip_cut = clip[10:1000]
    ```

=== "Trim filter"
    Just like everything else, cutting clips can also be done via a filter invocation.
    There's no real use for this
    (unless you're doing fancy things like passing around filter functions as objects,
    in which case you probably don't need to read this page),
    except for knowing that slicing is not magic.

    Note that the [Trim filter](http://www.vapoursynth.com/doc/functions/video/trim.html), unlike slicing, is inclusive.

    ```py3
    clip_cut = clip.std.Trim(first=10)    # Cut off 10 frames at the start
    clip_cut = clip.std.Trim(length=clip.num_frames - 10)   # Cut off 10 frames at the end

    # Start at frame 10 of the clip, and go up until frame 1000,
    # which is included.
    clip_cut = clip.std.Trim(first=10, last=1000)
    ```

### How do I cut out a section of frames from a clip?
See above.

### How do I join multiple clips together?

Clips can be joined by simply using the `+` operator in Python:
```py3
clip_joined = clip1 + clip2 + clip3
```
If you need to join many clips together, or have a list of clips,
it may be simpler to use [`core.std.Splice`](http://www.vapoursynth.com/doc/functions/video/splice.html):
```py3
clip_joined = core.std.Splice([clip1, clip2, clip3])
```

### How do I stack two clips on top of one another?
This can be done with [`core.std.StackVertical`](http://www.vapoursynth.com/doc/functions/video/stackvertical_stackhorizontal.html).
But chances are that you are asking this because you want to compare the clips with one another.
Unless you want to check if the clips are synced, chances are you want to use [multiple output nodes](#how-do-i-compare-multiple-clips) to compare them instead.

### How do I interleave two clips?
This can be done with [`core.std.Interleave`](http://www.vapoursynth.com/doc/functions/video/interleave.html).
But chances are that you are asking this because you want to compare the clips with one another.
Unless you want to check if the clips are synced, chances are you want to use [multiple output nodes](#how-do-i-compare-multiple-clips) to compare them instead.

### How do I compare multiple clips?
Set the clips you want to compare as outputs.
Then, open the script in vs-preview (see the [Setup] page)
and use the number keys to switch between outputs.

=== "vs-tools"
    ```py3
    from vstools import set_output

    set_output(clip1)
    set_output(clip2)
    ```

=== "Vanilla VS"
    ```py3
    clip1.set_output(0)
    clip2.set_output(1)
    ```

### How do I name my outputs?
```py3
from vstools import set_output

set_output(clip1, "My first clip")
set_output(clip2, "My second clip")
```

Note that the names will only show up in vs-preview and not in other previewers.

### How do I preview a VFR clip with the correct frame rate(s)?
Pass a timecodes file to `set_output`:

```py3
from vstools import set_output

set_output(clip, timecodes="timecodes.txt")
```

You can also pass a `Timecodes` object (which you could generate at runtime, or modify):
```py3
from vstools import set_output, Timecodes

timecodes = Timecodes.from_file("timecodes.txt")
set_output(clip, timecodes=timecodes)
```

You can generate a `Timecodes` object from a clip's per-frame `_DurationNum` and `_DurationDen` properties,
but note that this is very slow since it needs to go through the entire clip.
One useful method is to generate them once and then save them to a file.
```py3
import os.path
from vstools import set_output, Timecodes

TIMECODES_NAME = "timecodes.txt"

if not os.path.isfile(TIMECODES_NAME):
    timecodes = Timecodes.from_clip(clip)
    timecodes.to_file(TIMECODES_NAME)

timecodes = Timecodes.from_file(TIMECODES_NAME)
set_output(clip, timecodes=timecodes)
```
Remember to regenerate your timecodes file whenever the clip's frames or frame rate change.
With the above code, this can be done by just deleting the timecodes file.

### How do I get the luma/chroma of a clip?
=== "vs-tools"
    ```py3
    from vstools import get_y, get_u, get_v, split, plane

    y = get_y(clip)     # Luma
    u = get_u(clip)     # First chroma plane
    v = get_v(clip)     # Second chroma plane

    # Alternatively, you can use `split`:
    y, u, v = split(clip)

    # Or, you can use the `plane` function:
    y = plane(clip, 0)
    u = plane(clip, 1)
    v = plane(clip, 2)
    ```
    If you want to split an RGB clip instead, you'll need to use the equivalent `get_r`, `get_g`, `get_b` functions.

=== "Vanilla VS"
    ```py3
    y = clip.std.ShufflePlanes(planes=0, colorfamily=vs.GRAY)   # Luma
    u = clip.std.ShufflePlanes(planes=1, colorfamily=vs.GRAY)   # First chroma plane
    v = clip.std.ShufflePlanes(planes=2, colorfamily=vs.GRAY)   # Second chroma plane

    # Or, to get all three planes:
    y, u, v = clip.std.SplitPlanes()
    ```

If you only want to *see* the individual planes of a clip,
and not process them, you may want to use vs-preview's "Split Planes" plugin instead (see the [Setup] page).

### How do I combine luma and chroma into a clip, or replace planes of a clip?
=== "vs-tools"
    ```py3
    from vstools import join

    # Join luma and chroma
    joined = join(y, u, v)

    # Replace chroma in a YUV clip
    clip_replaced = join(clip, u, v)

    # Replace luma in a YUV clip
    clip_replaced = join(y, clip)
    ```

=== "Vanilla VS"
    ```py3
    # Join luma and chroma
    joined = core.std.ShufflePlanes(clips=[y, u, v], planes=[0, 0, 0], colorfamily=vs.YUV)

    # Replace chroma in a YUV clip
    clip_replaced = core.std.ShufflePlanes(clips=[clip, u, v], planes=[0, 0, 0], colorfamily=vs.YUV)

    # Replace luma in a YUV clip
    clip_replaced = core.std.ShufflePlanes(clips=[y, clip, clip], planes=[0, 1, 2], colorfamily=vs.YUV)
    ```

### How do I change a clip's bit depth?
=== "vs-tools"
    ```py3
    from vstools import depth

    clip_i16 = depth(clip, 16)
    clip_float = depth(clip, 32)
    ```

=== "Vanilla VS"
    ```py3
    clip_i16 = clip.resize.Point(format=clip.format.replace(bits_per_sample=16, sample_type=vs.INTEGER))
    clip_float = clip.resize.Point(format=clip.format.replace(bits_per_sample=32, sample_type=vs.FLOAT))
    ```

Note that the vanilla VS version does not dither by default, while `vstools.depth` does dither when necessary.
With both versions the dither type can be set in a parameter.

### How do I retag a clip's color matrix/color range/etc?
Retagging only changes the metadata (here in the form of frame properties) without changing any of the pixel values.
(But of course filters called on this clip may behave differently based on the metadata, which is the entire point.
In particular your clip will display differently in vs-preview, even though the pixel values are the same.)

=== "vs-tools"
    ```py3
    from vstools import Matrix, ColorRange

    clip_retagged = Matrix.BT601.apply(ColorRange.FULL.apply(clip))
    ```

=== "Vanilla VS"
    ```py3
    clip_retagged = clip.std.SetFrameProps(_Matrix=vs.MATRIX_BT601, _Range=vs.RANGE_FULL)
    ```

### How do I convert a clip's color matrix/color range/etc?
Tag your clip as the source matrix/range/etc and use the [`core.resize`](http://www.vapoursynth.com/doc/functions/video/resize.html)
function to convert it to the target matrix/range/etc.

Converting color matrix/range/etc will change the pixel values as well as the metadata,
so the resulting clip will look the same in a previewer (except for subtle differences due to dithering, etc)
even though the pixel values are different.

```py3
from vstools import Matrix, ColorRange  # You can also use Vanilla VS, see above

# Convert a clip from the BT601 matrix to the BT709 matrix
clip_converted = clip.resize.Point(Matrix.BT601.apply(clip), matrix=Matrix.BT709)

# Convert a clip from limited range to full range
# Note that you cannot use the ColorRange enum for the `range` argument here!
clip_converted = clip.resize.Point(ColorRange.LIMITED.apply(clip), range=1)
```
Note that the resizing does not dither by default. That does not mean you *should* dither
(usually it's better practice to do most of your filter chain with float clips, and then dither down at the end),
but you should be aware of it.

Also note that converting color matrix, transfer, or primaries (but not range or chroma location)
requires upscaling chroma to the luma's size.
The above code assumes a YUV444 clip;
it will *work* with YUV420 clips, but the output will not be good since it uses Point to resize.
However, you shouldn't simply replace `Point` with another scaler like `Lanczos`,
since that scaler would be used for both upscaling and downscaling.
It's better to explicitly upscale to YUV444 first (using, say, `Lanczos`), convert the color space,
and then eventually downscale back to YUV420 again (using, say, Hermite, i.e. `Bicubic` with b=c=0).

!!! warning
    Do not use the `matrix_in`/`range_in`/etc family of arguments to convert color spaces.
    Frame properties, when present, take precedence over these arguments, which can lead to very unexpected behavior.
    Hence you should instead be overwriting the frame properties, as done in the snippet above.

!!! warning
    Color range needs special treatment here, as shown in the above snippet.
    The meaning of the values `0` and `1` is flipped between the `_ColorRange` frame property and
    the `core.resize` function.
    In the frame property, `0` means full and `1` means limited ([docs](http://www.vapoursynth.com/doc/apireference.html#reserved-frame-properties)),
    but in `core.resize` it's the other way around ([docs](http://www.vapoursynth.com/doc/functions/video/resize.html)).

Alternatively, you can use [fmtconv](https://amusementclub.github.io/fmtconv/doc/fmtconv.html).

### How do I apply a filter to only some frames in the clip?
Unless the filter is a temporal one and you specifically want it to *only* get your selected frames as an input,
the simplest way is to apply the filter to the entire clip and then replace the desired frames afterwards:

```py3
filtered = clip.std.BoxBlur()

# only blur frames 10 through 19 (excluding frame 20)
partially_filtered = clip[:10] + filtered[10:20] + clip[20:]
```

For more convenience, you can use the `replace_ranges` function to avoid having to manually slice all the clips.
This can also be more performant when you have many ranges to replace.

```py3
from vstools import replace_ranges

# Replace frames 10 through 19, including 19. `replace_ranges` ranges are inclusive, unless you set `exclusive=True`.
MY_FRAME_RANGES = [(10, 19)]

# You could also use multiple ranges, and you can use None to denote the left/right end of the clip.
# Check the function docstring for more info.
# This would replace frames 10 through 19 and all frames starting from frame 200.
# MY_FRAME_RANGES = [(10, 19), (200, None)]

partially_filtered = replace_ranges(clip, filtered, MY_FRAME_RANGES)
```

Don't worry, even though you give the entire `clip` as an input to your filter,
the filter will not actually run on the frames not added to `partially_filtered`
when you set `partially_filtered` (or another clip based on it) as an output.
Filters are only run on frames when the frame is requested.

### How do I decide at runtime whether to apply a filter or not?
Unless you want to write your own plugin, the way to do this is with [`FrameEval`](http://www.vapoursynth.com/doc/functions/video/frameeval.html):

For example, to blur all frames whose average luma is larger than 0.5 (assume the clip is a float clip):
```py3
blurred = clip.std.BoxBlur()
stats = clip.std.PlaneStats()

def blur_some_frames(n: int, f, clip: vs.VideoNode, blurred: vs.VideoNode) -> vs.VideoNode:
    if f.props["PlaneStatsAverage"] > 0.5:
        return blurred
    return clip

partially_blurred = clip.std.FrameEval(
    eval=partial(blur_some_frames, clip=clip, blurred=blurred),
    prop_src=stats
    )
```

Try not to instantiate filters inside of the per-frame function, if possible.
Note how the above snippet creates the `blurred` and `stats` clips outside of the function,
and only references them inside the function.
This makes the filter only be applied once, instead of once for every frame.
Of course you cannot do this if the filter parameters need to vary per frame.
In that case, you need to be very careful when your filter's instantiation is very resource-heavy.

### How do I apply a filter to only a certain section of the picture?
In general this depends very strongly on what filter you're using and what you want to achieve.
One common answer, however, is to apply the filter to the entire frame and do a masked merge with the original clip.

For example, to only blur a certain rectangle in the frame:
```py3
from vsmasktools import squaremask

# a 200x200 rectangle whose top left corner is at (500, 500)
mask = squaremask(clip, 200, 200, 500, 500)

blurred = clip.std.BoxBlur()

partially_blurred = core.std.MaskedMerge(clip, blurred, mask)
```
In fact, for the specific purpose of a square mask there exists an even simpler wrapper function
(but I showed you the longer snippet to illustrate the general process):
```py3
from vsmasktools import replace_squaremask

blurred = clip.std.BoxBlur()
partially_blurred = replace_squaremask(clip, blurred, (200, 200, 500, 500))
```
Other ways to build masks include:
- Manually building a square mask using a `core.std.BlankClip` followed by `core.std.AddBorders`.
  There's no real reason to do this except to understand how `squaremask` might work internally.
- Manually building a mask with `core.akarin.Expr`, using an expression that computes the mask value based on the position.
- Building a mask using certain filters (e.g. edge masks) or manual expressions based on the pixel values
- Manually drawing a mask in an image editor and importing it from a file
- Drawing a mask using subtitle drawings in [Aegisub](https://aegisub.org), and rendering the resulting
  subtitle line using the [`core.sub`](https://github.com/vapoursynth/subtext/blob/master/docs/subtext.rst) plugin

### How do I access or modify a frame's content in Python?
Unless you know what you're doing, chances are that you shouldn't be doing this.
Modifying frame contents in Python is slow and not the way VapourSynth is intended to be used.
You should instead see if there is a plugin that applies the filter you want to apply,
or write such a plugin if there isn't.
If you want to apply some custom formula to a frame's pixels,
you can use the [`core.std.Expr`](http://www.vapoursynth.com/doc/functions/video/expr.html)
or the more powerful third-party [`core.akarin.Expr`](https://github.com/Jaded-Encoding-Thaumaturgy/akarin-vapoursynth-plugin?tab=readme-ov-file#expr) functions.

That said, accessing frame data from Python *can* be useful when you're trying out some new filter idea
and want to prototype using tools like numpy.

To read a frame's contents into a numpy array:
```py3
import numpy as np

# Get the first plane of frame 100 as a numpy array of shape (clip.height, clip.width)
data = np.asarray(clip.get_frame(100)[0])
```

To modify a frame's contents:
```py3
def modify(f, n):
    # Do the necessary imports inside of the function.
    # Doing them globally can cause issues in some scenarios,
    # since they may be dropped before the function is executed
    import numpy as np

    src = np.asarray(f[1][0])

    # The dimensions and dtype of `res` need to match the dimensions and format of `blank` below
    res = np.zeros((your_target_height, your_target_width), dtype=np.float32)

    # Write some data into `res` here

    dst = f[0].copy()
    np.copyto(np.asarray(dst[0]), res)
    return dst

# Set up a blank clip with your desired output width/height/format
# (which can differ from your input clip's format)
blank = clip.std.BlankClip(your_target_height, your_target_width, format=vs.GRAYS)
result = core.std.ModifyFrame(blank, [blank, clip], modify)
```

### How do I remove artifacts from a video without being too destructive?
Very carefully.

[setup]: ./setup.md
