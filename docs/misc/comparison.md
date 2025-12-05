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

    - [`LibP2P`](https://github.com/DJATOM/LibP2P-Vapoursynth), [`LSMASHSource`](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works), [`Subtext`](https://github.com/vapoursynth/subtext) and [`vs-placebo`](https://github.com/sgt0/vs-placebo) can be installed using `vsrepo` from [VapourSynth](https://github.com/vapoursynth/vapoursynth/releases). In your terminal, run the following:

    ```powershell
    vsrepo.py install libp2p lsmas sub placebo
    ```

    !!! note
        If `vsrepo.py` command doesn't work, make sure Windows is set to open `.py` files with Python. You may also need to add it to the `PATHEXT` environment variable.

    - [`awsmfunc`](https://github.com/OpusGang/awsmfunc) can be installed using `pip`:

    ```powershell
    python -m pip install git+https://github.com/OpusGang/awsmfunc.git
    ```

=== "Dolby Vision"

    If you're working with Dolby Vision (DV) content, you will need to install additional dependencies.

    - [`libdovi`](https://github.com/quietvoid/dovi_tool) can be installed using `vsrepo` from [VapourSynth](https://github.com/vapoursynth/vapoursynth/releases). In your terminal, run the following:

    ```powershell
    vsrepo.py install dovi_library
    ```

## Usage

In order to create a comparison, you will need to create a VapourSynth script. This script outlines the parameters and files which VSPreview will use when generating your comparison.

Create a file called `comp.py` and open it in your favorite text editor.

### Basic Script

Here's a simple `comp.py` script example that does nothing more than loading the videos and previewing them.

```py
from vssource import LSMAS
from vstools import vs, core, set_output
from awsmfunc import FrameInfo

# File paths: On Windows, in the File Explorer, hold shift and right-click on your file,
# select copy as path, and paste it here
clip1 = LSMAS.source(r"C:\Paste\File\Path\Here.mkv", 0)
clip2 = LSMAS.source(r"C:\Paste\File\Path\Here.mkv", 0)
clip3 = LSMAS.source(r"C:\Paste\File\Path\Here.mkv", 0)

# Source: Name of the source
source1 = "First source name"
source2 = "Second source name"
source3 = "Third source name"

# <Additional comp settings>
# Place any additional settings you want to use in your comp here
# <End of additional comp settings>

## Frameinfo: Displays the frame number, type, and group name in the top left corner (no modification required; add/remove lines as needed)
clip1 = FrameInfo(clip1, source1)
clip2 = FrameInfo(clip2, source2)
clip3 = FrameInfo(clip3, source3)

# Output: Comment/uncomment as needed depending on how many clips you're comparing
set_output(clip1, source1)
set_output(clip2, source2)
set_output(clip3, source3)
```

### Common issues

Most of the time, the basic script will not be enough. Different sources may need various adjustments to make a fair comparison, some of which are covered below with small code snippets on how to deal with them.

#### Frame Rate

Sets the source frame rate (fps) based on fractional input (`fpsnum`/`fpsden`). For example, `fpsnum=24000` and `fpsden=1001` forces the clip frame rate to 23.976 fps. *This should be used on sources that have different frame rates that don't automatically stay in sync.*

!!! note
    If a clip stays in sync without changing during scrubbing, you should note that the specific source has dropped or duplicate frames.

```py
# Frame rate: Change fps to match other sources
# (needed for when the previewer is unable to automatically keep them in sync)
clip1 = core.std.AssumeFPS(clip1, fpsnum=24000, fpsden=1001)
clip2 = core.std.AssumeFPS(clip2, fpsnum=25000, fpsden=1000)
clip3 = core.std.AssumeFPS(clip3, fpsnum=24000, fpsden=1000)
```

#### FieldBased

Sets interlaced flagged content that may be progressive as progressive.

```py
## FieldBased: Tags the content as progressive (0); used for progressive content tagged as interlaced
clip1 = core.std.SetFieldBased(clip1, 0)
clip2 = core.std.SetFieldBased(clip2, 0)
clip3 = core.std.SetFieldBased(clip3, 0)
```

#### Inverse Telecine

Quick inverse telecine filter for converting telecined clips to progressive.

```py
## Inverse telecine: Fixes telecined video
clip1 = core.vivtc.VFM(clip1, 1)
clip1 = core.vivtc.VDecimate(clip1)
```

!!! note
    You need [`vivtc`](https://github.com/vapoursynth/vivtc) installed for the above snippet to work.
    On Windows, You can install it with `vsrepo.py install vivtc`.

#### Cropping

Crops the source video by *n* pixels from the selected side. For example, `left=20` will remove 20 horizontal pixels starting from the left side. *This should be used on sources that use letterboxing or other form of borders.*

!!! warning
    If you are cropping with odd numbers, you will need to convert your clip to 4:4:4 chroma subsampling.


```py
## Cropping: Removes letterboxing (black bars) [16-bit required for odd numbers]
clip1 = core.std.Crop(clip1, left=240, right=240, top=0, bottom=0)
clip2 = core.std.Crop(clip2, left=0, right=0, top=276, bottom=276)
clip3 = core.std.Crop(clip3, left=0, right=0, top=21, bottom=21)
```

!!! note
    Make sure to check for variable aspect ratios throughout the file and only crop the smallest border.

#### Scaling

Downscales or upscales the video. *This should be used to match sources that have differing resolutions.*

- For upscaling (e.g. 720p -> 1080p), use `EwaLanczosSharp`.
  It is the default upscaler when using the `high-quality` profile on mpv:

```py
from vskernels import EwaLanczosSharp

# Upscaling: Increases the resolution of clips to match the highest resolution using EwaLanczosSharp
clip1 = EwaLanczosSharp().scale(clip1, 1920, 1080, sigmoid=True)
clip2 = EwaLanczosSharp().scale(clip2, 1920, 1080, sigmoid=True)
clip3 = EwaLanczosSharp().scale(clip3, 3840, 2160, sigmoid=True)
```

- For downscaling (e.g. 2160p/4K -> 1080p), use `Hermite`
  It is the default downscaler when using the `high-quality` profile on mpv:

```py
from vskernels import Hermite

# Downscaling: Decreases the resolution of clips to match the lowest resolution using Hermite
clip1 = Hermite().scale(clip1, 1920, 1080, linear=True)
clip2 = Hermite().scale(clip2, 1920, 1080, linear=True)
clip3 = Hermite().scale(clip3, 3840, 2160, linear=True)
```

!!! warning
    Downscaling is generally not recommended. We suggest upscaling your sources to match the highest resolution unless you have a specific reason (e.g. comparing how a higher resolution file would look on a lower resolution display).

#### Trimming

Removes the first *n* frames from the source. For example, `[24:]` will skip the first 24 frames and start the source at frame 25. *This should be used on sources that are out of sync.*

To get the frame difference, find a unique frame (e.g. scene changes) in the correct and incorrect source. Note the frame numbers each one begin at, then set the difference of the two for the incorrect source.

```py
# Trimming: Trim frames to match clips (calculate the frame difference and enter the number here)
clip1 = clip1[0:]
clip2 = clip2[24:]
clip3 = clip3[0:]
```

!!! note
    For more advanced trimming such as chaining, splicing, and looping, see [Vapoursynth's docs](https://www.vapoursynth.com/doc/pythonreference.html#slicing-and-other-syntactic-sugar).

#### Depth

Converts clips to 16-bit depth with 4:4:4 chroma subsampling. *Required for filters such as cropping (with odd numbers) or tonemapping.*

```py
from vstools import depth

## Depth: Convert clips to 16-bit 4:4:4 [required for cropping with odd numbers or tonemapping]
clip1 = EwaLanczosSharp().scale(depth(clip1, 16), format=vs.YUV444P16)
clip2 = EwaLanczosSharp().scale(depth(clip2, 16), format=vs.YUV444P16)
clip3 = EwaLanczosSharp().scale(depth(clip3, 16), format=vs.YUV444P16)
```

#### Tonemapping

Converts the colorspace of the source (i.e. HDR/DV -> SDR).

- For converting HDR (washed out colors) -> SDR, set `source_colorspace=ColorSpace.HDR10`
- For converting DV (green/purple hue) -> SDR, set `source_colorspace=ColorSpace.DOVI`

!!! note
    If you want to tonemap, you will need to change the clip's bit depth to 16-bit (see [above](#depth)).

```py
# Additional imports [Paste these at the very top of your script]
from awsmfunc.types.placebo import PlaceboColorSpace as ColorSpace
from awsmfunc.types.placebo import PlaceboTonemapFunction as Tonemap
from awsmfunc.types.placebo import PlaceboGamutMapping as Gamut
from awsmfunc.types.placebo import PlaceboTonemapOpts
from vstools import Matrix, Primaries, PropEnum, Transfer, core

# Tonemapping: Converts the dynamic range of the source [16-bit required]
# Specify the arguments based on your sources;
# play with different values when comparing against an SDR source to best match it
clip1args = PlaceboTonemapOpts(
    source_colorspace=ColorSpace.DOVI,
    target_colorspace=ColorSpace.SDR,
    tone_map_function=Tonemap.ST2094_40,
    gamut_mapping=Gamut.Clip,
    peak_detect=True,
    use_dovi=True,
    contrast_recovery=0.3,
)
clip2args = PlaceboTonemapOpts(
    source_colorspace=ColorSpace.HDR10,
    target_colorspace=ColorSpace.SDR,
    tone_map_function=Tonemap.ST2094_40,
    gamut_mapping=Gamut.Clip,
    peak_detect=True,
    use_dovi=False,
    contrast_recovery=0.3,
)
clip3args = PlaceboTonemapOpts(
    source_colorspace=ColorSpace.HDR10,
    target_colorspace=ColorSpace.SDR,
    tone_map_function=Tonemap.Spline,
    gamut_mapping=Gamut.Darken,
    peak_detect=True,
    use_dovi=False,
    contrast_recovery=0.3,
    dst_max=120,
)

## Apply tonemapping
clip1 = core.placebo.Tonemap(clip1, **clip1args.vsplacebo_dict())
clip2 = core.placebo.Tonemap(clip2, **clip2args.vsplacebo_dict())
clip3 = core.placebo.Tonemap(clip3, **clip3args.vsplacebo_dict())

## Retag video to 709 after tonemapping [required]
clip1 = PropEnum.ensure_presences(clip1, [Matrix.BT709, Transfer.BT709, Primaries.BT709])
clip2 = PropEnum.ensure_presences(clip2, [Matrix.BT709, Transfer.BT709, Primaries.BT709])
clip3 = PropEnum.ensure_presences(clip3, [Matrix.BT709, Transfer.BT709, Primaries.BT709])

```

!!! note
    Refer to the [libplacebo](https://libplacebo.org/options/) and [vs-placebo](https://github.com/sgt0/vs-placebo?tab=readme-ov-file#tonemap) docs to gain a better understanding of what each parameter does.

#### Range

Converts the color range of the clip to limited or full. *This should be used on sources containing incorrect metadata or after tonemapping DV content (set it to limited).*

```py
from vstools import depth

# Color range: Converts the clip's range as limited or full;
# DV clips will need to be set to limited after tonemapping
clip1 = depth(clip1, range_out=ColorRange.LIMITED)
clip2 = depth(clip2, range_out=ColorRange.FULL)
clip3 = depth(clip3, range_out=ColorRange.FULL)
```

#### Gamma

Adjusts the gamma level of the video. *This should only be used to fix the QuickTime gamma bug or similar where one source will appear much brighter than the rest.*

```py
from vstools import depth

## Gamma: Fixes gamma bug (i.e. one source is significantly brighter than the others) [32-bit required]
## Convert clips to 32-bit [required for gamma fix]
clip1 = depth(clip1, 32)
clip2 = depth(clip2, 32)
clip3 = depth(clip3, 32)
## Apply fix
clip1 = core.std.Levels(clip1, gamma=0.88, planes=0)
clip2 = core.std.Levels(clip2, gamma=0.88, planes=0)
clip3 = core.std.Levels(clip3, gamma=0.88, planes=0)
```

#### FrameProps

Set the correct frame properties for your sources. This is most commonly used on sources you're upscaling or 4K SDR content. *This should be used on sources with incorrect/missing metadata or colors that are off, particularly reds and greens.*

```py
from vstools import PropEnum
# FrameProps: Repairs sources with incorrect/missing metadata;
# typically used for 4K SDR and upscaled/downscaled content
# (colors will be off, particularly reds, greens, and blues)

# SDR: BD/WEB (720p - 4K)
clip1 = PropEnum.ensure_presences(clip1, [Matrix.BT709, Transfer.BT709, Primaries.BT709])

# SDR: PAL DVD
clip2 = PropEnum.ensure_presences(clip2, [Matrix.BT470_BG, Transfer.BT470_BG, Primaries.BT470_BG])

# SDR: NTSC DVD
clip3 = PropEnum.ensure_presences(clip3, [Matrix.ST170_M, Transfer.BT601, Primaries.ST170_M])

# HDR/DV
clip4 = PropEnum.ensure_presences(clip4, [Matrix.BT2020_CL, Transfer.BT2020_10, Primaries.BT2020])
```

#### Double-Range Compression (DRC)

Fixes washed out colors on selected sources.

```py
from vstools import ColorRange, depth

## Fix DRC: Repairs sources with very washed out colors
clip1 = depth(clip1, range_in=ColorRange.LIMITED, range_out=ColorRange.FULL)
clip1 = ColorRange.LIMITED.apply(clip1)
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
