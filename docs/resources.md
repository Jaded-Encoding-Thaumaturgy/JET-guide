# List of Encoding Resources
This page was originally the [Encoding Resources gist](https://gist.github.com/arch1t3cht/ef5ec3fe0e2e8ae58fcbae903f32cfe5) on my (arch1t3cht's) GitHub.
At the moment, this page is just a full copy-paste of that guide.
In the future, when this guide website grows and more topics get their own pages, some of this page's content can be moved there.

---

So this is supposed to be a list of encoding-related resources together with some very basic instructions. Kind of an encoding analogue to [fansub.html](https://tilde.club/~garret/fansub.html). This is *not* a full guide on encoding.

Since this page is starting to get linked elsewhere, I should also make clear that it mostly comes from (a person adjacent to) [the JET community](https://github.com/Jaded-Encoding-Thaumaturgy). In particular, it's written primarily from the perspective of anime encoding. Still, most parts will hold up equally well for live action and other areas.

This guide may seem fairly technical. Partly this is because I have a background in pure mathematics and this is how I learned the material, but partly it's just because encoding is cursed and complicated, and you will *need* to learn the things listed here in order to not make stupid mistakes.

Some sections contain some longer rants about stuff, most others don't. This is almost entirely based on the mood I was in when writing them.

I also give no guarantees of accuracy for any of the linked sites. I left out most links that are outdated or plain wrong, but I also did not audit every single page in detail. This is mostly just my bookmarks folder written up in markdown.

## Basics
- Most video files you'll come across are stored in a YCbCr colorspace with 4:2:0 subsampled chroma and limited color range.
- [Wikipedia article on YCbCr](https://en.wikipedia.org/wiki/YCbCr) (More info is in the colorspaces section further below)
- [Wikipedia article on chroma subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling)

### Math
Encoding is hard and technical. If you want to really understand what you're doing, you'll need a bit of math background. Some relevant topics are:

- Some basic linear algebra
- Knowing what a convolution is and how they work ([3b1b video](https://www.youtube.com/watch?v=KuXjwB4LzSA))
- Understanding Fourier transforms and, more generally, the concept of thinking in frequency space ([Imagemagick docs on Fourier transforms](https://www.imagemagick.org/Usage/fourier/))

### How to Learn
Whatever you're trying to learn (this is not even specific to encoding), it cannot be stressed enough that you should **try things out** and **use your resources**. That's the entire reason why this document exists. Sure, there might be people to ask for help on simpler topics, but some day you'll reach a point where there's no one who can answer your question and you'll need to figure it out yourself. And even before that, people will be much more willing to help you if you've shown some effort of solving your problem yourself.

## Colorspaces
- For the theory, read the [Wikipedia article on the CIE RGB Colorspace](https://en.wikipedia.org/wiki/CIE_1931_color_space)
- Zoomers that don't want to read can watch [this video](https://youtu.be/fv-wlo8yVhk?t=409) as an introduction (or at least the part that explains color spaces)
- For RGB-based colorspaces, the conversion chain is: CIE RGB -> RGB (using primaries and white point), RGB -> R'G'B' (using transfer function), R'G'B' -> Y'CbCr (using color matrix)
- For specific examples, read the articles on [BT.709](https://en.wikipedia.org/wiki/Rec._709) or [BT.601](https://en.wikipedia.org/wiki/Rec._601), or the actual standards ([BT.709](https://www.itu.int/rec/R-REC-BT.709-6-201506-I/en), [BT.601](https://www.itu.int/rec/R-REC-BT.601-7-201103-I/en))
- [Doom9 summary thread about colorspaces](https://forum.doom9.org/showthread.php?t=133982)
- [Poynton's Gamma and Colour FAQs](https://poynton.ca/notes/colour_and_gamma/)
- [The color-related articles on ImageWorsener's page](http://entropymine.com/imageworsener/)
- [List of primaries/transfer functions/matrices used in VapourSynth](http://vapoursynth.com/doc/functions/video/resize.html) The tables there being taken from the HEVC specification (Appendix E)
- [fmtconv docs](https://amusementclub.github.io/fmtconv/doc/fmtconv.html#description) also have a large list of color spaces and their relationships
- [The QuickTime Gamma Bug](https://vitrolite.wordpress.com/2010/12/31/quicktime_gamma_bug/)

### HDR
The terminology related to HDR is a huge mess, but conceptually HDR consists of two aspects

- New transfer functions (HLG and PQ) that allow for a much higher dynamic range in colors
- Formats for metadata that helps players and screens convert their HDR inputs to colors that they can display

While HDR primarily only concerns a different transfer function, it is often paired with a switch to BT.2020 primaries, even if their full gamut is not actually used (many HDR videos use the P3 gamut, for example).

A few resources:

- BT.2100, SMPTE ST 2084, SMPTE ST 2086, BT2446
- [Sheet on Dolby Vision Stuff](https://docs.google.com/spreadsheets/d/1jBIGF8XTVi9VmDBZ8a5hEyongYMCDlUiLHU9n1f_S74/edit#gid=1222148710)
- [dovi_tool](https://github.com/quietvoid/dovi_tool)
- [vs-nlq](https://github.com/quietvoid/vs-nlq): VapourSynth plugin to map DV enhancement layers. The BL needs to be 16 bit, the EL needs to be 10 bit and point-upscaled to the BL's size.

## VapourSynth
Understanding how exactly the VapourSynth ecosystem works and which parts play what roles is crucial when working with it. Otherwise, you will not be able to find the documentation you need or pinpoint where exactly your errors are coming from.

VapourSynth (at least the parts relevant for us) itself can be seen as consisting of three components:

- The core of VapourSynth is a *frame server*. It's able to chain together various functions, where each function (well, most functions) can take a sequence of video frames (or multiple sequences) together with some parameters, modify those frames in some way, and output the resulting sequence of frames (or other values).
  Such sequences of frames are called *video nodes*, and they are computed lazily: Frames are only computed when requested, and they are only requested when they're required in other functions. This allows VapourSynth to process a video frame by frame without having to store the entire clip in memory.
  Video nodes also contain *frame props*, which are pieces of data (key-value pairs) associated with each frame that functions can use and change as they please.
  
  VapourSynth offers a C/C++ api to call functions on video nodes and can load third-party *plugins* which provide functions.
  It supports common video pixel formats, but apart from that the core of VapourSynth knows next to nothing about how a video actually looks.
- On top of this architecture, VapourSynth then provides a small set of *standard* functions to perform various simple operations on video nodes.
  Some simple examples are concatenating clips, selecting or deleting frames from clips, flipping or cropping the picture, or modifying frame props.
  Some of the more sophisticated functions are the Convolution and Expr functions and the resize family of functions which can resample and convert between pixel formats.

  Furthermore, VapourSynth defines a set of reserved frame props to denote common video properties like the frame rate, sample aspect ratio, scan type, or color space.
- Finally, VapourSynth implements *Python bindings* for its filtering architecture and provides a VSScript API which allows one to run a Python script to create, process, and output video nodes.
  With these Python bindings, functions on video nodes can be called as simple member functions on the node objects, and common operations like joining or slicing can be performed using common Python operators.
  Furthermore, VapourSynth provides a simple program called `vspipe` that uses the VSScript API to execute such a Python script and output the frames it generates to then be passed to an encoder.
  This then results in the VapourSynth script workflow you probably know.

Then, there are three further components in the wider VapourSynth ecosystem:

- There are dozens of VapourSynth plugins written by users (or sometimes by the authors of VapourSynth themselves) which provide all kinds of functions to process video nodes.
  These are the filtering plugins that make up the real heart of VapourSynth
- There are various programs using the VapourSynth or VSScript APIs in order to somehow apply a filterchain or script to some video clip.
  These range from VapourSynth script editor/preview programs like VSEdit and vs-preview and utility programs for filtering like Wobbly to programs which just use VapourSynth as a means to an end to load or process video, like mpv or (forks of) Aegisub.
- There are Python libraries that provide wrappers for various existing plugins in order to cut down on boilerplate and make them easier to use with a Pythonic mindset. This is primarily the family of JET packages.

I'm placing a lot of emphasis on this distinction for two reasons: On one hand, understanding it can resolve many misconceptions about the ecosystem. VapourSynth isn't written in Python, it's written in C++ and provides Python bindings. It's completely possible to create API bindings for other languages (and has been done for some).
VapourSynth's library of standard functions is extremely useful, but in theory it would be possible to set up an entire filterchain without using a single standard function.
Python wrappers for filters are different from the filters themselves, and the two are installed and used in entirely different ways.

On the other hand, understanding the role of each piece in the machine will help you know where you need to go to find the information you need:
Want to know how to use `vsdenoise.BM3DCuda`? Well, you can check the docstrings and ask your Python language server to find out how to call it, but in the end this class is just a wrapper for the `bm3dcuda` plugin, so if you want to know what the parameters do you should read the documentation of that plugin. And if you want to know what BM3D *actually* does, you should read the paper the plugin is based on.
But then, if you're wondering what the `matrix` argument for `vsdenoise`'s `BM3DCuda` is for, well, that refers to a color matrix and you should read the docs of the VapourSynth standard library for that (as well as those of `vstools` for a more convenient wrapper, as your language server might tell you).

Now, after writing all of this, I should point out that this is not a perfect distinction, since for example it is also possible to implement filters directly in Python with certain more advanced techniques. Still, the point of explaining the VapourSynth ecosystem this way is not to give a perfect and complete description of it, but to help beginners understand how the various components interact and where various errors come from.

With this in mind, here are a couple of general resources on VapourSynth:
- [Full VapourSynth Docs](http://vapoursynth.com/doc/introduction.html)
- [List of Reserved FrameProps](http://vapoursynth.com/doc/apireference.html#reserved-frame-properties)
- [VapourSynth Standard Functions](http://vapoursynth.com/doc/functions.html)
- [Resize Docs](http://vapoursynth.com/doc/functions/video/resize.html) Also contains tables explaining the various matrix/primaries/transfer values
- Learn some basic Python. Use any resource you want, like [this one](https://www.learnpython.org/). You *need* to know basic Python if you want to write VapourSynth scripts, and people will not be very patient with you if half of your questions on VapourSynth just come from a lack of Python knowledge.

As for the various filter plugins and wrappers, there's too many of those to list here so just check their documentation.

Again, remember that Python wrappers really are just wrappers. They're very helpful if you want to *write* VapourSynth scripts without too much boilerplate, but for *learning* how certain filters work it can be very helpful to play around with the raw plugins a bit. Understanding how the plugins work will help you understand what the wrappers do.

## Filtering
This is a huge umbrella topic and the general advice still remains "Find out what filters exist for a given use case and try them out."

Keep in mind that there is no magical way to recover information, so any filter *will* be destructive to some degree. Don't use a filter if your source does not have the problem the filter is supposed to fix, or if the filter causes more issues than it fixes. Use your eyes to check for issues and do not blindly rely on automated metrics.

Recognizing artifacts:

- [guide.encode.moe's page on artifacts](https://guide.encode.moe/encoding/video-artifacts.html)
- [bakashots.me reference list for artifacts](https://bakashots.me/guide/index.php)

Unfortunately, neither of these is complete.

After giving these lists of artifacts it should be stressed *again* that you should not try to fix an artifact that isn't there. Your encoding process should be "See what artifacts the source has, then try to fix them," not "Ok, so my script should always have denoising, dehaloing, rescaling, antialiasing, debanding, and regraining." This is also the case when you cannot *see* an artifact that a source is supposed to have, even when others tell you it's there. (Though of course this means that you should try to find out what's going on and learn to spot this artifact.) If you can't see that an artifact is there, you also won't be able to judge whether your filtering fixes it.

Finally, if your source doesn't *have* any significant artifacts, that doesn't mean that you should throw filters at it to somehow still improve how it looks. It just means that maybe you don't even need to encode it.

## Resampling
- [Avisynth docs on resampling](http://avisynth.nl/index.php/Resampling)
- [Imagemagick docs on resampling](https://imagemagick.org/Usage/filter/)
- [guide.encode.moe's page on resampling](https://guide.encode.moe/encoding/resampling.html)
- [Docs for VapourSynth's Resize](http://vapoursynth.com/doc/functions/video/resize.html) This explains the meaning of parameters like `src_width` and `src_top`.
- The resampling-related articles on [ImageWorsener's page](http://entropymine.com/imageworsener/) and [ResampleScope's page](http://entropymine.com/resamplescope/)
- [Thingo I made with diagrams for all of this](https://files.catbox.moe/46dq7b.pdf)

It is extremely important to realize that upsampling and downsampling are two *fundamentally* different operations. A kernel that's good for upsampling does not need to be good for downsampling and vice-versa.

Conventional resampling (no matter if upsampling or downsampling) is linear (except for value clipping or when implicitly padding with a non-zero brightness value). This means that any horizontal resampling operation will commute with any vertical resampling operation and vice-versa.

### Upsampling
Conceptually, upsampling is divided into two steps

- Reconstruction: Convolve with the resampling kernel to obtain a continuous[^continuous] function. This step only depends on the kernel used
- Sampling: Sample the reconstructed function with a different sampling grid, determined by `width`/`height`, `src_width`/`src_height`, and `src_left`/`src_top`.

[^continuous]: Here, *continuous* means "defined on a continuous domain", as opposed to the discrete list of samples that was given as an input. The reconstructed function does not necessarily have to be continuous in the "no sudden jumps in values" sense.

Different kernels will yield different results with different artifacts. Traditional convolution-based resampling will always be a trade-off between blurring, aliasing, and ringing/haloing.

Note that *aliasing* is often conflated with *blocking*, but technically those are two different notions: Aliasing is about low frequencies incorrectly being reconstructed to high-frequencies, while blocking (more formally referred to as anisotropy) is specifically an effect of tensor resampling (and can thus only occur in 2D or higher dimensions) and is caused by the (2D) resampling kernel not being radially symmetric. Blocking can be partially alleviated by using a polar (or EWA) kernel, while aliasing cannot.

Here's some more resources on upsampling in particular

- For more mathematical background, read the [paper by Mitchell-Netravali](https://www.cs.utexas.edu/~fussell/courses/cs384g-fall2013/lectures/mitchell/Mitchell.pdf) (and if you want to dive even deeper, read some of the papers that references, like [[KEY81]](http://ncorr.com/download/publications/keysbicubic.pdf) and [[PAR83]](https://www.sciencedirect.com/science/article/abs/pii/0734189X83900269))
- [Desmos graph](https://www.desmos.com/calculator/ogo8cchpwi) visualizing the upsampling process
- [Plots of some common resampling kernels](https://amusementclub.github.io/ResampleHQ/kernels.html) Note that the Blurring/Sharpness/Ringing graphs on the bottom aren't really reliable.

### Downsampling
Downsampling is an entirely different process from upsampling. Applying the process used for upsampling to downsampling will result in massive aliasing no matter what reconstruction kernel is used. Thus, instead of asking how to best reconstruct a continuous function out of the samples like with upsampling, the main question when downsampling is how to prevent aliasing. This is done by applying a lowpass filter to reduce the high frequences that would cause aliasing. This is also indirectly covered in the Mitchell-Netravali paper.

With this in mind, good downsampling kernels are kernels that result in good lowpass filters like Gaussian kernels, or faster approximations to them like Hermite. In situations where you're worried about Moiré patterns, Mitchell is also a good candidate. But as a rule of thumb, kernels with strong negative lobes will not make good downsampling kernels, even if they're fantastic upsampling kernels.

## Descaling
The goal of a descale is to mathematically invert an upscale. *Never* descale a video unless you're absolutely sure that it was upscaled with those exact parameters, and that no additional post-processing was done afterwards.

Once you know what parameters your clip was upscaled with, the signature of the descale function should tell you everything you need to call the plugin. A descale call with given `kernel` and `src_width`, `src_height`, `src_left`, `src_top` parameters will invert a `core.resize` call with the exact same values. With a fractional descale, the parity of the width/height you're descaling to makes an important difference (and changing the parity amounts to a shift by `0.5`), but apart from the parity the width/height does not matter.

For evaluating whether your descale parameters are correct, you should check both the descale and the rescale (i.e. the upscale of the descale with the same parameters you descaled with). If the rescale's lineart looks different from the original clip, the descale cannot have been accurate. But for sharp kernels, the rescale can be very close to the original clip even for incorrect descales, so you need to check the descale too. If the descale has higher-order haloing (and usually even if it has first-order haloing[^descalehalo]), it's not going to be correct.

Rescale error is a decent metric to get estimates for a source resolution or shifts, but it's never the full story. Do not pick kernels based on lowest rescale error.

Dirty borders (when they exist) can be another indicator as to whether a descale is correct, but it seems like not all dirty borders are fixed by descales. We don't really know enough about the causes of dirty borders yet to be more certain here.

[^descalehalo]: A descale having first-order haloing is *theoretically* possible if you believe that the image was sharpened *before* upscaling, but this is very unlikely in practice. In the vast majority of cases, haloing in a descale means that the descale is incorrect.

Like (tensor) resampling, descaling is done in separate steps per axis. Furthermore, the operation is linear, so (again, except for clipping) it will commute with any resampling or descale operation along the other axis. For finding descale parameters, it can be useful to analyze the horizontal and vertical axes separately, though this can make it more difficult to visually identify correct descales. Some footage can only be descaled along one axis.

Do not descale subsampled chroma. This should be clear from the previous points but experience shows that it needs to be spelled out explicitly. Similarly, do not (horizontally) descale footage that went through the HDCAM format (and same for any other formats with subsampled luma).

## Formats and Encoders
- [Overview of the High Efficiency Video Coding (HEVC) Standard](https://ieeexplore.ieee.org/document/6316136) for a brief overview of how modern coding formats work
- For more detailed information, pick up a textbook like [High Efficiency Video Coding - Coding Tools and Specification](https://link.springer.com/book/10.1007/978-3-662-44276-0)
- The actual standards ([H.264](https://www.itu.int/rec/T-REC-H.264) and [H.265](https://www.itu.int/rec/T-REC-H.265)) probably won't help you unless you have extremely specific questions

### x264
- [Overview of x264's rate control modes (without `mbtree`)](https://code.videolan.org/videolan/x264/-/blob/master/doc/ratecontrol.txt)
- [MeGUI's x264 settings list](https://en.wikibooks.org/wiki/MeGUI/x264_Settings)
- [MeWiki's x264 settings list](http://www.chaneru.com/Roku/HLS/X264_Settings.htm)
- Use the [silentaperture guide](https://silentaperture.gitlab.io/mdbook-guide/encoding/x264.html) for decent starter settings

### x265
- x265 is based on x264 so many of the general concepts can be carried over
- [x265 docs](https://x265.readthedocs.io/en/master/cli.html)
- Use the [silentaperture guide](https://silentaperture.gitlab.io/mdbook-guide/encoding/x265.html) for decent starter settings

## IVTC
IVTC is *completely* different from deinterlacing. NEVER try to "IVTC" by calling QTGMC or anything like that. Also, never use AnimeIVTC.

- Understanding 3:2 Pulldown: [Wikipedia Page](https://en.wikipedia.org/wiki/Three-two_pull_down), [Wobbly Guide's Page on Telecining](https://wobbly.encode.moe/gettingstarted/primer.html)
- [fieldbased.media](http://fieldbased.media/)
- The basic concept of IVTC:

    Conceptually, IVTC is split into two steps, called fieldmatching and decimation. (Sometimes, it also needs additional post-processing steps like interpolating orphans, freezeframing, fixing fades, etc.)
    Fieldmatching rearranges the video's fields to try and match every field with its original counterpart. This results in a clip that ideally no longer has any combing (in practice this may not be the case due to complications like orphans, fades, etc), but will still be 30fps since it still contains duplicate frames.
    The decimation step then drops those duplicate frames to obtain a 24p clip.
    
    The Decomb docs ([here](https://www.rationalqm.us/decomb/DecombTutorial.html) and [here](https://www.rationalqm.us/decomb/DecombReferenceManual.html)) also illustrate this process pretty well.

- Understanding fieldmatching: Read the [Background and Overview](http://avisynth.nl/index.php/TIVTC/TFM#Background_and_overview:) section of the TIVTC docs
- There exist automated methods for IVTC (TIVTC, VIVTC, but note that TDecimate for VapourSynth is broken), but if you want good results you'll *need* to manually IVTC with a tool like [Wobbly](https://github.com/Jaded-Encoding-Thaumaturgy/Wobbly).
- [Wobbly Guide](http://wobbly.encode.moe/)
- [ivtc.org (archived)](https://web.archive.org/web/20220912021955/http://ivtc.vapoursynth.com/)
- [The Yatta Manifesto](https://web.archive.org/web/20160610134353/warpsharp.info/yatta.txt)

## Other SD Era Sadness (NTSC/PAL, DVDs, and all that)
- [Lurker's Guide](https://lurkertech.com/lg/) Collection of various guides on video. Includes guides like "Programmer's Guide to Video Systems" and "All about Video Fields"
- [SMPTE RP 187-1995](https://pub.smpte.org/doc/rp187/19951206-pub/)
- [A Quick Guide to Digital Video Resolution and Aspect Ratio Conversions](https://web.archive.org/web/20140218044518/http://lipas.uwasa.fi/~f76998/video/conversion/) Reference for DVD aspect ratios
- [The 625/50 PAL Video Signal and TV Compatible Graphics Modes](https://web.archive.org/web/20120802074713/http://lipas.uwasa.fi/%7Ef76998/video/modes/) Background for the previous guide, explaining the analog PAL signal in detail
- [Google Sheet on Analog Video Resolutions](https://docs.google.com/spreadsheets/d/1pzVHFusLCI7kys2GzK9BTk3w7G8zcLxgHs3DMsurF7g/edit#gid=0)
- [DVD-Video Information](https://dvd.sourceforge.net/dvdinfo/)
- [The DVD FAQ](https://dvddemystified.com/dvdfaq.html)

## Miscellaneous Stuff (mostly blogs)
- [torchlight's blog](https://mechaweaponsvidya.wordpress.com/)
- [Diary Of An x264 Developer](https://web.archive.org/web/20150419065724/http://x264dev.multimedia.cx/)
- [Falsehoods programmers believe about [video stuff]](https://haasn.dev/posts/2016-12-25-falsehoods-programmers-believe-about-[video-stuff].html)
- [Sneedex](https://sneedex.moe/) Site listing the best encodes and/or sources for many anime shows, with comparisons
- [JET Discord Server](https://discord.gg/XTpc6Fa9eB)
