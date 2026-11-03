// usage: node render.js page.html duration out.mp4 [fps] [t1,t2,...  -> stills mode]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [html, durS, out, fpsS, stills] = process.argv.slice(2);
  const fps = parseInt(fpsS || '30'), dur = parseFloat(durS);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => window.READY === true);
  if (stills) {
    for (const s of stills.split(',')) {
      await page.evaluate(t => window.seek(t), parseFloat(s));
      await page.screenshot({ path: `${out}_${s}.jpg`, type: 'jpeg', quality: 90 });
    }
    await browser.close(); return;
  }
  const tmp = out.replace(/\.mp4$/, '.part.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(dur * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.seek(t), i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
  require('fs').renameSync(tmp, out);
  await browser.close();
})();
