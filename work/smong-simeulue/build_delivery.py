#!/usr/bin/env python3
"""Create the channel delivery thumbnail and poster for AK-EP11."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CASE=Path(__file__).resolve().parent
OUT=CASE/'delivery'
OUT.mkdir(exist_ok=True)
FONT_A=CASE/'fonts'/'Anton-Regular.ttf'
FONT_B=CASE/'fonts'/'BarlowCondensed-ExtraBold.ttf'
IVORY=(239,238,230); RED=(216,42,42); NAVY=(5,22,34)

def ft(p,s): return ImageFont.truetype(str(p),s)

def thumb():
 w,h=1280,720
 im=Image.new('RGB',(w,h),NAVY); d=ImageDraw.Draw(im,'RGBA')
 d.ellipse((680,-240,1450,820),fill=(5,59,70,220)); d.ellipse((-220,490,700,1050),fill=(4,49,64,210))
 for i in range(12): d.arc((-140,360+i*33,1430,1060+i*33),190,348,fill=(69,137,149,45),width=3)
 raw=Image.open(CASE/'img'/'simeulue_topography_cc-by-sa-3.png').convert('RGB')
 card=Image.new('RGB',(510,452),IVORY); card.paste(raw.resize((458,407),Image.Resampling.LANCZOS),(26,22)); im.paste(card,(725,130))
 d.rounded_rectangle((56,55,370,102),radius=10,fill=RED); d.text((76,63),'SIMEULUE · 2004',font=ft(FONT_B,29),fill=IVORY)
 d.multiline_text((56,125),'LAUT\nSURUT',font=ft(FONT_A,105),fill=IVORY,spacing=-10)
 d.text((62,370),'MEREKA LANGSUNG',font=ft(FONT_B,48),fill=IVORY)
 d.text((62,417),'LARI KE BUKIT',font=ft(FONT_A,65),fill=RED)
 d.text((62,585),'SMONG · KISAH NYATA INDONESIA',font=ft(FONT_B,27),fill=(185,203,205))
 d.text((60,638),'PETA: SADALMELIK · CC BY-SA 3.0',font=ft(FONT_B,20),fill=(141,167,172))
 im.save(OUT/'AK-EP11_thumbnail_16x9.jpg',quality=93,optimize=True)

def poster():
 im=Image.open(CASE/'img'/'01_laut_surut.png').convert('RGB')
 im.save(OUT/'AK-EP11_poster_9x16.jpg',quality=93,optimize=True)

if __name__=='__main__': thumb(); poster()
