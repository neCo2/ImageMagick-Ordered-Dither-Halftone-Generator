# ImageMagick-Ordered-Dither-Halftone-Generator

This script generates 45° angled Halftone Ordered Dither Threshold Maps of arbitrary size for ImageMagick 7. See the [ImageMagick documentation](https://www.imagemagick.org/Usage/quantize/#diy_dither).

Visualizations of each map are provided in the `svg` directory.

To use the pre-generated maps, copy the contents of `thresholds.xml` into ImageMagick's `thresholds.xml` file, which can be found on windows in your installation directory, and on Linux under `~/.magick/thresholds.xml`. DO NOT OVERWRITE THE CONTENTS OF THE FILE, JUST APPEND THE NEW MAPS.<br>
After saving ImageMagick's `thresholds.xml` file, you can now apply the maps using the specified names (`map="h12x12a"` etc.). For example:

```
magick input.png -colorspace Gray -ordered-dither h12x12a output.png
```

To use the script yourself to generate maps with different sizes than provided, adjust the range on line 118 of the script and run it.