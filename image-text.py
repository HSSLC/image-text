from PIL import Image, ImageDraw, ImageFont
import sys

if len(sys.argv) < 3:
    print('自動製作多行字幕\n')
    print('使用方式: image-text.py 來源圖位置 來源字幕位置 [輸出檔案名稱]')
    exit()

im = Image.open(sys.argv[1])
with open(sys.argv[2], encoding='utf-8') as textfile:
    text = textfile.read().split('\n')
#font = ImageFont.load_default()
fontsize = int(im.height / 14)
font = ImageFont.truetype('msjhbd.ttc', fontsize)
padding = int(fontsize / 4)
ascent, descent = font.getmetrics()
#(width, baseline), (offset_x, offset_y) = font.font.getsize(text)
w, h = im.size

imagelines = []

for line in text:
    (width, baseline), (offset_x, offset_y) = font.font.getsize(line)
    crop = im.crop((0, h - (ascent + descent) - padding, w, h))
    textwidth = font.getsize(line)[0]
    draw = ImageDraw.Draw(crop)
    draw.text(((w-textwidth)/2, padding/2), line, (255, 0, 0), font=font)
    imagelines.append(crop)

padding_bottom = int(h / 280) if h > 280 else 1

imagelines_height = sum(x.height for x in imagelines[1:]) + (len(imagelines) - 1) * padding_bottom
output = Image.new(im.mode, (w, im.height + imagelines_height))
output.paste(im, (0, 0))
y = h - imagelines[0].height
for imageline in imagelines:
    output.paste(imageline, (0, y))
    y += imageline.height + padding_bottom
output.save(sys.argv[3] if len(sys.argv) > 3 else 'output.jpg', im.format)
