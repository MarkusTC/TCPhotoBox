#xmogrify -resize 968x648 *.jpg
montage tmp/4.jpg tmp/3.jpg tmp/2.jpg tmp/1.jpg  -auto-orient -bordercolor Lavender +polaroid -resize %100 -gravity center -background grey -geometry -10+2 -tile 2x2  polaroid_overlap.jpg
mogrify -resize 1965x1668 polaroid_overlap.jpg
montage -geometry +4+4 polaroid_overlap.jpg label.jpg polaroid_overlap.jpg