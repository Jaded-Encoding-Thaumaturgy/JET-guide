# Codecs, Containers, and Source Filters

This page collects some of what I (arch1t3cht) know about the technical aspects of storing, packaging and loading media files.
This will not be directly useful to you when you want to learn about video filtering and encoding.
There will be very little here about the *visual* aspects of video codecs, like motion vectors, quantization, rate control, etc.;
instead the codec-related information on this page will concern concepts like NAL units, reference frames, parameter sets, and so on.
This is not usually needed when doing "normal" video filtering, but one day you will find yourself working with some sort of broken video file and will want to know what exactly is wrong with it.
After reading this page, you too can be the person to whom people go and say "Hey can you figure out why this video is broken?"

Some notes/disclaimers:

- There's a lot of things to talk about and I wanted to finish writing this so this is not structured too well.
  On the other hand, I say this about 70% of the time when writing some guide page so just judge for yourself.
- All of the information here collects my personal understanding of things and may be wrong.
- I will focus on the formats that I know the most about and/or find the most interesting.
  I know a lot about the internals of H.264 and extremely little about, say, VP9, so this page will reflect that.
  Most importantly, I know extremely little about audio (compared to video and subtitles) so it won't really appear here.

## So what are these three things?
Let's start with some extreme basics, focusing on video for now.

### Codecs
The whole story starts with video *formats*.
A video format is some specification for how a video (a sequence of pictures, each consisting of a few two-dimensional arrays of sample values) can be encoded as binary data[^binary].
More specifically, such specifications usually only specify how the binary data can be *decoded* to a video, and leave the encoding part up to others.
In the cases we care about, the main goal of a video coding format is to save as much space as possible,
which is why these formats employ many clever tricks to save every bit they can.
These tricks include:
[^binary]: Of course, when being completely precise this is only true for *digital* formats. There also exist analog video formats who have their own fun quirks and intricacies, but I won't really talk about them here.

- *Entropy coding*: Representing numbers with a varying number of bits, depending on how likely they are to occur.
      When storing a number from 0 to 255 which is 0 50% of the time and 1 another 30% of the time, it's wasteful to encode it as a simple 8-bit unsigned integer.
      Instead, one could have the bit sequence `0` represent 0, `10` represent 1, and `11xxxxxx` represent other, larger numbers.
      Using tools like [Huffman trees](https://en.wikipedia.org/wiki/Huffman_coding) one can find optimal such coding schemes for any given probability distribution of values.

      To squeeze out even more space, one can abandon the idea of having one set of bits stand for one value and vice-verse entirely and move to [*arithmetic* coding](https://en.wikipedia.org/wiki/Arithmetic_coding).
      In simple terms, arithmetic coding encodes a whole *sequence* of values using some sequence of bits (which does not necessarily split into sequences of bits corresponding to each individual value) using a technique similar to Huffman coding.

      The efficiency on Huffman and arithmetic coding depend on the accuracy of the chosen probability distributions for the values that need to be encoded.
      Modern video formats like H.264 include both large pre-determined sets of such coding coefficients, and mechanisms for updating these coefficients *on the fly* depending on previous data.
      This way, one arrives at the CAVLC (Context-based Adaptive Variable Length Coding) and CABAC (Context-based Adaptive Binary Arithmetic Coding) processes included in H.264 and (in the case of CABAC) above.

      The exact details of these codings techniques don't matter here, but the important take-away is that merely *parsing* a, say, H.264 file already needs highly complex logic, which explains the need for container formats.
      (Of course, the H.264 designers weren't stupid, and H.264 does not use CAVLC/CABAC in high-level structures like parameter sets and slice headers and makes sure that the most important bits of data (the NAL unit header and the profile and level indicators) are at fixed offsets in the relevant data structures.
      Nevertheless, the point remains that formats like H.264 are bitstreams with very complex parsing and that external metadata may be needed to answer questions like "Where in this file can I start decoding?")

- *Inter-frame coding*: Instead of every frame being encoded individually, future frames can use the content of previous frames as a reference.
      Usually, this is done by allowing each block in a frame to be *predicted* from a nearby (specified by an encoded motion vector) section (not necessarily aligned with the block grid) in a previously decoded frame,
      and then corrected further with a residual (which, if the motion prediction is good, is now closer to zero and hence easier to encode).
      Depending on the video coding format, motion predictions may also be multiplied by weights or expressed as the weighted average of blocks from multiple (usually two) different previous frames (both of which can be useful for fades) or, in newer coding formats like H.266 or AV1, apply affine transformations (like rotation, shearing, and scaling) or even certain kinds of warping instead of just translating.

      As a consequence, frames cannot be *decoded* individually.
      If one jumps into a random point in the video stream and starts decoding (setting aside for a moment all the other reasons why this may not be possible), one might arrive at a frame that references previous frames that weren't yet decoded.
      This causes the "gray screen" and/or blocky corruption that you might have seen in some video players when skipping around the video (and can be induced on purpose to achieve some fun visual effects like [datamosh](https://www.youtube.com/watch?v=nS7QvOX8LVk).)
      To decode a certain frame, a player or source filter may need to step back and start decoding at an earlier frame.
      In particular, it needs to know what earlier frame it can safely start decoding at without causing corruption.

- *Frame reordering*: Sometimes (think e.g. of a cross-fade or a scene starting by a frame wipe), the best reference frame for some block or frame is not in the past, but in the future.
      Because of this, the H.26X series of formats allow *reordering* the frames of a video when encoding, so that frames following a certain frame in *playback* order (usually called *presentation order* or *output order* in formal material) can precede it in *decoding* order.

      As a result, the n-th frame of a given video (in output order) is not necessarily the n-th frame stored in the encoded file.
      This is something that decoders and source filters have to be very aware of, and causes a large percentage of bugs and headaches when working on them.

- *Invisible frames*: For patent reasons, the VP9/AV1 family of video formats cannot use frame reordering.
      Instead, they use the "totally different, I promise!!" method where they allow marking frames as "Hidden", i.e. not to be output by the decoder, and allow instructions like "Copy this previously decoded frame to the current frame wholesale" to be encoded very efficiently (with only one or two bytes, according to the VP9 specification).
      Such frames are also sometimes called *alt-ref frames* (though this seems to be encoder-specific terminology, since I cannot find this term anywhere in the actual specifications).

      Once again, this is something that source filters need to be aware of when they want to determine where they need to start decoding to obtain the n-th frame that will actually be output.

Video coding formats are often conflated with *codecs*:
Technically, a codec (portmanteau of coder/decoder) is a concrete program or device that encodes or decodes video (or other data), as opposed to the abstract format.
However, in the multimedia community, many people use "codec" to refer to the format itself (e.g. "What codec does this video use?"), and use "encoder" and "decoder" to refer to concrete programs.
I will be committing this sin myself occasionally.

There are two sets of common video coding formats that you are likely to meet in the wild:

1. The ISO MPEG and ITU-T line of formats. These consist of (among others):
    - H.261, specified in [ITU-T Rec. H.261](https://www.itu.int/rec/T-REC-H.261).
    - MPEG-1 Part 2, specified in [ISO/IEC 11172-2](https://www.iso.org/standard/22411.html).
        This format is inspired by H.261.
    - **H.262 or MPEG-2 Part 2**, specified in [ITU-T Rec. H.262](https://www.itu.int/rec/T-REC-H.262) or [ISO/IEC 13818-2](https://www.iso.org/standard/61152.html).
        This is the video format primarily used in DVD-Video. (DVD-Video additionally supports MPEG-1 Part 2 compression for certain lower-quality formats.)
    - H.263, specified in [ITU-T Rec. H.263](https://www.itu.int/rec/T-REC-H.263).
    - MPEG-4 Part 2, specified in [ISO/IEC 14496-2](https://www.iso.org/standard/39259.html).
        This format is partially based on H.263.
        This is the format encoded by the DivX and Xvid codecs.
    - **H.264** or MPEG-4 Part 10 or AVC (Advanced Video Coding), specified in [ITU-T Rec. H.264](https://www.itu.int/rec/T-REC-H.264) or [ISO/IEC 14496-10](https://www.iso.org/standard/83529.html).
        This is by far the most ubiquitous video coding format worldwide, and will probably stay that way for at least another decade.
        It is the format primarily used in (non-UHD) Blu-rays, as well as in many other places in the web, in digital television, or in consumer-level video cameras.
        (Once again, all of these fields can use other formats, but H.264 is certainly the most common one.)
        If you plan on learning about one video format in detail, I recommend H.264.
    - **H.265** or MPEG-H Part 2 or HEVC (High Efficiency Video Coding), specified in [ITU-T Rec. H.265](https://www.itu.int/rec/T-REC-H.265) or [ISO/IEC 23008-2](https://www.iso.org/standard/85457.html). This is probably the second most common video format, but due to having a stricter patent situation, it is not natively supported in as many places as H.264. H.265 is used in UHD Blu-rays and frequently in UHD streaming.
        In particular, HDR and Dolby Vision content is usually in H.265. (H.264 was retrofitted with support for HDR metadata, but in practice H.265 is used more often.)
        A good short overview of H.265 and its differences to H.265 is given in [this IEEE paper](https://ieeexplore.ieee.org/document/6316136).
    - H.266 or MPEG-I[^mpegi] Part 3 or VVC (Versatile Video Coding), specified in [ITU-T Rec. H.266](https://www.itu.int/rec/T-REC-H.266) or [ISO/IEC 23090-3](https://www.iso.org/standard/86516.html).
        Starting with H.266, the specification for certain metadata that was mostly shared across H.264/5/6 (namely SEI and VUI) was outsourced into a separate standard document [ITU-T Rec. H.274](https://www.itu.int/rec/T-REC-H.274) or [ISO/IEC 23002-7](https://www.iso.org/standard/83530.html), and the values mappings for most VUI fields were outsourced to [ITU-T Rec. H.273](https://www.itu.int/rec/T-REC-H.273) or [ISO/IEC 23091-2](https://www.iso.org/standard/81546.html).
        A short overview of H.266 is given in [this IEEE paper](https://ieeexplore.ieee.org/document/9503377).

        At the time of writing, H.266 was finalized a few years ago, but is only just starting to be adopted:
        Support in players is extremely limited, and next to no practical encoding tooling exists.

    - MPEG-5 Part 1 or EVC (Essential Video Coding), specified in [ISO/IEC 23094-1](https://www.iso.org/standard/57797.html) is currently being developed.

2. The specifications for the formats that are part of ITU-T are freely available, but their implementation and usage is restricted by patents.
    This is why, for example, many web browsers cannot play H.265 video.
    For this reason, another popular set of formats is the VPx/AV1 line.
    This is a series of *royalty-free* standards, which is why they are, for example, supported in many web browsers.
    The most notable formats are VP8, VP9, and AV1, with AV1 being the most recent one.
    As an example, the average YouTube video provides VP9 and H.264 streams, with some videos also having AV1 streams.

There are various other coding formats (the other most notable ones being Theora, VC-1, and Apple ProRes, as well as raw formats like Y4M), but the formats listed above are the ones you're most likely to run into in the wild.

[^mpegi]: Note that the I in MPEG-I is the capital letter `i`, not the number 1.

### Containers


# TODO
- Rant about bframes vs frame reordering
- Rant about 10bit
- Everything else but the above two are ones I'm likely to forget
