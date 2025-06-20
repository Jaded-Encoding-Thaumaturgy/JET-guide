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

## General Parameters

The following parameters
are the type of parameters
you'll usually always set,
and rarely touch again.