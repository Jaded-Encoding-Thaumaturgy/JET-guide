# General settings

These are the settings that you shouldn't touch between encodes.

## Preset

Presets apply a number of parameters, which can be referenced [here](https://dev.beandog.org/x264_preset_reference.html)
Just use the placebo preset, we'll change the really slow stuff, anyway:

```
--preset placebo
```

## Level
Where --preset applies a defined set of parameters, --level provides a set of limitations to ensure decoder compatibility. For further reading, see this [Wikipedia article](https://en.wikipedia.org/wiki/Advanced_Video_Coding#Levels)

For general hardware support level 4.1 is recommended, otherwise you may omit this.

```
--level 41
```

## Motion estimation
For further reading [see this excellent thread on Doom9](https://web.archive.org/web/20210516085632/https://forum.doom9.org/showthread.php?p=1789660)

x264 has two motion estimation algorithms worth using, umh and tesa.
The latter is a placebo option that's really, really slow, and seldom yields better results, so only use it if you don't care about encode time.
Otherwise, just default to umh:

```
--me umh
```

## Ratecontrol lookahead

The ratecontrol lookahead (rc-lookahead) setting determines how far ahead the video buffer verifier (VBV) and macroblock tree (mbtree) can look.
Raising this can slightly increase memory use, but it's generally best to leave this as high as possible:

```
--rc-lookahead 250
```

If you're low on memory, you can lower it to e.g. 60.

# Source-specific settings

These settings should be tested and/or adjusted for every encode.

## Ratecontrol

Beyond all else, this is the single most important factor for determining the quality from any given input. Due to how poorly x264 handles lower bitrates (comparatively, particularly when encoding 8-bit) starving your encode will result in immediate artifacts observable even under the lightest scrutiny.

While manipulating other settings may make small, but usually noticeable differences; an encode can't look great unless given enough bits.

For some further insight, reference [this article](https://github.com/jpsdr/x264/blob/master/doc/ratecontrol.txt)

### Constant ratefactor

For more information please see [this post by an x264 developer](https://forum.doom9.org/showthread.php?p=1261917#post1261917).

The constant ratefactor (CRF) is the suggested mode for encoding.
Rather than specifying a target bitrate, CRF attempts to ensure a consistent quality across a number of frames; as such, the resulting bitrate will only be consistent if passed identical values.
In short, CRF is recommended for use with your finalized encode, not testing, where two pass is recommended.

Lower CRF values are higher quality, higher values lower.
Some settings will have a very large effect on the bitrate at a constant CRF, so it's hard to recommend a CRF range, but most encodes will use a value between 15.0 and 20.0.
It's best to test your CRF first to find an ideal bitrate, then test it again after all other settings have been tested with 2pass.

To specify CRF:

```
--crf 16.9
```

### Two pass

An alternative to CRF which leverages an initial pass to collect information about the input before encoding. This comes with two distinct advantages:

* The ability to target a specific bitrate
* Effectively infinite lookahead

This is very suitable for testing settings, as you will always end up at almost the same bitrate no matter what.

As mentioned previously, to encode this two runs are necessary. The first pass can be sent to /dev/null, since all we care about is the stats file.
To specify which of the two passes you're encoding all we need to change is ``--pass``

```
vspipe -c y4m script.vpy - | x264 --demuxer y4m --preset placebo --pass 1 --bitrate 8500 -o /dev/null -
```

```
vspipe -c y4m script.vpy - | x264 --demuxer y4m --preset placebo --pass 2 --bitrate 8500 -o out.h264 -
```

#### Chroma quantizer offset

If you're struggling with chroma getting overly distorted, it can be worth tinkering with this option.
You can find examples of what bitstarved chroma can look like [HERE](https://silentaperture.gitlab.io/mdbook-guide/encoding/images/godfather_road_sky.png) and [HERE](https://silentaperture.gitlab.io/mdbook-guide/encoding/images/godfather_plane_split.png).
Lower values give more bits to chroma, higher values will take away.
By default, this will be -2 for 4:2:0 and -6 for 4:4:4.
Setting this will add your offset onto -2.

To lower the chroma QP offset from -2 to -3, granting chroma more bits:

```
--chroma-qp-offset -1
```

## Deblock

For an explanation of what deblock does, read [this Doom9 post](https://forum.doom9.org/showthread.php?p=1692393#post1692393) and [this blog post](https://web.archive.org/web/20220323033558/https://huyunf.github.io/blogs/2017/11/20/h264_deblocking_algorithm/)

Set this too high and you'll have a blurry encode, set it too low and you'll have an overly blocky encode.
We recommend testing deblock in a range of `-2:-2` to `0:0` (animated content should use stronger deblock settings).
Usually, you can test this with the same alpha and beta parameters at first, then test offsets of ±1.

Many people will mindlessly use -3:-3, but this tends to lead to unnecessary blocking that could've been avoided had this setting been tested.

To specify e.g. an alpha of -2 and a beta of -1:

```
--deblock -2:-1
```

## Quantizer curve compression

The quantizer curve compression (qcomp) is effectively the setting that determines how bits are distributed among the whole encode.
It has a range of 0 to 1, where 0 is a constant bitrate and 1 is a constant quantizer, the opposite of a constant bitrate.
This means qcomp affects how much bitrate you're giving to "important" scenes as opposed to "unimportant" scenes.
In other words, it can be seen as the trade-off between bitrate allocation to simple or static scenes and complex or high motion scenes.
Higher qcomp will allocate more to the latter, lower to the former.

It's usually recommended to set this between `0.60` and `0.70` without mbtree and `0.70` and `0.85` with mbtree.
You want to find that sweet spot where complex scenes will look good enough without ruining simple scenes.

```
--qcomp 0.60
```

## Macroblock tree

From [this thread by an x264 developer](https://forum.doom9.org/showthread.php?t=148686): "It tracks the propagation of information from future blocks to past blocks across motion vectors. It could be described as localizing qcomp to act on individual blocks instead of whole scenes. Thus instead of lowering quality in high-complexity scenes (like x264 currently does), it'll only lower quality on the complex part of the scene, while for example a static background will remain high-quality. It also has many other more subtle effects, some potentially negative, most probably not."

Curious readers can reference the [paper directly](https://archive.org/download/x264_mbtree/x264_mbtree.pdf)

Macroblock tree ratecontrol (mbtree) can lead to large savings for very flat content, but tends to be destructive on anything with a decent amount of grain.
If you're encoding something with very little movement and variation, especially cartoons and less grainy digital anime, it's recommended to test this setting to see if it's worth it.

When using mbtree, you should max out your lookahead (`--rc-lookahead 250`) and use a high qcomp ≥0.70.

## Adaptive quantization

While qcomp determines bit allocation for frames across the video, adaptive quantization (AQ) can be seen as in charge of doing this on a block-basis, i.e. throughout a frame.
It does so by distributing bits from higher contrast areas to lower contrast regions.
This is done because, while lower contrast areas are mathematically less significant, the human eye considers them of equal importance.

For more on this, the explanation in [this document](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-Variance-Boost.md) is quite helpful.
[This post](https://huyunf.github.io/blogs/2017/12/06/x264_adaptive_quant/) grants a bit of insight on the implementation in x264.

There are three modes available in vanilla x264:

1. Allow AQ to redistribute bits across the whole video and within frames.
2. Auto-variance; this attempts to adapt strength per-frame.
3. Auto-variance with a bias to dark scenes.

Generally speaking, you'll likely get the best results with AQ mode 3.
With the other two modes, you have to carefully make sure that darks aren't being damaged too much.
If you e.g. have a source without any dark scenes (or only very few), it can be worth manually allocating more bits to darks via [zoning](#zones) and using AQ modes 1 or 2.

This comes along with a strength parameter.
For modes 1 and 2, you usually want a strength between 0.80 and 1.30.
Mode 3 is a bit more aggressive and usually looks best with a strength between 0.60 and 0.85.

Raising the AQ strength will help flatter areas, e.g. by maintaining smaller grain and dither to alleviate banding.
However, higher AQ strengths will tend to distort edges more.

Older, grainier live action content will usually benefit more from lower AQ strengths and may benefit less from the dark scene bias present in AQ mode 3, while newer live action tends to benefit more from higher values.
For animation, this setting can be very tricky; as both banding and distorted edges are more noticeable.
It's usually recommended to run a slightly lower AQ strength, e.g. around 0.60 to 0.70 with mode 3.

To use e.g. AQ mode 3 with strength 0.80:

```
--aq-mode 3 --aq-strength 0.80
```

### AQ dark bias strength

Some mods now include a parameter to control AQ mode 3's bias to dark scenes strength.
With this, the dark bias strength is a multiple of the AQ strength, meaning higher bias strength raises the dark bias and lower bias strength trends towards AQ mode 2.

This can be very useful in cases where you want to give more or fewer bits to darks without affecting the AQ strength.
To apply an AQ dark bias strength of 1.00:

```
--aq-mode 3 --aq-bias-strength 1.00
```

## Motion estimation range

The motion estimation range (merange) determines how many pixels are used for motion estimation.
Larger numbers will be slower, but can be more accurate for higher resolutions.
However, go too high, and the encoder will start picking up unwanted info, which in turn will harm coding efficiency.
You can usually get by with testing `32`, `48`, and `64`, then using the best looking one, preferring lower numbers if equivalent:

```
--merange 32
```

## Frame type quantizer ratio

To understand this parameter, one needs to know what the different frame types are.
The [Wikipedia article](https://en.wikipedia.org/wiki/Video_compression_picture_types) on this subject is very useful for this.

These settings determine how bits are distributed among the different frame types.
Generally speaking, you want to have an I-frame to P-frame ratio (ipratio) around 0.10 higher than your P-frame to B-frame ratio (pbratio).
Usually, you'll want to lower these from the defaults of `1.40` for ipratio and `1.30` for pbratio, although not by more than 20.

Lower ratios will tend to help with grainier content, where less information from previous frames can be used, while higher ratios will usually lead to better results with flatter content.

You can use the stats created by the x264 log at the end of the encoding process to check whether the encoder is over-allocating bits to a certain frame type and investigate whether this is a problem.
A good guideline is for P-frames to be double the size of B-frames and I-frames in turn be double the size of P-frames.
However, don't just blindly set your ratios so that this is the case.
Always use your eyes.

To set an ipratio of `1.30` and a pbratio of `1.20`:

```
--ipratio 1.30 --pbratio 1.20
```

If using mbtree, pbratio doesn't do anything, so only test and set ipratio.

## Psychovisually optimized rate-distortion optimization

One big issue with immature encoders is that they don't offer psychovisual optimizations like psy-rdo.
What it does is distort the frame slightly, sharpening it in the process.
This will make it statistically less similar to the original frame, but will look better and more similar to the input.
What this means is this is a weak sharpener of sorts, but a very much necessary sharpener!

The setting in x264 comes with two options, psy-rdo and psy-trellis, which are both set via the same option:

```
--psy-rd rdo:trellis
```

Unfortunately, the latter will usually do more harm than good, so it's best left off.
The psy-rdo strength should be higher for sharper content and lower for blurrier content. For animated content, psy-rdo can introduce ringing even with default values. We suggest using lower values, between  `0.60` and `0.90`. For live action content where this is of much lesser concern you should find success with values around `0.95` to `1.10`. 

When testing this, pay attention to whether content looks sharp enough or too sharp, as well as whether anything gets distorted during the sharpening process.

For example, to set a psy-rd of 1.00 and psy-trellis of 0:

```
--psy-rd 1.00:0
```

## DCT block decimation

Disabling DCT block decimation (no-dct-decimate) is very common practice, as it drops blocks deemed unimportant.
This importance decision is made by checking if there are enough nonzero large coefficients, i.e. whether higher frequencies are present.
For high quality encoding, this is often unwanted and disabling this is wise.
However, for flatter content, leaving this on can aid with compression.
Just quickly test on and off if you're encoding something flat.

To disable DCT block decimation:

```
--no-dct-decimate
```

## Video buffer verifier

To understand what this is, there's actually a [Wikipedia article you can read](https://en.wikipedia.org/wiki/Video_buffering_verifier). Alternatively, you may find [this video presentation](https://www.youtube.com/watch?v=-Q7BuSXdO_8) from demuxed informative.

For us, the main relevance is that we want to disable this when testing settings, as video encoded with VBV enabled will be non-deterministic.
Otherwise, just leave it at your level's defaults.

To disable VBV:

```
--vbv-bufsize 0 --vbv-maxrate 0
```

VBV settings for general hardware compliance (High@L4.1)
```
--vbv-bufsize 78125 --vbv-maxrate 62500
```

## Reference frames

The reference frames (ref) setting determines how many frames P frames can use as reference. Many existing guides may provide an incorrect formula to find the 'correct' value. **Do not use this**. Rather, allow x264 to calculate this for automatically (as dictated by `--level`). 

Otherwise, if you don't care about compatibility with 15 year old TVs and 30 year old receivers, set this however high you can bare, with a maximum value of 16.
Higher refs will improve encoder efficiency at the cost of increased compute time.

To set the maximum value of 16:

```
--ref 16
```

## Zones

Sometimes, the encoder might have trouble distributing enough bits to certain frames, e.g. ones with wildly different visuals or sensitive to banding.
To help with this, one can zone out these scenes and change the settings used to encode them.

When using this to adjust bitrate, one can specify a CRF for the zone or a bitrate multiplier.
It's very important to not bloat these zones, e.g. by trying to maintain all the grain added while debanding.
Sane values tend to be ±2 from base CRF or bitrate multipliers between `0.75` and `1.5`.

To specify a CRF of 15 for frames 100 through 200 and 16 for frames 300 through 400, as well as a bitrate multiplier of 1.5 for frames 500 through 600:

```
--zones 100,200,crf=15/300,400,crf=16/500,600,b=1.5
```

For a more complete picture of what --zones can and can not manipulate, see [this section](https://www.chaneru.com/Roku/HLS/X264_Settings.htm#zones).

## Output depth and color space

To encode 10-bit and/or 4:4:4 video, one must specify this via the following parameters:

```
--output-depth 10 --output-csp i444
```

