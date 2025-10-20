# Descaling
Descaling can be one of the most powerful filtering techniques when used correctly,
but it can also be extremely destructive when used incorrectly.
This page introduces descaling and outlines the current state of knowledge surrounding
methods to find and judge descale parameters.

## What is Descaling?
Descaling is the process of mathematically inverting an upscaling operation.
Since conventional upscaling algorithms are linear (when ignoring rounding and clipping)
and separable, this can be done fairly efficiently by solving a system of linear equations,
provided that the parameters that were used for the upscale are known.

Descaling itself is easy; it's fully handled by
the [`descale` plugin](https://github.com/Jaded-Encoding-Thaumaturgy/vapoursynth-descale).
The much, much harder part is *finding* the parameters to descale with,
and ensuring that they are correct.
More often than not, the best decision is not to descale at all.

## Why is Descaling?
While the vast majority of modern anime is released in 1080p
(either via web streams or with BluRay releases),
many productions are not actually *produced* in that resolution.
Instead, they're animated in some lower resolution and then upscaled
to 1080p later in the production pipeline.
The original resolution can be a well-known resolution like 540p, 720p, 810p, or 900p,
but it can also have more obscure dimensions like 873 or even fractional values like 843.75.

When upscaling to 1080p, studios usually use some conventional convolutional scaling algorithm
like bilinear or some bicubic kernel.
The core idea of rescaling is to invert that upscaling process,
and reupscale the footage using some better scaling method like a Waifu2x-based one.
An example where this is especially effective is shows that have been upscaled
with BicubicSharp (the bicubic kernel with b=0 and c=1),
which causes strong aliasing and haloing.
But even for other kernels such a rescale can be a noticeable improvement.
For example, a Waifu2x-based rescale with Hermite (bicubic with b=0 c=0) as a downscaler
can completely remove halos created by upscaling while still being fairly sharp.

### Why upscale back to 1080p?
You might wonder why, after descaling to the original resolution,
the video should even be upscaled back to 1080p.
Shouldn't it be better to just leave it at its original resolution,
which is closer to the source?
Well, there are two main reasons why this isn't done:

1. Descaling can only be done to the luma.
   The video's chroma is subsampled to 960x540, so it can no longer be descaled.
   If the original resolution was, say, 720p, encoding a 720p video would mean storing
   its chroma at a resolution 640x360, which would lose even more information.
   If one was to instead encode with 444 chroma subsampling, the chroma would
   need to be upscaled to 1280x720 which creates its own problems
   (since then it'd likely still be upscaled a second time during playback).
2. Shows can rarely be descaled completely.
   Often, some elements of shows were added in 1080p after upscaling.
   One common example is credits in openings or endings.
   It's also possible for different scenes to have different native resolutions,
   or for some scenes to not be descaleable at all.

## Descaling Theory
As explained above, the difficult part in descaling is finding the parameters used to upscale
(in fact, it's easy to make *guesses* at these parameters, the hard part is determining whether one's guess is correct).
These "parameters" involve the following:

- The original width and height.
  These can be integers, but they can also be fractional values when the video was cropped after resizing or
  when the resize used a different sample grid model (see below).
- The sample grid model used when upscaling.
  VapourSynth's resize functions and the `descale` plugin use the common "match edges" model
  (see [the entropymine article](https://entropymine.com/imageworsener/matching/) for an explanation of these terms).
  When a video is upscaled from an integer resolution like 720p using a different model like "match centers",
  this is equivalent to upscaling with a non-integer source width/height (e.g. a `src_height` of `1080 * 719/1079 ≈ 719.67`)
  using a "match edges" model.
  Hence, when descaling such an upscale, these non-integer dimensions would need to be passed to the `descale` plugin.
- The kernel used for upscaling. Determining this is often the most difficult part.
- How the original upscale handled the edges of the frame,
  i.e. whether it implicitly padded width values of zero, mirrored the image, or did something else entirely.
- Any shifts that were applied when upscaling.
- Any post-processing that was applied after upscaling.
  In the vast majority of cases, post-processing after upscaling implies that your source is not descaleable,
  but if the post-processing was a somewhat reversible (ideally linear) function like convolutional sharpening, you might still have a chance.
- What color space the video was upscaled in, i.e. what color space conversions were performed after the upscale.
  Note that a nonlinear color space conversion after upscaling can make a fully accurate descale impossible.
- Whether there are any non-descaleable elements (e.g. credits) in the video or elements that'd otherwise negatively affect the descale
  and should be masked out in the descale (e.g. clipped pixels).
- The order in which the video was upscaled (horizontally, then vertically, or vice-versa).
  Since resampling is linear this is usually irrelevant, but it becomes relevant when dealing with clipped values.

Additionally, these parameters (including whether the video is descaleable at all) can vary between scenes or frames,
and the parameters for a horizontal descale can be different from the parameters for a vertical descale.
In particular, it's possible for a source to be descaleable only along one axis.
An example for this is footage that went through the HDCAM format, which subsamples luma to a width of 1440 (from 1920).
Such footage will not be horizontally descalable to its original resolution (maybe to 1440 if you're lucky),
but can sometimes still be descaled vertically.
Whether a source like this is worth descaling is a separate question.

The following sections will explain some of these parameters in more detail, as well as how to attempt to determine them.

### Source Dimensions
The source dimensions are, of course, the essential part of rescaling.
Luckily, they're also fairly easy to approximately determine.
There exist two methods for determining source resolutions:

1. The brute-force method, which simply tries descaling the source clip to a large set of resolutions,
   scales them back up with the same kernel, and graphs the total error relative to the original image.
   It turns out empirically that the resulting graph will show a spike around the "correct" resolution even
   when the kernel used in the descales is not the correct one.
2. Frequency-based methods, which exploit the behavior of convolutional resampling in the frequency domain.
   These include various different methods: On one hand, simply looking at the size of the "center blob"
   in a two-dimensional frequency plot of an image can already give an indication of whether this image was upscaled,
   and (very) approximately by how much.
   A slightly more quantitative method is to take the one-dimensional discrete cosine transform of every row (resp. column)
   and sum the entry-wise absolute values across all columns (resp. rows).
   Due to how resampling behaves in frequency space, the resulting graph will show a spike at the source resolution.
   This is the method used by the "Frequency Analysis" tab in vs-preview's native resolution plugin.

### TODO

## Evaluating Descales
The above sections explained how to find candidates for descale parameters, but ultimately these were all just heuristics.
In the end, every descale needs to be evaluated manually.
This is so important that it warrants being repeated even louder:

!!! danger "Attention"
    **NEVER** blindly decide on a descale purely based on graphs and error values.
    **ALWAYS** manually verify that your candidate parameters are correct, using the methods explained below.

Evaluating a descale entails

1. Comparing a rescale of the descaled clip with the same parameters to the original clip.
   This is the most obvious necessary condition for a descale to be correct.
   For the theoretical perfectly descaleable clip, these two should match exactly.
   In practice, there can be some slight differences due to quantization and compression noise,
   but nonetheless if a same-kernel rescale significantly differs from the original clip,
   that always means that the descale cannot be correct.
2. Inspecting the descale itself. An accurate descale will have line-art that looks "clean" at least to some degree.
   If your descale has higher-order haloing or very fuzzy-looking lines, it's likely not correct even if the rescale is very close to the descale.
   Even first-order haloing in a descale is usually an indication of an incorrect descale,
   but to our knowledge it's possible in theory (but fairly rare in the wild) for footage to have been sharpened before upscaling.

Comparing the rescale to the source or inspecting a descale is best done around sharp lines.
Exactly horizontal or exactly vertical lines are especially good indicators of rescale quality,
since around such lines the descale is essentially purely one-dimensional.
The same is true for borders when the video was upscaled using zero-padding:
here it's crucial to check whether descaling with `border_handling=1` fixes the borders or not
(and whether the rescale matches the original borders).

When searching for descales it can and will happen that you simply will not find any
set of parameters giving you satisfying results, even if you find one or more parameters
that get you closer than any other ones.
Once again, in a situation like this, the answer is usually to just give up descaling.
There are plenty of other methods to antialias or dehalo that do not carry the same risks
as incorrect descales.
Not every show has to be descaled.

### Example Code for Evaluating Descales
Here's the code snippet that I (arch1t3cht) usually use when evaluating descales.
Of course, this is just one possible method and you can just as well use any other system, including some wrapper library like vodesfunc.
The important part is that you're able to see the descale, the same-kernel rescale, and the difference clip.

```py
from vstools import get_y, depth, set_output
from vskernels import Bilinear, Catrom, BicubicSharp, Lanczos   # import more here if you need

# Load your clip here

clip = depth(get_y(clip), 32)   # take the luma and convert to 32 bits if you haven't already

set_output(clip)

for kernel in [Bilinear(), Catrom(), BicubicSharp(), Lanczos(3)]:
    desc = kernel.descale(clip, 1280, 720)
    resc = kernel.scale(desc, clip.width, clip.height)
    err = core.std.Expr([clip, resc], "x y - abs 10 *")

    set_output(desc, f"{kernel} Descale")
    set_output(resc, f"{kernel} Rescale")
    set_output(err, f"{kernel} Diff")
```

Of course, it can be freely adapted to use other kernels, another resolution
(possibly a fractional resolution, or possibly multiple resolutions using a second loop),
or other additional parameters like border handling.
You can comment out one or more of the `set_output` calls as you wish to only focus on the descales, rescales, or the difference clips.
Usually, looking at the difference clips is the easiest way to quickly rule out incorrect parameters.
In more ambiguous cases they also make it easier to find areas where the rescales are most inaccurate (e.g. horizontal/vertical lines),
which you can then investigate on the descales or rescales.
Before deciding that a rescale is accurate, you should inspect all three clips for any possible issues.

### Upscaling with the Descale Plugin
When descaling with some of the more exotic parameters like custom kernels or blur
(in which case you should make sure that you know what you're doing),
it becomes harder to rescale with the same parameters since VapourSynth's resize functions
support neither of these. In fact this problem arises even for `border_handling`
(unless you want to mess around with manually padding your clip, which can be annoying),
but there it's not as much of an issue since that doesn't affect the rest of the frame.
To help with this issue, the `descale` plugin can also upscale clips using the same parameter syntax.
For example, a BicubicSharp descale with `border_handling=1`:
```py
desc = clip.descale.Debicubic(1280, 720, b=0, c=1, border_handling=1)
```
can be reverted with the exact same keyword parameters with `core.descale.Bicubic`:
```py
resc = desc.descale.Bicubic(clip.width, clip.height, b=0, c=1, border_handling=1)
```
Unfortunately, this is not yet supported by vs-kernels.
If you want a lightweight similar alternative in the meantime, you can use the following code:
```py
class MyKernel():
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def scale(self, clip, width, height, **kwargs):
        return getattr(clip.descale, self.name)(width, height, **self.kwargs, **kwargs)
    
    def descale(self, clip, width, height, **kwargs):
        return getattr(clip.descale, "De" + self.name.lower())(width, height, **self.kwargs, **kwargs)

# Then, define your own kernels like this, which can mostly be used like vs-kernels kernels
MBilinear = MyKernel("Bilinear")
MCatrom = MyKernel("Bicubic", b=0, c=0.5)
MFFmpeg = MyKernel("Bicubic", b=0, c=0.6)
MLanczos2 = MyKernel("Lanczos", taps=2)
MLanczos3 = MyKernel("Lanczos", taps=3)
MLanczos4 = MyKernel("Lanczos", taps=4)
```
This method has its own limitations, though, since for example it does not support (de-)scaling in linear light with `linear=True`.
