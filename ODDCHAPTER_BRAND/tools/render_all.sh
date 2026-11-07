#!/usr/bin/env bash
# Renders every SVG asset to the PNG size its platform requires, then reports QC.
set -euo pipefail
cd "$(dirname "$0")/.."
R() { node tools/render.mjs "$1" "$2" "$3" none; }

# --- logo masters
R 01_LOGO/master/LOGO_MASTER.svg            01_LOGO/master/LOGO_MASTER_4000.png 4000
R 01_LOGO/master/LOGO_MASTER_TAGLINE.svg    01_LOGO/master/LOGO_MASTER_TAGLINE_4000.png 4000
R 01_LOGO/master/MONOGRAM_MASTER.svg        01_LOGO/master/MONOGRAM_MASTER_2048.png 2048
R 01_LOGO/master/AVATAR_COMPACT.svg         01_LOGO/master/AVATAR_COMPACT_1024.png 1024
R 01_LOGO/dark/LOGO_DARK.svg                01_LOGO/dark/LOGO_DARK_2400.png 2400
R 01_LOGO/dark/LOGO_DARK_TAGLINE.svg        01_LOGO/dark/LOGO_DARK_TAGLINE_2400.png 2400
R 01_LOGO/dark/MONOGRAM_DARK.svg            01_LOGO/dark/MONOGRAM_DARK_1200.png 1200
R 01_LOGO/light/LOGO_LIGHT.svg              01_LOGO/light/LOGO_LIGHT_2400.png 2400
R 01_LOGO/light/LOGO_LIGHT_TAGLINE.svg      01_LOGO/light/LOGO_LIGHT_TAGLINE_2400.png 2400
R 01_LOGO/light/MONOGRAM_LIGHT.svg          01_LOGO/light/MONOGRAM_LIGHT_1200.png 1200
R 01_LOGO/monochrome/LOGO_MONO.svg          01_LOGO/monochrome/LOGO_MONO_2400.png 2400
R 01_LOGO/monochrome/MONOGRAM_MONO.svg      01_LOGO/monochrome/MONOGRAM_MONO_1200.png 1200

# --- youtube
R 02_YOUTUBE/avatar/YOUTUBE_AVATAR_800.svg           02_YOUTUBE/avatar/YOUTUBE_AVATAR_800.png 800
R 02_YOUTUBE/banner/YOUTUBE_BANNER_2560x1440.svg     02_YOUTUBE/banner/YOUTUBE_BANNER_2560x1440.png 2560
R 02_YOUTUBE/banner/BANNER_CROP_CHECK.svg            02_YOUTUBE/banner/BANNER_CROP_CHECK.png 2400
R 02_YOUTUBE/watermark/WATERMARK_LIGHT_150.svg       02_YOUTUBE/watermark/WATERMARK_LIGHT_150.png 150
R 02_YOUTUBE/watermark/WATERMARK_DARK_150.svg        02_YOUTUBE/watermark/WATERMARK_DARK_150.png 150
R 02_YOUTUBE/watermark/WATERMARK_LIGHT_150.svg       02_YOUTUBE/watermark/WATERMARK_LIGHT_800.png 800
R 02_YOUTUBE/thumbnails/TEMPLATE_01_PERISTIWA.svg    02_YOUTUBE/thumbnails/TEMPLATE_01_PERISTIWA.png 1280
R 02_YOUTUBE/thumbnails/TEMPLATE_02_BERTAHAN_HIDUP.svg 02_YOUTUBE/thumbnails/TEMPLATE_02_BERTAHAN_HIDUP.png 1280
R 02_YOUTUBE/thumbnails/TEMPLATE_03_SAINS_ANEH.svg   02_YOUTUBE/thumbnails/TEMPLATE_03_SAINS_ANEH.png 1280
R 02_YOUTUBE/end_card/YOUTUBE_END_CARD_1920x1080.svg 02_YOUTUBE/end_card/YOUTUBE_END_CARD_1920x1080.png 1920

# --- social (stories + OG card come from build_extra)
python3 tools/build_extra.py
R 03_SOCIAL/profile/SOCIAL_PROFILE_1024.svg   03_SOCIAL/profile/SOCIAL_PROFILE_1024.png 1024
R 03_SOCIAL/profile/SOCIAL_HEADER_DARK.svg    03_SOCIAL/profile/SOCIAL_HEADER_DARK.png 1500
R 03_SOCIAL/profile/SOCIAL_HEADER_LIGHT.svg   03_SOCIAL/profile/SOCIAL_HEADER_LIGHT.png 1500
R 03_SOCIAL/post_templates/SOCIAL_POST_1080.svg 03_SOCIAL/post_templates/SOCIAL_POST_1080.png 1080
R 03_SOCIAL/stories/SOCIAL_STORY_1080x1920.svg       03_SOCIAL/stories/SOCIAL_STORY_1080x1920.png 1080
R 03_SOCIAL/stories/SOCIAL_STORY_COVER_1080x1920.svg 03_SOCIAL/stories/SOCIAL_STORY_COVER_1080x1920.png 1080
R 03_SOCIAL/link_preview/OPEN_GRAPH_1200x630.svg      03_SOCIAL/link_preview/OPEN_GRAPH_1200x630.png 1200

# --- print artwork
python3 tools/build_print.py

# --- documentation sheets
python3 tools/build_sheets.py
R 05_PREVIEWS/USAGE_DO_DONT.svg   05_PREVIEWS/USAGE_DO_DONT.png 2400
R 05_PREVIEWS/CONTACT_SHEET.svg   05_PREVIEWS/CONTACT_SHEET.png 2000
R 04_MOTION/animation_reference/ANIMATION_STORYBOARD.svg 04_MOTION/animation_reference/ANIMATION_STORYBOARD.png 2400

# --- motion (frames + gif + poster + smil)
python3 tools/build_motion.py

# --- print previews (SVG is the master; these are for review on screen)
R 07_PRINT/stationery/BUSINESS_CARD_FRONT_91x61.svg 07_PRINT/previews/BUSINESS_CARD_FRONT_PREVIEW.png 1075
R 07_PRINT/stationery/BUSINESS_CARD_BACK_91x61.svg  07_PRINT/previews/BUSINESS_CARD_BACK_PREVIEW.png 1075
R 07_PRINT/stationery/LETTERHEAD_A4_210x297.svg     07_PRINT/previews/LETTERHEAD_PREVIEW.png 1240
R 07_PRINT/poster/POSTER_A2_420x594.svg             07_PRINT/previews/POSTER_A2_PREVIEW.png 1500
R 07_PRINT/merch/STICKER_DIECUT_75mm.svg            07_PRINT/previews/STICKER_PREVIEW.png 956
R 07_PRINT/merch/TEE_ART_A3_297x420.svg             07_PRINT/previews/TEE_ART_PREVIEW.png 1000
R 07_PRINT/PRINT_SCALE_TEST.svg                     07_PRINT/PRINT_SCALE_TEST.png 1800

# --- favicons / delivery
R 01_LOGO/dark/ICON_SQUARE_DARK.svg  06_EXPORTS/FAVICON_512.png 512
R 01_LOGO/dark/ICON_SQUARE_DARK.svg  06_EXPORTS/FAVICON_192.png 192
R 01_LOGO/dark/ICON_SQUARE_DARK.svg  06_EXPORTS/FAVICON_32.png 32
R 01_LOGO/master/ICON_SQUARE.svg     06_EXPORTS/ICON_TRANSPARENT_512.png 512
R 01_LOGO/master/LOGO_MASTER.svg     06_EXPORTS/LOGO_PRIMARY_2000.png 2000
