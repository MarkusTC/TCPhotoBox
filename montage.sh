#!/bin/bash
mogrify -resize 968x648 *.jpg
montage tmp/*.jpg -geometry 968x648 +10+10 -tile 2x2 +polaroid -bordercolor Lavender -background SkyBlue /tmp/polaroid_overlap2.jpg
montage tmp/polaroid_overlap2.jpg /label.jpg -tile 2x1 /tmp/polaroid_overlap2.jpg