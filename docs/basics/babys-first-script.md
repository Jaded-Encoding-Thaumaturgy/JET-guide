# Baby's first script

Some basics that might be useful when writing your first script.

## Index a video

### Available indexers to consider

- [bestsource](https://github.com/vapoursynth/bestsource)[^1]<br>
    The most accurate but slowest indexer.
- [lsmas](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works/)[^2]<br>
    Fast, mostly reliable enough.
- [ffms2](https://github.com/FFMS/ffms2)[^3]<br>
    With the latest version pretty much on par with lsmas and possibly even faster.

DGIndexNV is also technically something you can use, but recent versions have been buggy and it's restricted to Nvidia GPUs.

!!! warning "DVDs"
    For DVDs you can skip the following Usage section and simply read the `IsoFile` usage section in the [vs-source readme](https://github.com/Jaded-Encoding-Thaumaturgy/vs-source?tab=readme-ov-file#usage).<br>
    I've been told `dvdsrc` also should set the metadata correctly but ymmv.

#### Usage

=== "Vanilla VS"
    ```py
    from vstools import vs, core

    # bestsource
    clip = core.bs.VideoSource(R"path/to/file.mkv")

    # lsmas
    clip = core.lsmas.LWLibavSource(R"path/to/file.mkv")

    # ffms2
    clip = core.ffms2.Source(R"path/to/file.mkv")
    ```
=== "vs-source"
    ```py
    from vssource import BestSource, LSMAS, source

    # bestsource
    clip = BestSource.source(R"path/to/file.mkv")

    # lsmas
    clip = LSMAS.source(R"path/to/file.mkv")

    # Automatic indexer selection
    # usually defaults to lsmas while previewing with vs-preview and bestsource when otherwise
    clip = source(R"path/to/file.mkv")
    ```
=== "vs-muxtools"
    ```py
    from vsmuxtools import src_file, FileInfo # same thing as src_file

    # lsmas
    JPBD = FileInfo(R"path/to/file.mkv", force_lsmas=True)

    # bestsource
    JPBD = FileInfo(R"path/to/file.mkv", force_bs=True)

    # Automatic indexer selection
    # usually defaults to lsmas while previewing with vs-preview and bestsource when otherwise
    JPBD = FileInfo(R"path/to/file.mkv")

    # Actually getting the clip
    clip = JPBD.src
    # Or with trims, if defined
    clip = JPBD.src_cut
    ```

### Getting Comfortable with vs-preview

If you've followed the [installation instructions][installation],
you should have `vs-preview` installed and should be able to preview your video file.
Here are a few things you can try out:

-  Press Space to play or pause
-  Click around in the timeline bar below the video display to step around the video
-  Ctrl+Scroll to zoom and Click+Drag to pan around the displayed image
-  Click the "Pipette" button at the bottom and look at the values at the bottom changing while you move your mouse around the image.
-  Click the "Benchmark" button at the bottom and click "Run" to find out how fast your VapourSynth script runs.
   At the moment, your script just loads a video, so it should be fairly fast,
   but in the future your scripts might contain more complex filtering, and knowing how fast or slow your filtering is will be more important.
-  Click the "Comp" button at the bottom and click "Start Upload".
   Once the upload is done, find the box containing a `slow.pics` link and press the button next to it to copy that link to your clipboard.
   Open that link in your browser: You'll get a `slow.pics` comparison of random frames in your video.
   If your script has multiple outputs, the comparison will show all output nodes.
-  Move your mouse to the very right of vs-preview's window and drag the bar there to the left.
   This opens the plugins panel, which contains one tab for each vs-preview plugin.
   First, open the "Frame Props" tab and have a look at the values there.

   Then, open the "Split Planes" tab.
   This shows the individual planes of your video.
   For your average video clip, this will consist of one luma plane and two chroma planes with half the width and height.
   You can press Ctrl+A to unlock the split planes view,
   which will allow you to freely zoom and pan around in the view like you would on the normal video.

## Ensure video metadata

Most functions that resample/resize a video require metadata to be present.<br>
Most videos you download and the majority of BDs are untagged so this is often a necessary step. (And really also just good practice)

**Indexing via `vs-source` will automatically try to guess via resolution.**

=== "vstools"
    ```py
    from vstools import initialize_clip, Matrix, Primaries, Transfer

    # Will automatically try to guess via resolution and upsample to 16 bit.
    clip = initialize_clip(clip)

    # You can also set everything manually with the enums in vstools/vs

    # For most HD sources
    clip = initialize_clip(clip, matrix=Matrix.BT709, primaries=Primaries.BT709, transfer=Transfer.BT709)

    # For most NTSC DVDs
    clip = initialize_clip(clip, matrix=Matrix.SMPTE170M, primaries=Primaries.SMPTE170M, transfer=Transfer.BT601)
    ```
=== "vs-muxtools"
    ```py
    # init() and init_cut() just call initialize_clip internally and accept the same arguments.

    # Will automatically try to guess via resolution and upsample to 16 bit.
    clip = JPBD.init_cut()

    # You can also set everything manually with the enums in vstools/vs
    from vstools import Matrix, Primaries, Transfer

    # For most HD sources
    clip = JPBD.init_cut(matrix=Matrix.BT709, primaries=Primaries.BT709, transfer=Transfer.BT709)

    # For most NTSC DVDs
    clip = JPBD.init_cut(matrix=Matrix.SMPTE170M, primaries=Primaries.SMPTE170M, transfer=Transfer.BT601)
    ```

## Output the clips

Technically all you need is `clip.set_output(0)` but vstools/vspreview provide a helper function with more features.

```py
from vspreview import set_output

# Naming the nodes in vspreview
set_output(clip, "Name shown in vspreview")

# Making a clip ineligible for comparisons in vspreview
set_output(clip, disable_comp=True)
```

If you want to only output clips when previewing and do other stuff, like [encoding with vs-muxtools](https://muxtools.vodes.pw/guide/encode-video/), you can use the vspreview helper function like this

```py
from vspreview import is_preview, set_output

if is_preview():
    set_output(src, "JPBD")
    set_output(clip, "Filtered")
else:
    ...
```

## Other notable stuff

### Affinity and memory allocation

!!! tip
    It is highly recommended to at least set the cache size vapoursynth is allowed to use.<br>
    This should ideally always be done as the **first (non-import) step** in your script.

You can set the cache size like this:

=== "vstools (recommended)"
    ```py
    from vstools import vs, core

    core.set_affinity(max_cache=22000) # This value is in MB
    ```

=== "Vanilla VS"
    ```py
    from vstools import vs, core

    core.max_cache_size = 22000 # This value is in MB
    ```

Threads and affinity allocation is less "figured out" and may require testing on *your individual system*.

Some quick testing on a **Zen 4 (Ryzen 7000) chip without 3D-VCache** suggested that using every other thread for vs and letting the encoder choose by itself is the fastest.

You can set the affinity *and* cache size like this:

```py
from vstools import vs, core

core.set_affinity(threads=range(0, 32, 2), max_cache=22000)
```

Vanilla VS only allows you to set a number of threads via `core.num_threads`.<br>The vs-tools wrapper also sets the affinity.<br>
This example uses every other thread in the range of 0 - 31. Read more about ranges [here](https://docs.python.org/3/library/stdtypes.html#range).

[^1]: vsrepo install bs
[^2]: vsrepo install lsmas
[^3]: vsrepo install ffms2

[installation]: ../installation/standard.md
