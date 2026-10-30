import { Config } from '@remotion/cli/config';

// Mesin render di sini 2 core tanpa GPU: satu worker, Chromium bawaan
// @sparticuz (diatur lewat flag CLI), dan CRF rendah karena banyak gradien.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setConcurrency(1);
Config.setChromiumOpenGlRenderer('swangle');
