# SVT-AV1 Parameters

This page is a high-level overview of relevant
SVT-AV1 information and parameters you should
know about to make informed encoding decisions.
Explanations behind certain parameters are
included, but the primary focus is to provide
a list of go-to parameters we recommend to make
the most out of the AV1 format.

These parameters are aimed at high-*efficiency*
video encoding, with a focus on visual appeal.
Transparency remains an area where SVT-AV1 has 
room for improvement at this point in time,
so expect some visible quality loss
even in high-bitrate scenarios.

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

Parts of this guide have been written based off the work done in
the "Deep Dive" [blog post](https://wiki.x266.mov/blog) series on the codec wiki.
Look them up if you like benchmarks, tables and graphs!

!!! warning
    The recommendations are primarily aimed at encoding *anime*,
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

Let's begin with the encoder situation.
AV1 has three publicly-available software encoders:
*aomenc*, *SVT-AV1* and *rav1e*.
The former is the reference encoder, is very slow,
and doesn't hold the efficiency crown nowadays.
The latter is coded in rust and had an interesting
psychovisual design from the ground up, however 
development stopped years ago after funding was cut.
SVT-AV1, as its full name implies, is the most scalable
encoder of the bunch, be it in performance, or in its
various usecases. We will therefore focus on that
encoder implementation that still receives frequent updates.

The SVT-AV1 code base is good, with enormous potential for 
psychovisual development. This led to many advances since 
early 2024, when the [*SVT-AV1-PSY*](github.com/psy-ex/svt-av1-psy) fork, commonly maintained
by members of the community, was introduced. Many features
that either brought QoL improvements, increased efficiency
or visual quality were upstreamed to mainline SVT-AV1,
until development of the fork stopped in early 2025.
Two new forks emerged from its remnants, [*SVT-AV1-PSYEX*](https://github.com/BlueSwordM/svt-av1-psyex/)
and [*SVT-AV1-HDR*](https://github.com/juliobbv-p/svt-av1-hdr), the former with the goal of being the
direct continuation of the *-PSY* project, and the latter
concentrating on improving perceptual fidelity on specific
grainy and HDR scenarios.

This situation isn't ideal, as it tends to split the userbase.
Fortunately, most development efforts have been merged into 
mainline SVT-AV1, so for simplicity, the recommendations in
this guide will focus on the main encoder. Readers are
encouraged to research and experiment with SVT-AV1 forks if
they wish to explore further.

SVT-AV1 can be found in most popular encoding software nowadays.

??? question "Where do I find standalone SVT-AV1 binaries?"
     It is possible to get official builds from the SVT-AV1 repository directly
     by going in the *Pipeline/Tags* tab ([direct link](https://gitlab.com/AOMediaCodec/SVT-AV1/-/pipelines?scope=tags)),
     clicking on the download button in the appropriate row for the latest version,
     and selecting the *"[Release]"* build that matches your Operating System.

     However, these builds lack any sort of compile optimizations to ensure broad
     compatibility with most systems.

     Therefore, you can alternatively get unofficial Windows binaries from this [repository](https://github.com/Patman86/SVT-AV1-Mod-by-Patman/releases),
     including *SVT-AV1-PSYEX* and *SVT-AV1-HDR* ones. Prefer Clang binaries,
     then GCC and lastly MSVC.

     Compiling SVT-AV1 is fairly easy on any platform thanks to the built-in
     build.bat / build.sh helper script. For instance, this command on a 
     Linux distro will provide an almost perfectly optimized binary for your system:
     `build.sh cc=clang cxx=clang++ jobs=$(nproc) release enable-lto native static`.
     One can try to leverage PGO or BOLT to chase the maximum possible encoding speeds.
     A basic compiling guide can be found in the [SVT-AV1 documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Build-Guide.md),
     but such compiling optimizations are better documented on the *AV1 weeb edition*
     discord server, as well as further details on the overall process.

<!-- MORE? -->

## General Parameters

The following parameters are the type of parameters
you'll usually always set, and rarely touch again.

### Preset

**Use `--preset 2` or `4`.**

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
     to give higher fidelity results compared to `2`. It is usually
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

`--tune 1` is the default in mainline SVT-AV1 and consistently wins
the efficiency crown on psychovisual metrics like SSIMULACRA2 or 
Butteraugli in the latest encoder version.

One can try to experiment with `--tune 0` which enables sharper decision
modes for many internal features of the encoder. That tune can reduce
blurring by increasing visual energy, at the expensive of additional
artifacting. It is up to the user to determine if the trade-offs are
worth it, however for the purpose of this guide and the recommended
AV1 usecase, **staying on the default `1` is preferable.**

??? info "`--tune 3`"
     A *SVT-AV1-PSY(EX)*-exclusive `--tune 3`, with psychovisual intents,
     builds on `2` (the former efficiency champion)
     while borrowing features from `0`.

     Not to be confused with *SVT-AV1-HDR*'s `--tune 3`
     which is effectively a `tune grain` equivalent.
     It disables certain features like CDEF, restoration,
     temporal filtering and sets agressive psy-rd strengths.
     It is most effective on noisy live-action content.

### Variance Boost

Usually enabled by default in SVT-AV1 forks, *varboost* is
however disabled in mainline SVT-AV1.

**Enable it with `--enable-variance-boost 1`.**

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

According to the [SVT-AV1 documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-CDEF.md),
*"The constrained directional enhancement filter (CDEF) [...] aims at improving the reconstructed picture by addressing ringing artifacts."*

The closest equivalent to this feature would be SAO in x265,
except it is not prone to the same level of detail loss.

`--enable-cdef` tends to limit edge artefacts effectively
without introducing severe *additional* line fading,
thus improving visual appeal.

Therefore, it is **recommended to leave it on.**

??? info "Specific SVT-AV1-HDR usage"

     The *SVT-AV1-HDR* fork disables CDEF in *tune 3* to hopefully increase
     grain retention consistency across the whole picture, but it is effectively
     a bruteforcing method and cannot be generalized to a more general usecase.

### Restoration Filter

According to the [SVT-AV1 documentation](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Appendix-Restoration-Filter.md),
*"The restoration filter [...] aims at improving the reconstructed picture by recovering some of the information lost during the compression process."*

In effect, `--enable-restoration` tends to increase efficiency
slightly and doesn't have any documented drawbacks, 
so it **can safely be left on** at all times.

??? info "Specific SVT-AV1-HDR usage"

     The *SVT-AV1-HDR* fork disables restoration in *tune 3* to hopefully increase
     grain retention consistency across the whole picture, but it is effectively
     a bruteforcing method and cannot be generalized to a more general usecase.

### Temporal Filtering

Temporal filtering in SVT-AV1 combines information from multiple nearby
video frames to create cleaner reference pictures with reduced noise, 
which helps improve compression quality especially for noisy source material.

The feature was often considered too strong and often created unavoidable
blocking on keyframes, so we historically disabled temporal filtering.
However *SVT-AV1-PSY* introduced a strength parameter
which has allowed to tame its effects. `--tf-strength` was backported
into mainline SVT-AV1, so it is widely available.

It is recommended to **leave `--enable-tf` on** for the efficiency benefits
it provides, but to **reduce `--tf-strength`** from its default `3` **to `1`**,
or below, to completely eliminate the tf blocking issue.

??? info "Specific SVT-AV1-PSY forks usage"

     The *SVT-AV1-PSY(EX)* and *-HDR* forks include an additional
     `--kf-tf-strength` which decouples tf strength on
     keyframes, and allows the user to concurrently 
     fix the blocking issue and use a stronger 
     tf strength on all other frames
     if one wishes so. 

For the rest of this section from this point on, it is less clear
what can be considered *better*, so more generic guidelines are given.

### Sharpness

The `--sharpness` parameter impacts the deblocking filter sharpness.

Increasing its value to `1` or `2` is a conservative way of improving
efficiency slightly, as well as perceptual quality. Higher values can
at times provide additional perceptual benefits, but they also tend to 
decrease efficiency to an extent, so it is recommended to proceed with caution.

### Tiles

AV1 tiles are a straightforward method of splitting the video frame into 
independent tiles of equal size to hopefully increase encoding and decoding
thread-ability. In SVT-AV1, tiles don't increase encoding speeds but they can
help devices (especially low-powered ones) to software decode AV1 more easily.

The following recommendation minimizes efficiency losses and provide
non-negligible benefits in decoding performance:

- `--tile-columns 1 --tile-rows 0`: at 1080p and above. 
- `--tile-columns 2 --tile-rows 1`: at 4K and above.

You can leave tiles to their default `--tile-columns 0 --tile-rows 0` if 
you don't care in the slightest about decoding speeds.

### Fast Decode

SVT-AV1 ships with its own built-in method for reducing decoding bottlenecks
by smartly tuning down or disabling specific internal tools that trade off some
efficiency for decoding performance.

The encoder offers two `--fast-decode` levels, with `2` being more aggressive.
The default is `0`. A small amount of tiles should be preferred to minimize
efficiency losses.

You can combine fast decode and tiles to decrease decoding complexity further.
Fast decode can even speed up your encoding instances, however it has been observed
that the output can be more prone to macro-blocking, so proceed with caution.

## Source-Specific Parameters

The following parameters should be adjusted
based on your specific video, and likely will
require tweaking on a case-by-case basis.

### Constant Rate Factor

For an optimal usage of the encoder, **set a Constant Rate Factor (`--crf`) value between 20 and 30.**

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

### Film Grain Synthesis

Film Grain Synthesis (FGS) is a key AV1 feature that takes the form
of additional metadata in the bitstream. Its intended goal is to help 
reconstruct grain using fewer bits than would otherwise be needed to 
preserve such grain in the actual encode. It is declined in two 
versions that produce similarly structured metadata:

- **Photon noise tables**: A single grain type applied uniformly
across the entire AV1 bitstream. This approach better matches
digital grain and has minimal impact on file size.
These static tables can be generated using tools like Av1an or
grav1synth. A comprehensive database of such tables is available
in this [repository](https://github.com/nekotrix/AV1-Photon-Noise-Tables).
You can use a photon noise table by providing its file path to the
`--fgs-table` parameter. Noise tables have no impact on encoding speeds.
- Actual **grain synthesis**: SVT-AV1 includes its own built-in FGS
implementation that dynamically adjusts grain appearance based on source
characteristics. This usually better matches the source's energy,
assuming you select an appropriate strength value for the given source.
It tends to more closely resemble analog grain. Note that due to its 
variable nature, the grain metadata can consume up to a few megabytes per 
10 minutes of encoded video, which is typically negligible for most use cases.
You can enable internal grain synthesis by setting any `--film-grain`
value between `1-50`, with higher values meaning stronger grain. An integrated
denoiser step exists (`--film-grain-denoise`) but it is terrible, so it's best
left disabled (the default behavior). Film-grain's impact on encoding speed
increases the slower your CPU is or the faster the preset in use.

Just like CRF, this process requires manual adjustment depending on
your source material.

Even in cases where grain retention is not a concern, for example with 
relatively clean sources, using **FGS is still highly recommended for its**
**forced dithering benefits**. You're probably familiar with x26x encoders'
tendency to produce poor gradients at high CRF values. You can prevent
this issue to some extent in AV1 encodes by using a photon noise ISO of
400 or higher, or a film-grain strength of 4 or higher. Lower values 
don't consistently resolve these dithering problems.

### Quantisation Matrices

QMs control the relative quantization of lower frequencies
and higher frequencies. You set a *min* and *max* allowed value
and the encoder is supposed to automatically select the most
appropriate one for the content, however the implementation
in AV1 is pretty barebone and despite efforts to improve the
feature, there is no real consensus on what QM combination
is best. Parts of the reason is that it is highly content
and CRF dependent.

Specifically, the frame QM is selected on linear interpolation
between set *min* and *max* QMs based on the frame *qindex* (qp).

`--enable-qm` still tends to improve efficiency,
especially when paired with a lower `--qm-min` than
the default `8`, so feel free to experiment with this. 

??? info "Specific SVT-AV1-PSY forks usage"
     The *SVT-AV1-PSY(EX)* and *-HDR* forks include additional
     `--chroma-qm-min` & `--chroma-qm-max` parameters
     which decouple QMs for luma and chroma, allowing
     more control over quantization, as the chroma subsampling
     tends to make the default chroma QMs too aggressive.

     It is thus recommended to keep a higher `--chroma-qm-min`
     relative to `--qm-min`.

### Luma Bias

`--luminance-qp-bias`, often abbreviated as luma bias, effectively
applies a simple qp offset to frames of lower overall brightness.

The range of accepted values is `0-100`.
The higher the value, the stronger the effect is.

This implementation has one advantage and one weakness: it gives the user
simple control over the bitrate balancing between bright and dark frames, 
however if only parts of the frame are dark and the rest is fairly bright, 
it may not fix cases of localized bitrate starving.

Still, due to how much SVT-AV1 starves dark content,
luma bias usually provides slight efficiency benefits at low strengths.
That may not always be the case if higher values
(> 50) are selected.

To better balance out bitrate allocation between bright and dark frames,
it is recommended to up `--luminance-qp-bias` and `--crf` at the same time.

## Sane Base SVT-AV1 Parameters List

Assuming a clean-ish 1080p source:

```bash
--preset 4 --enable-variance-boost 1 --tf-strength 1 --sharpness 1 --tile-columns 1 --crf 25 --film-grain 4 --luminance-qp-bias 25
```

## Fork-Specific Parameters

The following parameters have not made their way into mainline
SVT-AV1 (yet). They are mostly mentioned for reference purposes.

### QP Scale Compress Strength

This feature still exclusive to SVT-AV1 forks compresses QP values across
all temporal layers, resulting in less quality variations across frames 
in a mini-gop.

A `--qp-scale-compress-strength` value of `1` and above increases video 
quality temporal consistency.

QP scale compress strength closest equivalent in x26x encoders is a 
combination of the ipratio & pbratio settings.

### PSY-RD & SPY-RD

Psy-rd configures the rate distortion strength to improve perceived quality 
by attempting to preserve the visual energy distribution of high-frequency
details and textures, at the possible expense of increased artefacting.
The implementation is very x264-inspired at the moment.
The default `--psy-rd` is 0.5, with the highest allowed value being 6.0. 

Spy-rd configures psychovisually-oriented pathways that bias towards sharpness
and detail retention, at the possible expense of increased blocking and banding.
The default `--spy-rd` is 0, with 1 being the most aggressive and 2 being less
aggressive.

Neither features are planned for mainline merging any time soon.

### Complex HVS

`--complex-hvs 1` activates a higher quality psy-rd mode with a slightly higher
computational cost based on PSNR-HVS that is otherwise locked behind the placebo
*preset -1*.