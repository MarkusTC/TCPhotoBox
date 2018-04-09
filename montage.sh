#!/bin/bash
mogrify -resize 968x648 *.jpg
montage /tmp/*.jpg -geometry 968x648 +10+10 -tile 2x2 +polaroid -bordercolor Lavender -background SkyBlue /tmp/polaroid_overlap2.jpg