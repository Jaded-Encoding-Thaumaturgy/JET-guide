Some basics that might be useful when writing your first script.

## Index a video

#### Available indexers to consider

- [bestsource](https://github.com/vapoursynth/bestsource)[^1]<br>
    The most accurate but slowest indexer.
- [lsmas](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works/)[^2]<br>
    Fast, mostly reliable enough.
- [ffms2](https://github.com/FFMS/ffms2)[^3]<br>
    With the latest version pretty much on par with lsmas and possibly even faster.

DGIndexNV is also technically something you can use but recent versions have been buggy and it's restricted to Nvidia GPUs.

!!! danger "DVDs"
    For DVDs you can skip the following Usage section and simply read the `IsoFile` usage section in the [vs-source readme](https://github.com/Jaded-Encoding-Thaumaturgy/vs-source?tab=readme-ov-file#usage).<br>
    I've been told dvdsrc also should set the metadata correctly but ymmv.

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
## Ensure video metadata

Most functions that resample/resize a video require metadata to be present.<br>
Most videos you download and the majority of BDs are untagged so this is often a necessary step. (And really also just good practice)

**Indexing via vs-source will automatically try to guess via resolution.**

=== "vstools"
    ```py
    from vstools import initialize_clip, Matrix, Primaries, Transfer
    
    # Will automatically try to guess via resolution and upsample to 16 bit.
    clip = initialize_clip(clip)
    
    # You can also set everything manually with the enums in vstools/vs
    
    # For most HD sources
    clip = initialize_clip(clip, matrix=Matrix.BT709, primaries=Primaries.BT709, transfer=Transfer.BT709)
    
    # For most NTSC DVDs
    clip = initialize_clip(clip, matrix=Matrix.SMPTE170M, primaries=Primaries.ST170M, transfer=Transfer.BT601)
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
    clip = JPBD.init_cut(matrix=Matrix.SMPTE170M, primaries=Primaries.ST170M, transfer=Transfer.BT601)
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


[^1]: vsrepo install bs
[^2]: vsrepo install lsmas
[^3]: vsrepo install ffms2