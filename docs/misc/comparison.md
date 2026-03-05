# Comparison

Quality comparisons are frequently used within the enthusiast community to compare the video quality offered by different sources/releases. It serves as a great way to distinguish the differences between good and bad sources, and can help you determine which one to download.

This guide goes through the process of setting up and effectively utilizing [VSPreview](https://github.com/Jaded-Encoding-Thaumaturgy/vs-preview), a previewer utility for [VapourSynth](https://github.com/vapoursynth/vapoursynth), to produce useful quality comparisons that will allow you to ascertain which release offers the best visual experience.

!!! warning
    The goal of this guide is to ensure the video is represented as accurately as possible. Do **NOT** use this guide as a reference for making encodes where the goal is to make the video look **better**.

## VSPreview

VSPreview is a previewer application for scripts created in VapourSynth. It features a simple graphical interface to allow you to use VapourSynth's features (and create comparisons) with ease. This should already be installed in your environment if you followed the [setup](../basics/installation.md#installing-the-jet-packages).

### Dependencies

=== "General Setup"

    In order to create comparisons with VSPreview, you will need to install some necessary dependencies.

    - A suitable source filter ([`BestSource`](https://github.com/vapoursynth/bestsource), [`LSMASHSource`](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works), or [`FFMS2`](https://github.com/FFMS/ffms2)).
    - [`vivtc`](https://github.com/vapoursynth/vivtc)
    - [`vs-placebo`](https://github.com/sgt0/vs-placebo)
    - [`libdovi`](https://github.com/quietvoid/dovi_tool)
    - [`awsmfunc`](https://github.com/OpusGang/awsmfunc)

    See [setup](../basics/installation.md) if you need guidance on installing any dependencies.

## Usage

In order to create a comparison, you will need to create a VapourSynth script. This script outlines the parameters and files which VSPreview will use when generating your comparison.

Create a file called `comp.py` and open it in your favorite text editor.

### Basic Script

Here's a simple `comp.py` script example that does nothing more than loading the videos and previewing them.

```py
from vstools import vs, core, depth, set_output, PropEnum, Matrix, Transfer, Primaries, ColorRange, FieldBased

from vssource import BestSource
from vskernels import Point, EwaLanczosSharp
from vsdeinterlace import vfm, vdecimate

from awsmfunc.types.placebo import PlaceboColorSpace as ColorSpace
from awsmfunc.types.placebo import PlaceboTonemapFunction as Tonemap
from awsmfunc.types.placebo import PlaceboGamutMapping as Gamut
from awsmfunc.types.placebo import PlaceboTonemapOpts

# File paths: On Windows, in the File Explorer, hold shift and right-click on your file,
# select copy as path, and paste it here
clip1 = BestSource.source(r"C:\Paste\File\Path\Here.mkv", 0)
clip2 = BestSource.source(r"C:\Paste\File\Path\Here.mkv", 0)
clip3 = BestSource.source(r"C:\Paste\File\Path\Here.mkv", 0)

# Source: Name of the source
source1 = "First source name"
source2 = "Second source name"
source3 = "Third source name"

# <Additional comp settings>
# Place any additional settings you want to use in your comp here
# <End of additional comp settings>

# Output: Comment/uncomment as needed depending on how many clips you're comparing
set_output(clip1, source1)
set_output(clip2, source2)
set_output(clip3, source3)
```

### Common issues

Most of the time, the basic script will not be enough. Different sources may need various adjustments to make a fair comparison, some of which are covered below with small code snippets on how to deal with them.

#### Inverse Telecine

Quick inverse telecine filter for converting telecined clips to progressive.

```py
clip1 = vdecimate(vfm(clip1))
```

#### FieldBased

Force the FieldBased flag to be progressive. This should be done to ensure the content is processed correctly.

```py
clip1 = FieldBased.PROGRESSIVE.apply(clip1)
clip2 = FieldBased.PROGRESSIVE.apply(clip2)
clip3 = FieldBased.PROGRESSIVE.apply(clip3)
```

#### Trimming

Removes the first *n* frames from the source. For example, `[24:]` will skip the first 24 frames and start the source at frame 25. *This should be used on sources that are out of sync.*

To get the frame difference, find a unique frame (e.g. scene changes) in the correct and incorrect source. Note the frame numbers each one begin at, then set the difference of the two for the incorrect source.

```py
clip1 = clip1[0:]
clip2 = clip2[24:]
clip3 = clip3[0:]
```

!!! note
    For more advanced trimming such as chaining, splicing, and looping, see [Vapoursynth's docs](https://www.vapoursynth.com/doc/pythonreference.html#slicing-and-other-syntactic-sugar).

#### Frame Rate

Sets the source frame rate (fps) based on fractional input (`fpsnum`/`fpsden`). For example, `fpsnum=24000` and `fpsden=1001` forces the clip frame rate to 23.976 fps. *This should be used on sources that have different frame rates that don't automatically stay in sync.*

!!! note
    If a clip stays in sync without changing during scrubbing, you should note that the specific source has dropped or duplicate frames.

```py
clip1 = core.std.AssumeFPS(clip1, fpsnum=24000, fpsden=1001)
clip2 = core.std.AssumeFPS(clip2, fpsnum=25000, fpsden=1000)
clip3 = core.std.AssumeFPS(clip3, fpsnum=24000, fpsden=1000)
```

#### FrameProps

Set the correct frame properties for your sources. This is most commonly used on sources you're upscaling or 4K SDR content. *This should be used on sources with incorrect/missing metadata or colors that are off, particularly reds and greens.*

```py
# Example metadata adjustments:

# SDR: BD/WEB (720p - 4K)
clip1 = PropEnum.ensure_presences(clip1, (Matrix.BT709, Transfer.BT709, Primaries.BT709, ColorRange.LIMITED))

# SDR: NTSC DVD
clip2 = PropEnum.ensure_presences(clip2, (Matrix.ST170_M, Transfer.BT601, Primaries.ST170_M, ColorRange.LIMITED))

# SDR: PAL DVD
clip3 = PropEnum.ensure_presences(clip3, (Matrix.BT470_BG, Transfer.BT601, Primaries.BT470_BG, ColorRange.LIMITED))

# HDR/DV
clip4 = PropEnum.ensure_presences(clip4, (Matrix.BT2020_NCL, Transfer.ST2084, Primaries.BT2020, ColorRange.LIMITED))
```

#### Subsampling

Converts clips to 16-bit depth with 4:4:4 chroma subsampling. *Required for filters such as cropping (with odd numbers), tonemapping, debanding (if matching mpv is desired) and furthur gamma-corrected scaling.*

- `EwaLanczosSharp` with antiring is used here as it matches mpv's `high-quality` profile.

```py
clip1 = EwaLanczosSharp().scale(clip1, format=vs.YUV444P16, antiring=0.6)
clip2 = EwaLanczosSharp().scale(clip2, format=vs.YUV444P16, antiring=0.6)
clip3 = EwaLanczosSharp().scale(clip3, format=vs.YUV444P16, antiring=0.6)
```

#### Cropping

Crops the source video by *n* pixels from the selected side. For example, `left=20` will remove 20 horizontal pixels starting from the left side. *This should be used on sources that use letterboxing or other form of borders.*

!!! warning
    If you are cropping with odd numbers, you will need to convert your clip to 4:4:4 chroma subsampling.

```py
clip1 = core.std.Crop(clip1, left=240, right=240, top=0, bottom=0)
clip2 = core.std.Crop(clip2, left=0, right=0, top=276, bottom=276)
clip3 = core.std.Crop(clip3, left=0, right=0, top=21, bottom=21)
```

!!! note
    Make sure to check for variable aspect ratios throughout the file and only crop the smallest border.

#### Tonemapping

Converts the colorspace of the source (i.e. HDR/DV -> SDR).

- For converting HDR -> SDR, set `source_colorspace=ColorSpace.HDR10`
- For converting DV -> SDR, set `source_colorspace=ColorSpace.DOVI`

```py
# Specify the arguments based on your sources:
clip1args = clip2args = PlaceboTonemapOpts(
    source_colorspace=ColorSpace.HDR10,
    target_colorspace=ColorSpace.SDR,
    tone_map_function=Tonemap.Spline,
    gamut_mapping=Gamut.Perceptual,
    peak_detect=True,
    use_dovi=True,
    contrast_recovery=0.3,
    dst_max=100,
)
clip3args = PlaceboTonemapOpts(
    source_colorspace=ColorSpace.DOVI,
    target_colorspace=ColorSpace.SDR,
    tone_map_function=Tonemap.Spline,
    gamut_mapping=Gamut.Perceptual,
    peak_detect=True,
    use_dovi=True,
    contrast_recovery=0.3,
    dst_max=100,
)

## Apply tonemapping
clip1 = core.placebo.Tonemap(clip1, **clip1args.vsplacebo_dict())
clip2 = core.placebo.Tonemap(clip2, **clip2args.vsplacebo_dict())
clip3 = core.placebo.Tonemap(clip3, **clip3args.vsplacebo_dict())

## Retag video to 709 after tonemapping [required]
clip1 = PropEnum.ensure_presences(clip1, (Matrix.BT709, Transfer.BT709, Primaries.BT709))
clip2 = PropEnum.ensure_presences(clip2, (Matrix.BT709, Transfer.BT709, Primaries.BT709))
clip3 = PropEnum.ensure_presences(clip3, (Matrix.BT709, Transfer.BT709, Primaries.BT709))
```

!!! note
    Refer to the [libplacebo](https://libplacebo.org/options/) and [vs-placebo](https://github.com/sgt0/vs-placebo?tab=readme-ov-file#tonemap) docs to gain a better understanding of what each parameter does.

### "Fake HDR" / "SDR-in-HDR" sources

Sometimes the source will be SDR in an HDR container, often seen with anime on Netflix. In these cases you can clip the source to get an exact match to SDR, unlike with traditional tonemapping.

```py
## Clip HDR source to SDR
clip1 = Point().resample(clip1, matrix=Matrix.BT709, transfer=Transfer.BT709, primaries=Primaries.BT709)

## Clip DV source to SDR
clip3args = PlaceboTonemapOpts(source_colorspace=ColorSpace.DOVI, target_colorspace=ColorSpace.HDR10, use_dovi=True)

clip3 = core.placebo.Tonemap(clip3, **clip2args.vsplacebo_dict())
clip3 = PropEnum.ensure_presences(clip3, (Matrix.BT2020_NCL, Transfer.ST2084, Primaries.BT2020))

clip3 = Point().resample(clip3, matrix=Matrix.BT709, transfer=Transfer.BT709, primaries=Primaries.BT709)
```

#### Double-Range Compression (DRC)

Fixes washed out colors on sources that have been converted to limited range twice.

```py
clip1 = depth(clip1, range_in=ColorRange.LIMITED, range_out=ColorRange.FULL)
clip1 = ColorRange.LIMITED.apply(clip1)
```

### Depth

Converts clips to 32-bit depth. *Required for gamma adjustment and final output scaling.*

```py
clip1 = depth(clip1, 32)
clip2 = depth(clip2, 32)
clip3 = depth(clip3, 32)
```

#### Gamma

Adjusts the gamma level of the video. *This should only be used to fix the QuickTime gamma bug or similar where one source will appear much brighter than the rest.*

```py
clip1 = core.std.Levels(clip1, gamma=0.88, planes=0)
clip2 = core.std.Levels(clip2, gamma=0.88, planes=0)
clip3 = core.std.Levels(clip3, gamma=0.88, planes=0)
```

### Pixel format

The following steps require the input to be RGBS format for the best results, so add an additional conversion here if you're applying them.

```py
clip1 = Point().resample(clip1, format=vs.RGBS)
clip2 = Point().resample(clip2, format=vs.RGBS)
clip3 = Point().resample(clip3, format=vs.RGBS)
```

### Debanding

Applies a debanding filter to the selected clip(s). *Otherwise competitive sources with obvious banding should be debanded to see how they'd fare with mpv's built-in deband filter. The debanded clip should never replace the original. Instead, it should be added as an additional node.*

```py
# mpv -> vsplacebo thresholds should be divided by 16.384.
# mpv -> vsplacebo grain strength should be divided by 8.192.
# https://github.com/mpv-player/mpv/blob/3b55bc9795a4ab6cf04d1611f4839330cf5c1990/video/out/vo_gpu_next.c#L2561-L2562

clip4 = core.placebo.Deband(clip1, planes=1|2|4, threshold=48 / 16.384, grain=32 / 8.192)
```

#### Scaling

Upscales the video. *This should be used to match sources that have differing resolutions.*

- `EwaLanczosSharp` with antiring is used here as it matches mpv's `high-quality` profile.

```py
clip1 = EwaLanczosSharp().scale(clip1, 3840, 2160, sigmoid=True, antiring=0.6)
clip2 = EwaLanczosSharp().scale(clip2, 3840, 2160, sigmoid=True, antiring=0.6)
clip3 = EwaLanczosSharp().scale(clip3, 3840, 2160, sigmoid=True, antiring=0.6)
```

### Running

To run your comparison script, launch a terminal window in your working directory and run the following:

```powershell
vspreview comp.py
```

### Tips

- Label your sources clearly.
- Try to capture a large variety of scenes (e.g. low/high detail, bright/dark, low/high motion).
- Try to capture frames of the same type.
- Try to capture `P` or `B` type frames when possible. Although it's not always guaranteed that your source will have all the picture types (e.g. Crunchyroll WEB-DLs don't have `B` frames).

### Basic Keybinds

Key                | Action
-------------------|------------------------------------------------------------
`Left arrow` (<-)  | Move back *n* frames (default: *n = 1*)
`Right arrow` (->) | Move forward *n* frames (default: *n = 1*)
Number keys        | Switches to source *n* (e.g. `2` switches to `clip2`)
`Shift` + `S`      | Take and save screenshot of the current frame
`Ctrl` + `Space`   | Mark current frame number for [semi-automatic] comparisons

### Process

VSPreview offers three methods for creating comparisons:

=== "Automatic"

    Automatic comparisons are created completely without any additional user input. VSPreview will automatically select, capture, and upload frames for you. *This is the fastest method for creating comparisons.*

    1. In VSPreview, click the *Plugins* button in the bottom right corner and
       then click the *SlowPics Comps* tab

    2. Fill out these fields:

        Key              | Description
        -----------------|-----------------------------------------------------------------------------------------------------
        Collection name  | The title of your comparison/show
        Random           | Number of frames to randomly capture. *This should be set to a value higher or equal to 40 frames*
        Picture types    | The picture type
        TMDB ID          | The [TMDB ID](https://www.themoviedb.org) for the show

    3. Hit the *Start Upload* button to begin creating your comparison

=== "Semi-automatic"

    Semi-automatic comparisons are created with minor user input. VSPreview will automatically capture and upload frame manually marked by the user. *This is the recommended method for creating comparisons.*

    1. Locate the frame(s) you want to compare
        - Use `Left arrow` to go the previous frame and `Right arrow` to go to the next frame.
        - Use `Shift + Left arrow` and `Shift + Right arrow` to navigate `N` number of frames on either side.

    2. Once you land on a frame you like, mark it with `Ctrl` + `Space`.

    <hr>

    3. In VSPreview, click the *Plugins* button in the bottom right corner and
       then click the *SlowPics Comps* tab

    4. Fill out these fields:

        Key              | Description
        -----------------|-----------------------------------------------------------------------------------------------------
        Collection name  | The title of your comparison/show
        TMDB ID          | The [TMDB ID](https://www.themoviedb.org) for the show

    5. Hit the *Start Upload* button to begin creating your comparison

=== "Manual"

    Manual comparisons are created completely by the user. VSPreview displays and handles frame capture, while the main actions are performed by the user through the previewer.

    1. Locate the frame(s) you want to compare
        - Use `Left arrow` to go the previous frame and `Right arrow` to go to the next frame.
        - Use `Shift + Left arrow` and `Shift + Right arrow` to navigate `N` number of frames on either side.

    2. Once you land on a frame you like, take its screenshot with `Shift` + `S`.

    3. Switch to the other sources and take screenshots of their current frame
        - Press the number keys to change sources (e.g. `1` for `clip1`, `2` for `clip2`)

    4. Repeat process for the next frames in your comparison

    !!! note
        If you want to use automatic Slowpoke Pics sorting, make sure your file naming scheme is set to `{frame}_{index}_{Name}`.
        By default, all frames are stored within your working directory unless manually changed to a different destination.

### Slowpoke Pics

If you plan on uploading to [Slowpoke Pics](https://slow.pics) (slow.pics) under
your account, you will need to provide VSPreview with your account credentials.

1. In VSPreview, go to **Plugins** -> **SlowPics Comps** -> **Settings**
2. Fill out the *Username* and *Password* fields
3. Click *Login*
