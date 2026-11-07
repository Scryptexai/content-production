# What the browser can reach — measured, 2026-11-07

Test harness: `10_FILM/remotion/scripts/browser-probe.mjs` and
`browser-capability.mjs`. Nothing below is assumed; each row is an observed result.

| test | result | evidence |
|---|---|---|
| Chromium binary | `@sparticuz/chromium` **153.0.8010.0** runs | `--version`, launched 103 ms |
| renders a real web app | **yes** | Remotion Studio at `127.0.0.1:3333` rendered and screenshotted, 1440×900 and 390×844 — `output/browser-capability/studio_*.png` |
| executes page JS | **yes** | in-page `fetch()` and `document.body.innerText` read back correctly |
| opens remote sites | **no** | `example.com`, `id.wikipedia.org`, `commons.wikimedia.org`, `archive.org`, `images.nasa.gov` → all `net::ERR_CONNECTION_CLOSED` |
| downloads a file over the network | **yes, when the host is reachable** | 90.0 MB tarball from `codeload.github.com` delivered through CDP download behaviour; sha256 identical to the same file fetched with curl |
| the downloaded file is real media | **yes** | two MP4s extracted: `echo-hereweare.mp4` 44.6 s 480×270 h264+aac, `big_buck_bunny.mp4` |
| TLS to allowlisted hosts | needs `--ignore-certificate-errors` | sandbox terminates TLS with its own CA; Chromium returns `ERR_CERT_AUTHORITY_INVALID` otherwise |

## The binding constraint

The browser is not the limit — **the sandbox egress allowlist is**. Reachable hosts:

```
github.com  codeload.github.com  api.github.com
registry.npmjs.org  pypi.org  files.pythonhosted.org
```

Everything else is refused at connect time, from both `curl` and Chromium. So:
no Pexels, no Pixabay, no Wikimedia, no Archive.org, no NASA — nothing can be
downloaded from this session directly.

## What *does* work for sourcing

| channel | status |
|---|---|
| `web_search` / `fetch_page` | **works against the open internet** — used to read Wikimedia Commons category and file pages and to pull licences |
| `image_search` | works, writes real JPEGs into the workspace — but they are search-result thumbnails (Getty, Dreamstime, …), so **reference only, never publishable** |
| `git clone` / `git fetch` | **works at full size** — 90 MB repo cloned; this is the practical footage ingest |
| Google Drive connector | uploads work; reading binary back is possible but only practical for small files |
| GitHub Actions | **not dispatchable from this session** (`403 Resource not accessible by integration`) |

## Consequences

1. Footage has to arrive through git: either committed by a human, or fetched by
   `.github/workflows/footage.yml` on a runner (which *does* have open internet)
   and committed to `footage/inbox` — that workflow needs one manual
   "Run workflow" click, because this session cannot dispatch Actions.
2. Anything generated (SVG, d3, Remotion, `generate_image`) remains the reliable
   path for original visuals.
3. Search results can be **read** and licence-checked here even though the bytes
   cannot be fetched here — so sourcing decisions can still be made in-session.
