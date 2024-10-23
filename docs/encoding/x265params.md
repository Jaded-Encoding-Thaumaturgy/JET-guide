# x265 Parameters

This page is a very high-level overview
of relevant x265 parameters
you should use
and modify as necessary.
Explanations behind certain parameters
are included,
but the primary focus is to provide
a list of go-to parameters
we recommend for high-quality video encoding.

These parameters are aimed at high-quality video encoding,
with a focus on transparency.
The files will naturally wind up fairly large,
but that's preferable over them being bitstarved.

??? info "Transparency"

     "Transparency" refers to the degree to which
     the encoded output matches the source.
     A more transparent encode will look closer to the original source,
     while a less transparent encode will have noticeable compression artifacts
     and/or distortions.

     Achieving perfect transparency is borderline impossible
     (especially once you factor in random variance such as with dithering),
     but the end goal should be to have a "transparent" encode,
     a.k.a. to get as close as reasonably possible.

For a more in-depth look at these parameters,
see the [x265 documentation](https://x265.readthedocs.io/en/stable/cli.html).

!!! warning
    These parameters are primarily aimed at encoding *anime*,
    and may not be suitable for other types of content.
    We will try to give alternative options
    for live-action content where possible,
    but a lot of parameters should still be sufficient.

    Furthermore,
    these parameters are tailored to piracy-scene encoding.
    If you're encoding for a streaming service
    or authoring company,
    you may need to change some parameters
    and ensure you're in compliance
    with your company's requirements.

## General Parameters

The following parameters
are the type of parameters
you'll usually always set,
and rarely touch again.

### Preset

Use the `veryslow` or `slower` preset.

These presets will still set some parameters
that aren't useful,
but we will override them with better values later.

??? question "Why not use `--tune animation`?"
     `--tune animation` is a preset that is designed to work well with "animation".
     However,
     the type of animation this appears to be optimized for
     is not anime or anything with similarly complex backgrounds,
     gradients, and other details.
     Instead,
     this tune is better optimized for very "flat" animation,
     such as flash animations and things of that nature.

     For that reason,
     you should **NOT** use this tune for anime.

### Threads

...
<!-- TODO: Add explanation -->

### Sample Adaptive Offset

Disable sample adaptive offset using `--no-sao`.

Sample Adaptive Offset (SAO) aims to reduce visual artifacting, particularly around edges.
However, it's very prone to creating detail loss.
It's best to avoid using it
unless you're trying to encode a mini-encode.

### CU Tree

Disable CU tree using `--no-cutree`.

CU Tree is a rate control algorithm that allocates bits based on the complexity of each Coding Unit (CU).
This often leads to simpler areas (such as backgrounds) being starved of bitrate,
creating noticeable blocking artifacts.
There's also no way to fully control its behavior (or "strength"),
so it's best to just disable it.
Turning it off allows for a more even distribution of bits across the frame,
which will look closer to the original video
and prevent "patches" of starved areas.

### Adaptive Quantization Mode

Use `--aq-mode 3`.

Adaptive Quantization (AQ) adjusts the quantization level for different parts of the frame based on their complexity.
This helps distribute bits more efficiently across the image,
allocating more bits to complex areas and fewer to simpler areas.

Using `--aq-mode 3` enables AQ with auto-variance and a bias towards dark scenes.
This mode is particularly effective for anime content for several reasons:

1. It helps preserve detail in darker areas, which are common in anime and often prone to banding or blocking artifacts.
2. The auto-variance feature adapts the strength of AQ based on the overall variance of the frame.
3. The bias towards dark scenes helps maintain the integrity of shadows and prevents loss of detail in low-light areas,
   which is crucial for maintaining the artistic intent in many anime scenes.

### B-**Frames**

Use at least 8 B-Frames,
and ideally 16
using `--bframes 16`.

Higher values will reduce encoding speed,
so only use 16 if you don't mind that cost.
If you desperately need the speed,
you can go lower,
but don't go below 8.

### Deblock

Use at least `--deblock=-1:-1`
or `--deblock=-2:-2`.
If you're encoding live-action content,
stick with `--deblock=-2:-2`.

Deblocking will affect how much smoothing is applied.
This can be harmful to dithering and grain,
so you should avoid deblocking.
However,
setting it to its lowest value (`-3:-3`)
may _create_ noticeable blocking artifacts instead.

### Transform Skip

Enable transform skip using `--tskip`
if you're encoding anime.

Transform skip enables the evaluation of skipping the transform (DCT) step for 4x4 transform units,
while still applying quantization.
This is useful for preserving sharp edges and fine details,
which anime often has a lot of.

### Chroma QP Offset

Use at least `--cbqpoffs -2`,
or `--cbqpoffs -3`
if you don't mind the additional file size.

This parameter affects the quantization parameter (QP)
for chroma (color) components relative to the luma QP.
A negative value reduces the chroma QP,
allocating more bits to chroma and potentially improving color quality.

Chroma often receives fewer bits than luma,
which can lead to color quality suffering.
This offset helps correct for that by allowing more bits for chroma,
effectively reducing the quantization step size for color information.

## Source-Specific Parameters

The following parameters
should be adjusted
based on your specific video,
and likely will require tweaking
on a case-by-case basis.

### Constant Rate Factor

Use a Constant Rate Factor (CRF) value between 12 and 14

CRF is a rate control mode that aims to achieve a consistent quality level across the entire video.
Lower values result in higher quality and larger file sizes,
while higher values lead to lower quality and smaller file sizes.

For anime,
we recommend using CRF values between 12 and 14
to achieve high-quality, transparent encodes.
This range typically provides an excellent balance
between visual quality and file size for anime content.

!!! warning "Lower resolution encodes may require a lower CRF value"
     Lower resolution encodes may require a lower CRF value
     to achieve the same level of quality as higher resolution encodes.
     This is due to the fact that lower resolution encodes
     will be upscaled during playback,
     which makes quantization artifacts more noticeable.
     For SD content,
     you may need to use a CRF value of 9 or lower.

If you notice that your encode is still too starved,
or that grain and dithering are patching together,
you may need to decrease the CRF value slightly.

### Quantization Compression Ratio

Use `--qcomp 0.7`.

The Quantization Compression Ratio (qcomp) controls how the quantizer varies within a frame.

A value of `0.7` is generally a good starting point for most anime content.
However, if you're working with very grainy content,
you may want to increase the value slightly.

### Adaptive Quantization Strength

Use an `--aq-strength` value between 0.6 and 0.7.

Adaptive Quantization (AQ) helps distribute bits more efficiently across a frame.
For anime content,
it's generally recommended to keep the AQ strength relatively low.
Lower values reduce QP fluctuations,
which can result in better-looking grain,
especially in motion.

Values between `0.6` and `0.7` typically work well for most anime,
but when working with very grainy content,
you may need to decrease the value slightly.
Be cautious about setting the value too low,
as some degree of adaptive quantization
is still beneficial for overall picture quality.

### Psychovisual Optimization

Use `--psy-rd 2.0` and `--psy-rdoq 2.0`,
and avoid values higher than `2.5`.

The `--psy-rd` parameter controls the strength of psychovisual optimization
during the rate-distortion optimization process.
A value of `2.0` is generally a good starting point for anime,
as it helps preserve detail and texture without introducing too many artifacts.

The `--psy-rdoq` parameter affects the psychovisual optimization during
quantization. Like `--psy-rd`, a value of `2.0` is often suitable for anime content.

These parameters can be quite sensitive,
and their effects may vary depending on the specific content.
Higher values will try to match the source structure more aggressively,
which can help preserve grain and detail.
However, they may also introduce noticeable distortions if set too high.

### Keyframe Interval

Use a keyframe interval of 240
using `--keyint 240`
and a minimum keyframe interval of 24
using `--min-keyint 24`.

These parameters help control where I-frames (or "keyframes") are placed.
In most scenarios,
you want I-frames to be as spread out as possible,
so that you can get the benefits of B-Frames
while minimizing the bitrate cost.

A good rule of thumb is to set the keyframe interval to 10 seconds of content,
and the minimum keyframe interval to 1 second.
This means if your content is 24 fps,
your keyframe interval should be 240,
and your minimum keyframe interval should be 24.
If your content is 30 fps,
your keyframe interval should be 300,
and your minimum keyframe interval should be 30.

### Rate Distortion Optimization Mode

`--rd 4` makes RDO act more like x264,
with more similar artifacting such as blurring and blocking.
`--rd 6` will create more noticeable distortion patterns,
but can also hold grain together better in certain scenarios.

`4` is usually the best choice for anime,
but depending on the type of grain your content has,
you may want to experiment with `6`.

### IP/P/B Ratio

The IP ratio (`--ipratio`) and PB ratio (`--pbratio`)
control the relative quality of I-frames, P-frames, and B-frames.
These parameters can be useful for fine-tuning the balance
between different frame types.

If you notice degradation with specific frame types,
tweaking these ratios may help:

- `--ipratio`: Controls the ratio of bits allocated to I-frames relative to P-frames.
  A higher value allocates more bits to I-frames.
- `--pbratio`: Controls the ratio of bits allocated to P-frames relative to B-frames.
  A higher value allocates more bits to P-frames.

Default values are often sufficient,
but if you're experiencing issues with certain frame types,
you might want to adjust these.
For example:

- If I-frames look noticeably worse than other frames, try increasing `--ipratio`.
- If P-frames are causing issues, you might adjust both `--ipratio` and `--pbratio`.

These parameters will be mostly useful on very grainy content.


