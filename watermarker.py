import argparse

from watermarker.file_ops import get_files
from watermarker.image_ops import add_watermark

parser = argparse.ArgumentParser(description='Overlay an image with a watermark')

file_group = parser.add_mutually_exclusive_group(required=True)
file_group.add_argument("-f", "--file", help='The file to overlay the watermark on')
file_group.add_argument("-d", "--directory", help='Directory of files to overlay the watermark on')

parser.add_argument("-w", "--watermark", help='The watermark to overlay on the file', required=True)
parser.add_argument("-c", "--corner", help='Corner to place the watermark', default='bottom-left')
args = parser.parse_args()


if __name__ == '__main__':
    if args.file:
        add_watermark(args.file, args.watermark, args.corner)
    elif args.directory:
        for file in get_files(args.directory):
            add_watermark(file, args.watermark, args.corner)
