# Comparison

Quality comparisons are frequently used within the enthusiast community to compare the video quality offered by different sources/releases. It serves as a great way to distinguish the differences between good and bad sources, and can help you determine which one to download.

This guide goes through the process of setting up and effectively utilizing [VSPreview](https://github.com/Jaded-Encoding-Thaumaturgy/vs-preview), a previewer utility for [VapourSynth](https://github.com/vapoursynth/vapoursynth), to produce useful quality comparisons that will allow you to ascertain which release offers the best visual experience.

!!! warning
    The goal of this guide is to ensure the video is represented as accurately as possible. Do **NOT** use this guide as a reference for making encodes where the goal is to make the video look **better**.

### VSPreview

VSPreview is a previewer application for scripts created in VapourSynth. It features a simple graphical interface to allow you to use VapourSynth's features (and create comparisons) with ease. This should already be installed in your environment if you followed the [setup](https://jaded-encoding-thaumaturgy.github.io/JET-guide/setup/).

#### Dependencies

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

Create a file called `comp.py` and launch it in your favorite text editor.

### Basic Script

Here's a simple `comp.py` script example that does nothing more than loading the videos and previewing them.

```py
from vstools import vs, core, set_output
from awsmfunc import FrameInfo

## File paths: Hold shift and right-click your file in the Windows File Explorer, select copy as path, and paste it here
clip1 = core.lsmas.LWLibavSource(r"C:\Paste\File\Path\Here.mkv")
clip2 = core.lsmas.LWLibavSource(r"C:\Paste\File\Path\Here.mkv")
clip3 = core.lsmas.LWLibavSource(r"C:\Paste\File\Path\Here.mkv")

## Source: Name of the source
source1 = "FirstSourceName"
source2 = "SecondSourceName"
source3 = "ThirdSourceName"

## <Additional comp settings>
## Place any additional settings you want to use in your comp here
## <End of additional comp settings>

## Frameinfo: Displays the frame number, type, and group name in the top left corner (no modification required; add/remove lines as needed)
clip1 = FrameInfo(clip1, source1)
clip2 = FrameInfo(clip2, source2)
clip3 = FrameInfo(clip3, source3)

## FrameProp: Slowpoke Pics/file-name labeling (no modification required; add/remove lines as needed)
clip1 = clip1.std.SetFrameProp('Name', data=source1)
clip2 = clip2.std.SetFrameProp('Name', data=source2)
clip3 = clip3.std.SetFrameProp('Name', data=source3)

## Output: Comment/uncomment as needed depending on how many clips you're comparing
set_output(clip1, name=source1)
set_output(clip2, name=source2)
set_output(clip3, name=source3)
```

### Common issues

Most of the time, the basic script will not be enough. Different sources may need various adjustments to make a fair comparison, some of which are covered below with small code snippets on how to deal with them.

#### Frame Rate

Sets the source frame rate (fps) based on fractional input (`fpsnum`/`fpsden`). For example, `fpsnum=24000` and `fpsden=1001` forces the clip frame rate to 23.976 fps. *This should be used on sources that have different frame rates that don't automatically stay in sync.*

!!! note
    If a clip stays in sync without changing during scrubbing, you should note that the specific source has dropped or duplicate frames.

```py
## Frame rate: Change fps to match other sources (needed for when the previewer is unable to automatically keep them in sync)
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
    You need [`vivtc`](https://github.com/vapoursynth/vivtc) installed for the above snippet to work. You can install it with `vsrepo.py install vivtc`.


#### Cropping

Crops the source video by *n* pixels from the selected side. For example, `left=20` will remove 20 horizontal pixels starting from the left side. *This should be used on sources that use letterboxing or other form of borders.*

!!! warning
    If you are cropping with odd numbers, you will need to change the depth to 16-bit.


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

- For upscaling (e.g. 720p -> 1080p), use `EwaLanczos`:

```py
from vskernels import EwaLanczos

## Upscaling: Increases the resolution of clips to match the highest resolution using EwaLanczos (equivalent scaling to mpv's high-quality profile); recommended
clip1 = EwaLanczos.scale(clip1, 1920, 1080, sigmoid=True)
clip2 = EwaLanczos.scale(clip2, 1920, 1080, sigmoid=True)
clip3 = EwaLanczos.scale(clip3, 3840, 2160, sigmoid=True)
```

- For downscaling (e.g. 2160p/4K -> 1080p), use `Hermite`:

```py
from vskernels import Hermite

## Downscaling: Decreases the resolution of clips to match the lowest resolution using Hermite (equivalent scaling to mpv's high-quality profile); not recommended
clip1 = Hermite.scale(clip1, 1920, 1080, linear=True)
clip2 = Hermite.scale(clip2, 1920, 1080, linear=True)
clip3 = Hermite.scale(clip3, 3840, 2160, linear=True)
```

!!! warning
    Downscaling is generally not recommended. We suggest upscaling your sources to match the highest resolution unless you have a specific reason (e.g. comparing how a higher resolution file would look on a lower resolution display).

#### Trimming

Removes the first *n* frames from the source. For example, `[24:]` will skip the first 24 frames and start the source at frame 25. *This should be used on sources that are out of sync.*

To get the frame difference, find a unique frame (e.g. scene changes) in the correct and incorrect source. Note the frame numbers each one begin at, then set the difference of the two for the incorrect source.

```py
## Trimming: Trim frames to match clips (calculate the frame difference and enter the number here)
clip1 = clip1[0:]
clip2 = clip2[24:]
clip3 = clip3[0:]
```

!!! note
    For more advanced trimming such as chaining, splicing, and looping, see [Vapoursynth's docs](https://www.vapoursynth.com/doc/pythonreference.html#slicing-and-other-syntactic-sugar).


#### Depth

Converts clips to 16-bit depth with 4:4:4 chroma subsampling. *Required for filters such as cropping (with odd numbers) or tonemapping.*

```py
## Depth: Convert clips to 16-bit 4:4:4 [required for cropping with odd numbers or tonemapping]
clip1 = core.resize.Lanczos(clip1, format=vs.YUV444P16)
clip2 = core.resize.Lanczos(clip2, format=vs.YUV444P16)
clip3 = core.resize.Lanczos(clip3, format=vs.YUV444P16)
```

#### Tonemapping

Converts the dynamic range of the source (i.e. HDR/DV -> SDR).

- For converting HDR (washed out colors) -> SDR, set `source_colorspace=csp.HDR10`
- For converting DV (green/purple hue) -> SDR, set `source_colorspace=csp.DOVI`

!!! warning
    If you want to use tonemapping, you will need to change the color depth to 16-bit (see [above](#depth)).

```py
## Additional imports [Paste these at the very top of your script]
from awsmfunc.types.placebo import PlaceboColorSpace as csp
from awsmfunc.types.placebo import PlaceboTonemapMode as TMmode
from awsmfunc.types.placebo import PlaceboTonemapFunction as TMfunc
from awsmfunc.types.placebo import PlaceboGamutMode as GMTmode
from awsmfunc.types.placebo import PlaceboTonemapOpts as TMopts

## Tonemapping: Converts the dynamic range of the source [16-bit required]
## Specify the arguments based on your sources; play with different values when comparing against an SDR source to best match it
clip1args = TMopts(source_colorspace=csp.DOVI, target_colorspace=csp.SDR, tone_map_mode=TMmode.RGB, tone_map_function=TMfunc.ST2094_40, gamut_mode=GMTmode.Clip, peak_detect=True, use_dovi=True)
clip2args = TMopts(source_colorspace=csp.HDR10, target_colorspace=csp.SDR, tone_map_mode=TMmode.RGB, tone_map_function=TMfunc.ST2094_40, gamut_mode=GMTmode.Clip, peak_detect=True, use_dovi=True)
clip3args = TMopts(source_colorspace=csp.HDR10, target_colorspace=csp.SDR, tone_map_mode=TMmode.Hybrid, tone_map_function=TMfunc.Spline, gamut_mode=GMTmode.Darken, peak_detect=True, use_dovi=True, dst_max=120)
## Apply tonemapping
clip1 = core.placebo.Tonemap(clip1, **clip1args.vsplacebo_dict())
clip2 = core.placebo.Tonemap(clip2, **clip2args.vsplacebo_dict())
clip3 = core.placebo.Tonemap(clip3, **clip3args.vsplacebo_dict())
## Retag video to 709 after tonemapping [required]
clip1 = core.std.SetFrameProps(clip1, _Matrix=vs.MATRIX_BT709, _Transfer=vs.TRANSFER_BT709, _Primaries=vs.PRIMARIES_BT709)
clip2 = core.std.SetFrameProps(clip2, _Matrix=vs.MATRIX_BT709, _Transfer=vs.TRANSFER_BT709, _Primaries=vs.PRIMARIES_BT709)
clip3 = core.std.SetFrameProps(clip3, _Matrix=vs.MATRIX_BT709, _Transfer=vs.TRANSFER_BT709, _Primaries=vs.PRIMARIES_BT709)
```

!!! note
    `dst_max` forces a set brightness, which can be used to make HDR/DV clips appear brighter for easier comparison to SDR.

#### Range

Sets the color range of the clip as limited (`0`) or full (`1`). *This should be used on sources containing incorrect metadata or after tonemapping DV content (set it to limited).*

```py
## Color range: Marks the clip's range as limited (0) or full (1); DV clips will need to be set to limited (0) after tonemapping
clip1 = core.resize.Lanczos(clip1, format=vs.YUV444P16, range=0)
clip2 = core.resize.Lanczos(clip2, format=vs.YUV444P16, range=0)
clip3 = core.resize.Lanczos(clip3, format=vs.YUV444P16, range=1)
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
## FrameProps: Repairs sources with incorrect/missing metadata; typically used for 4K SDR and upscaled/downscaled content (colors will be off, particularly reds, greens, and blues)

# SDR: BD/WEB (720p - 4K)
clip1 = core.std.SetFrameProps(clip1, _Matrix=vs.MATRIX_BT709, _Transfer=vs.TRANSFER_BT709, _Primaries=vs.PRIMARIES_BT709)

# SDR: PAL DVD
clip2 = core.std.SetFrameProps(clip2, _Matrix=vs.MATRIX_BT470_BG, _Transfer=vs.TRANSFER_BT470_BG, _Primaries=vs.PRIMARIES_BT470_BG)

# SDR: NTSC DVD
clip3 = core.std.SetFrameProps(clip3, _Matrix=vs.MATRIX_ST170_M, _Transfer=vs.TRANSFER_BT601, _Primaries=vs.PRIMARIES_ST170_M,)

# HDR/DV
clip4 = core.std.SetFrameProps(clip4, _Matrix=vs.MATRIX_BT2020_NCL, _Transfer=vs.TRANSFER_BT2020_10, _Primaries=vs.PRIMARIES_BT2020)
```

If you are unable to correct the source's colors with the initial matrix command, the source is likely flawed rather than an issue with the metadata. If this is the case, you should use the filters below:

```py
from vstools import depth

## Resample: If the colors cannot be corrected with just retagging
# SDR: BD/WEB (720p - 4K)
clip1 = depth(clip1, 32)
clip1 = core.placebo.Resample(clip1, height=clip1.height, width=clip1.width, filter="ewa_lanczos", blur=0.98125058372237073562493, radius=3.2383154841662362076499)
clip1 = core.std.SetFrameProps(clip1, _Matrix=vs.MATRIX_BT709, _Transfer=vs.TRANSFER_BT709, _Primaries=vs.PRIMARIES_BT709)

# SDR: PAL DVD
clip2 = depth(clip2, 32)
clip2 = core.placebo.Resample(clip2, height=clip2.height, width=clip2.width, filter="ewa_lanczos", blur=0.98125058372237073562493, radius=3.2383154841662362076499)
clip2 = core.std.SetFrameProps(clip2, _Matrix=vs.MATRIX_BT470_BG, _Transfer=vs.TRANSFER_BT470_BG, _Primaries=vs.PRIMARIES_BT470_BG)

# SDR: NTSC DVD
clip3 = depth(clip3, 32)
clip3 = core.placebo.Resample(clip3, height=clip3.height, width=clip3.width, filter="ewa_lanczos", blur=0.98125058372237073562493, radius=3.2383154841662362076499)
clip3 = core.std.SetFrameProps(clip3, _Matrix=vs.MATRIX_ST170_M, _Transfer=vs.TRANSFER_BT601, _Primaries=vs.PRIMARIES_ST170_M,)

# HDR/DV
clip4 = depth(clip4, 32)
clip4 = core.placebo.Resample(clip4, height=clip4.height, width=clip4.width, filter="ewa_lanczos", blur=0.98125058372237073562493, radius=3.2383154841662362076499)
clip4 = core.std.SetFrameProps(clip4, _Matrix=vs.MATRIX_BT2020_NCL, _Transfer=vs.TRANSFER_BT2020_10, _Primaries=vs.PRIMARIES_BT2020)
```

#### Double-Range Compression (DRC)

Fixes washed out colors on selected sources.

```py
## Fix DRC: Repairs sources with very washed out colors
clip1 = core.resize.Point(clip1, range_in=0, range=1, dither_type="error_diffusion")
clip1 = core.std.SetFrameProp(clip1, prop="_ColorRange", intval=1)
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
- Try to capture `P` or `B` type frames when possible. Although it's not always guranteed that your source will have all the picture types (e.g. Crunchyroll WEB-DLs don't have `B` frames).

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

    #### Capturing

    1. In VSPreview, navigate to the bottom bar and toggle the *Comp* section

    2. Fill out these fields:

        Key              | Description
        -----------------|-----------------------------------------------------------------------------------------------------
        Collection name  | The title of your comparison/show
        Random           | Number of frames to randomly capture. *This should be set to a value higher or equal to 40 frames*
        Picture types    | The picture type
        TMDB ID          | The [TMDB ID](https://www.themoviedb.org) for the show

    3. Hit the *Start Upload* button under *Comp* to begin creating your comparison

=== "Semi-automatic"

    Semi-automatic comparisons are created with minor user input. VSPreview will automatically capture and upload frame manually marked by the user. *This is the recommended method for creating comparisons.*

    #### Setup

    1. Locate the frame(s) you want to compare
        - Use `Left arrow` to go the previous frame and `Right arrow` to go to the next frame.
        - Use `Shift + Left arrow` and `Shift + Right arrow` to navigate `N` number of frames on either side.
    
    2. Once you land on a frame you like, mark it with `Ctrl` + `Space`.

    #### Capturing

    1. In VSPreview, navigate to the bottom bar and toggle the *Comp* section

    2. Fill out these fields:

        Key              | Description
        -----------------|-----------------------------------------------------------------------------------------------------
        Collection name  | The title of your comparison/show
        TMDB ID          | The [TMDB ID](https://www.themoviedb.org) for the show

    3. Hit the *Start Upload* button under *Comp* to begin creating your comparison

=== "Manual"

    Manual comparisons are created completely by the user. VSPreview displays and handles frame capture, while the main actions are performed by the user through the previewer.

    #### Capturing

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

#### Fetching Account Tokens

If you plan on uploading to [Slowpoke Pics](https://slow.pics) (slow.pics) under your account, you will need to provide VSPreview with your account token.

=== "Chrome"

    - Visit [Slowpoke Pics](https://slow.pics) in your browser and log into your account
    - Open your browser's **Developer Tools**. You will need to get two values:
    - To get your `browserId`, go to **Application** -> **Storage** -> **Local Storage** -> `https://slow.pics`. Copy the key listed there
    - To get your `sessionId`, go to **Network**. Refresh the page, then find `slow.pics`. On the right section open cookies and copy the `SLP-SESSION` value
    - In VSPreview, go to **Settings** -> **Comp**
    - Paste the two values in the boxes provided

=== "Firefox"

    - Visit [Slowpoke Pics](https://slow.pics) in your browser and log into your account
    - Open your browser's **Developer Tools**. You will need to get two values:
    - To get your `browserId`, go to **Storage** -> **Local Storage** -> `https://slow.pics`. Copy the key listed there
    - To get your `sessionId`, go to **Storage** -> **Cookies** -> `https://slow.pics`. Copy the key listed under `SLP-SESSION`
    - In VSPreview, go to **Settings** -> **Comp**
    - Paste the two values in the boxes provided