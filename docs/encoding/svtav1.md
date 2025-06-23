# SVT-AV1 Parameters

This page is a very high-level overview
of relevant SVT-AV1 information and parameters
you should know about
to make informed encoding decisions.
Explanations behind certain parameters
are included,
but the primary focus is to provide
a list of go-to parameters
we recommend to make the most out of the AV1 format.

These parameters are aimed at high-efficiency video encoding,
with a focus on visual appeal.
Transparency remains an area where SVT-AV1 has 
room for improvement at this point in time,
so expect some visible quality loss
even in high-bitrate encodes.

??? info "Transparency"

     "Transparency" refers to the degree to which
     the encoded output matches the source.
     A more transparent encode will look closer to the original source,
     while a less transparent encode will have noticeable compression artifacts
     and/or distortions.

     Achieving perfect transparency is borderline impossible
     (especially once you factor in random variance such as with dithering),
     and one end goal of encoding is to have a "transparent" encode,
     a.k.a. to get as close as reasonably possible to the source.

     Given AV1's origins as a web-focused codec
     its strength lies not in achieving transparency but 
     in creating visually appealing encodes,
     that is to say small file sizes with minimal perceptible artifacts.

For a more complete look at these parameters,
see the [SVT-AV1 documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Parameters.md).

!!! warning
    These parameters are primarily aimed at encoding *anime*,
    and may not be suitable for other types of content.
    We will try to give alternative options
    for live-action content where possible,
    but a lot of parameters should still be sufficient.

    Furthermore,
    these parameters are not tailored for compatibility.
    If you're encoding for a streaming service,
    you may need to change some parameters
    and ensure you're in compliance
    with your company's requirements.

## General AV1 Knowledge

AV1 is generally less well-known than its H.26x competitors,
justifying such a section.

...
<!-- TODO -->

## General Parameters

The following parameters
are the type of parameters
you'll usually always set,
and rarely touch again.

### Preset

Use `--preset 2` or `4`.

Unlike x26x encoders, SVT-AV1 presets set
internal parameters that are not accessible
to the user. Therefore, there is no real concern
of overriding anything crucial by setting them.

??? question "How do I choose one over the other? Why not use `--preset 3`?"
     `--preset 2` is the slowest preset that showcase good efficiency 
     improvements for little speed losses. Going lower is considered
     entering placebo territory, plus there are concerns of blurrier
     visuals at slower presets.
     `--preset 4` is noticeably faster and has been reported
     to give higher fidelity results compared to `2`, it is usually
     considered a better efficiency-to-speed trade-off.
     The best course of action is to try both on your usual content,
     ideally on small test samples, and determine which one you prefer.

     `--preset 3` falls into an awkward middle ground between `2` and `4`,
     offering little compelling reason to choose it over either alternative.
     By the way, presets `5` and above are more suited for realtime usecases
     and are therefore not considered here.

### Tune

There exists three main tunes in the original SVT-AV1 implementation:
`--tune 0` (VQ, for Visual Quality),
`--tune 1` (PSNR, for Peak Signal-to-Noise Ratio) and
`--tune 2` (SSIM, for Structural Similarity Index Measure).

A *SVT-AV1-PSY(EX)*-exclusive `--tune 3`, with psychovisual intents,
builds on `2` while borrowing features from `0`.

!!! warning
    Not to be confused with *SVT-AV1-HDR*'s `--tune 3`
    which is effectively a `tune grain` equivalent.
    It disables certain features like CDEF, restoration,
    temporal filtering and sets agressive psy-rd strengths.
    It is most effective on noisy live-action content.

...
<!-- TODO -->

### Variance Boost

Usually enabled by default in SVT-AV1 forks, *varboost* is however disabled
in mainline SVT-AV1.

You can control its on or off state with `--enable-variance-boost`.

In a nutshell, *varboost* allocates more bits to low-contrast areas in a frame.
A complete rundown is available in the [SVT-AV1 documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-Variance-Boost.md).

You can control its behavior by changing its `--variance-boost-strength`
from the default `2` or its `--variance-octile` from the default `6`.
Basically, the strength controls how much areas are to be boosted,
while octile controls how much of the area needs to be deemed low-contrast
before being boosted.

Historically, metrics have shown this strength-octile combination to be
the most efficient on a wide variety of content types,
therefore it is usually not recommended to stray away from the defaults.

### Constrained Directional Enhancement Filter

According to the [official documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-CDEF.md),
"The constrained directional enhancement filter (CDEF) [...]
aims at improving the reconstructed picture by
addressing ringing artifacts."

The closest equivalent to this feature would be SAO in x265,
except it is not prone to the same level of detail loss.

`--enable-cdef` tends to limit edge artefacts effectively
without introducing severe additional line fading,
thus improving visual appeal.

Therefore, it is recommended to leave it on.

??? info "Specific SVT-AV1-HDR usage"

     The SVT-AV1-HDR fork disables CDEF in tune 3 to hopefully increase
     grain retention consistency across the whole picture, but it is effectively
     a bruteforcing method and cannot be generalized to a more general usecase.

### Restoration Filter

According to the [official documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-Restoration-Filter.md),
"The restoration filter [...] aims at improving the reconstructed picture by
recovering some of the information lost during the compression process.

In effect, `--enable-restoration` tends to increase efficiency
slightly and doesn't have any documented drawbacks, 
so it can safely be left on at all times.

??? info "Specific SVT-AV1-HDR usage"

     The SVT-AV1-HDR fork disables restoration in tune 3 to hopefully increase
     grain retention consistency across the whole picture, but it is effectively
     a bruteforcing method and cannot be generalized to a more general usecase.

### Temporal Filtering

Temporal filtering in SVT-AV1 combines information from multiple nearby
video frames to create cleaner reference pictures with reduced noise, 
which helps improve compression quality especially for noisy source material.

The feature was often considered too strong and often created unavoidable
blocking on keyframes, so we historically disabled temporal filtering.
However SVT-AV1-PSY introduced a strength parameter
which has allowed to tame its effects.

It is recommended to leave `--enable-tf` on for the efficiency benefits
it provides, but to reduce `--tf-strength` from its default `3` to `1`,
or below, to completely eliminate the tf blocking issue.

??? info "Specific SVT-AV1-PSY forks usage"

     The SVT-AV1-PSY(EX) and -HDR forks include an additional
     `--kf-tf-strength` which decouples tf strength on
     keyframes, and allows the user to concurrently 
     fix the blocking issue and use a stronger 
     tf strength on all other frames
     if you wishes so. 

### Quantisation Matrices

...
<!-- TODO -->

### Luma Bias

...
<!-- TODO -->

### Sharpness

...
<!-- TODO -->

### Tiles

...
<!-- TODO -->

### Fast Decode

...
<!-- TODO -->

## Source-Specific Parameters

The following parameters
should be adjusted
based on your specific video,
and likely will require tweaking
on a case-by-case basis.

### Constant Rate Factor

For an optimal usage of the encoder, set a Constant Rate Factor (CRF) value between 20 and 30

CRF is a rate control mode that aims to achieve a consistent quality level across the entire video.
Lower values result in higher quality and larger file sizes,
while higher values lead to lower quality and smaller file sizes.

We recommend using CRF values between 20 and 30
to achieve high-efficiency, appealing encodes.
This range typically provides the best balance
between visual appeal and file size for most content.

If you need to go below 20, you may achieve better results
with encoders better suited for high-fidelity like x265.

!!! warning "Lower resolution encodes may require a lower CRF value"
     Lower resolution encodes may require a lower CRF value
     to achieve the same level of quality as higher resolution encodes.
     This is due to the fact that lower resolution encodes
     will be upscaled during playback,
     which makes quantization artifacts more noticeable.
     For SD content,
     you may need to use a CRF value of 20 or lower.



...
<!-- TODO -->

### Film Grain Synthesis

...
<!-- TODO -->