# Recognizing Video/Compression Artifacting

!!! warning "Stub"
    This page is a [stub][wikipedia-stubs].
    You can help by [expanding it][contributing].

    !!! abstract "Extra information"
        Missing a variety of example images.
        Please try to keep the examples diverse,
        and use as many different consumer sources as possible.

!!! warning "This list is not exhaustive"
    Due to the nature of video compression and mastering,
    there are infinitely many types of artifacting that can occur.
    This document aims to capture the most common types,
    but there are many more that are not covered here.

    If you're unsure if something is an artifact,
    you should err on the side of caution
    or ask in the [JET Discord][discord].

Artifacting is a broad term that encompasses any video-encoding related error or unwanted distortion
that manifests in a change in the decoded image.
This can occur due to improper mastering,
poor compression,
or a number of other reasons introduced during the authoring or encoding chain.

Understanding what is and isn't an artifact is key
to being able to effectively filter your video
without introducing new artifacts
or causing unwanted detail loss.

## What is _not_ an artifact?

Some video effects are intentional and not considered artifacts.
You should avoid filtering these,
as they are often an artistic choice
or a fundamental part of the video
that is difficult to alter without causing other issues.

### Grain

Grain is a visual noise that can be added to a video to give it a nostalgic atmosphere or to make it appear more realistic. There are two types of grain: analog and digital.

!!! example "Different types of grain"
    === "Digital grain"

        Digital grain is added in post-production.

        It is a simulation of the analog film grain effect
        and is usually a semi-randomly generated pattern of brighter/darker pixels.
        It's often used in digital compositing
        to give the scene a more nostalgic or gritty look,
        or to make the video appear more realistic.

        === "Example A"

            ![An example of digital grain][placeholder-image]

        === "Example B"

            ![An example of digital grain][placeholder-image]

        === "Example C"

            ![An example of digital grain][placeholder-image]

    === "Analog grain"

        Analog grain is a characteristic of _film_.

        It is created by the physical properties of the film stock itself,
        often due to the presence of silver halide crystals.
        As the film ISO increases, more silver is added,
        making the film more sensitive to light.
        This results in a texture that is an integral part of the image,
        with grain size and density affecting the overall aesthetic.

        === "Example A"

            ![An example of analog grain][placeholder-image]

        === "Example B"

            ![An example of analog grain][placeholder-image]

        === "Example C"

            ![An example of analog grain][placeholder-image]

Grain is often mistaken for compression noise,
but there are ways to distinguish the two:

1. **Pattern**:<br>
    Analog grain has a consistent pattern due to the physical properties of the film,
    while digital grain is mostly uniformly applied.<br>
    Compression noise does not follow a consistent pattern.
2. **Strength**:<br>
    Grain, whether analog or digital,
    is usually more pronounced and spans the entire frame.<br>
    Compression noise is typically smaller
    and more localized to specific areas of the frame.

!!! warning "Compression"
    Grain itself is not an artifact,
    but due to the nature of compression,
    strong compression noise will often form on grainy content.

Regular denoising filters with sane settings should not remove (much) grain,
and target mostly compression noise.
If your denoising settings are too strong,
you may remove patches of grain,
creating a half-grain/half-flat area effect,
which can look jarring.

### Poorly drawn lineart

Poorly drawn lineart,
while unwanted,
is not considered an artifact.
It is a fundamental aspect of the video
and should not be filtered out.

Exceptions may be made,
but you should only do so in extreme cases
where the lineart is so poor that it is distracting.
When doing this,
always scenefilter this.

!!! example "Examples of poorly drawn lineart"
    === "Example A"

        ![An example of poorly drawn lineart][placeholder-image]

    === "Example B"

        ![An example of poorly drawn lineart][placeholder-image]

    === "Example C"

        ![An example of poorly drawn lineart][placeholder-image]

### Digital chromatic aberration

Chromatic aberration is a natural optical phenomenon
that occurs when light passes through different media,
such as a lens or prism,
causing different colors to refract at different angles.
This can result in color fringing around objects in the video.

This is an artifact when dealing with analog film,
but is often used intentionally in digital compositing
to achieve a particular stylistic look
or to simulate lens imperfections
to make the video appear more realistic.

!!! example "Examples of digital chromatic aberration"
    === "Example A"

        ![An example of digital chromatic aberration][placeholder-image]

    === "Example B"

        ![An example of digital chromatic aberration][placeholder-image]

    === "Example C"

        ![An example of digital chromatic aberration][placeholder-image]

## Common types of artifacting

!!! question "So how do I fix this artifact?"
    This document aims to capture the most common types of artifacting,
    but does not cover how to filter them.<br>
    For more information,
    refer to the filtering guides for each type
    or filters included with the relevant JET packages.

Below are the most common types of video/compression artifacting
that can be reasonably filtered out.

### Color banding

Color banding is a common artifact in video compression
that occurs when the color information in a video frame
is not evenly distributed.
This can result in visible bands of color
or uneven brightness in the video.

There are two common sources of color banding:

!!! example "Color banding"
    === "Compression"

        Color banding often results from insufficient bitrate being given to the video during compression.
        When a video lacks the necessary data to accurately represent color transitions,
        it creates visible "bands" or blobs of color instead of smooth gradients.

        This type of banding is particularly noticeable in darker scenes,
        because the standard gamma curves are the most imprecise relative to human vision.
        However, it can be noticeable in brighter scenes as well.

        === "Example A"

            ![An example of color banding caused by compression][placeholder-image]

        === "Example B"

            ![An example of color banding caused by compression][placeholder-image]

        === "Example C"

            ![An example of color banding caused by compression][placeholder-image]

    === "Bitdepth conversion"

        Color banding can occur when converting video from higher to lower bitdepth
        without proper dithering.

        For instance, converting 10-bit video to 8-bit without adequate dithering
        can result in a loss of color information,
        as pixel values must be rounded.
        This can result in visible bands of color.

        Common scenarios include:

        - Converting HDR to SDR content
        - Downscaling professional 10-bit footage to consumer 8-bit formats

        === "Example A"

            ![An example of color banding caused by compression][placeholder-image]

        === "Example B"

            ![An example of color banding caused by compression][placeholder-image]

        === "Example C"

            ![An example of color banding caused by compression][placeholder-image]


??? question "Which package contains filters to fix this?"

    The [vs-deband] package contains filters specifically designed to address color banding issues.


### Quantization error

Quantization error is an umbrella term
for unwanted artifacts that result from quantization.
These artifacts are most noticeable around sharp edges
or in areas of high contrast.

The most common perceptual defects are:

- **Blocking**
- **Noise**
- **Ringing**

The way quantization error manifests is highly dependent on the source material and encoder or codec used.

!!! example "Examples of common quantization errors by different encoders"
    === "x264"

        x264 quantization error usually manifests as blocking artifacts
        around high contrast edges,
        or noise in flat areas and around high contrast edges.

        === "Example A"

            ![An example of quantization error artifacts from x264][placeholder-image]

        === "Example B"

            ![An example of quantization error artifacts from x264][placeholder-image]

        === "Example C"

            ![An example of quantization error artifacts from x264][placeholder-image]

    === "x265"

        x265 quantization error usually manifests as ringing artifacts
        around high contrast edges.
        This can be particularly noticeable in darker scenes with any amount of dithering,
        as it will create an ugly "squiggly" pattern.

        === "Example A"

            ![An example of quantization error artifacts from x265][placeholder-image]

        === "Example B"

            ![An example of quantization error artifacts from x265][placeholder-image]

        === "Example C"

            ![An example of quantization error artifacts from x265][placeholder-image]

    === "MPEG2"

        !!! warning "Stub"
            This page is a [stub][wikipedia-stubs].
            You can help by [expanding it][contributing].

            !!! abstract "Extra information"
                There are no encoders in JET who use MPEG2,
                so external contributions are welcome.
                This tab should also get a better title,
                ideally of the most used MPEG2 encoder(s).

        Mpeg2 quantization error usually manifests as huge blocking artifacts,
        particularly on the chroma planes.

        === "Example A"
            ![An example of blocking artifacts from MPEG2][placeholder-image]

        === "Example B"
            ![An example of blocking artifacts from MPEG2][placeholder-image]

        === "Example C"
            ![An example of blocking artifacts from MPEG2][placeholder-image]

    === "AV1"

        !!! warning "Stub"
            This page is a [stub][wikipedia-stubs].
            You can help by [expanding it][contributing].

            !!! abstract "Extra information"
                There are no encoders in JET who use AV1,
                so external contributions are welcome.
                This tab should also get a better title,
                ideally of the most used AV1 encoder(s).

        AV1 quantization error depends on the encoder used.
        The most common form is heavy blurring of flatter areas.

        === "SVT-AV1"
            ![An example of quantization error artifacts from SVT-AV1][placeholder-image]

        === "RAV1E"
            ![An example of quantization error artifacts from RAV1E][placeholder-image]

        === "Some other AV1 encoder"
            ![An example of quantization error artifacts from some other AV1 encoder][placeholder-image]

    === "VP9"

        !!! warning "Stub"
            This page is a [stub][wikipedia-stubs].
            You can help by [expanding it][contributing].

            !!! abstract "Extra information"
                There are no encoders in JET who use VP9,
                so external contributions are welcome.
                This tab should also get a better title,
                ideally of the most used VPx encoder(s).

        VP9 quantization error usually manifests as ringing artifacts
        around high contrast edges.

        === "Example A"
            ![An example of ringing artifacts from VP9][placeholder-image]

        === "Example B"
            ![An example of ringing artifacts from VP9][placeholder-image]

        === "Example C"
            ![An example of ringing artifacts from VP9][placeholder-image]

??? question "Which package contains filters to fix this?"
    The [vs-denoise] package contains filters specifically designed to noise, including many forms of compression noise caused by quantization error.
    </p>
    <p>
    In more extreme cases,
    you may need to use a neural network-based model
    tailored to the specific encoder and compression level used.
    At the time of writing,
    JET does not have a neural network-based package,
    but vs-denoise includes a wrapper for <a href="https://github.com/xinntao/DPIR">DPIR</a>.


### Ringing

### Aliasing


[//]: # (stubs)
[contributing]: https://github.com/Jaded-Encoding-Thaumaturgy/JET-Guide?tab=readme-ov-file#contributing
[wikipedia-stubs]: https://en.wikipedia.org/wiki/Wikipedia:Stubs

[##]: # (placeholder image)
[placeholder-image]: https://archive.org/download/placeholder-image/placeholder-image.jpg

[##]: # (packages)
[vs-deband]: https://github.com/Jaded-Encoding-Thaumaturgy/vs-deband
[vs-denoise]: https://github.com/Jaded-Encoding-Thaumaturgy/vs-denoise

[//]: # (other)
[discord]: https://discord.gg/XTpc6Fa9eB