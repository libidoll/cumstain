# watermarker
Quick Python program to watermark images and (soon) videos

## Usage

| Parameter | Description | Default |
|-----------| --- | --- |
| -f        | Input file | None |
| -d        | Input directory | None |
| -w        | Watermark file | None |
| -c        | Corner | bottom-left |

Either `-f` or `-d` must be specified. If `-d` is specified, all files in the directory will be watermarked. If `-f` is specified, only that file will be watermarked.  
`-w` must be given as well.

## Examples
Watermark image `image.png` with `watermark.png` in the bottom left corner:  
`python watermarker.py -f image.png -w watermark.png`  
Watermark all images in the directory `images` with `watermark.png` in the top right corner:  
`python watermarker.py -d images/ -w watermark.png -c top-right`  