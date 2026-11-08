# Publishing: approval → YouTube / Facebook Reel / TikTok

Two things are true about this pipeline and both matter:

1. **It cannot post on its own.** The workflow only runs when a person starts it,
   and the publishing job sits behind the `production` environment, which you
   configure with *required reviewers*. An approval click is the gate.
2. **Your Buffer key never touches the repo, the chat, or a log.** It lives in
   GitHub Secrets and is read as `BUFFER_API_KEY` at run time.

---

## 1. One-time setup (about 10 minutes, all in GitHub/Buffer UI)

### 1.1 Create the approval environment

`Settings → Environments → New environment → production`

- **Required reviewers:** add yourself. (This is the approval gate.)
- Optional: restrict deployment branches to `main`.

Without this step the workflow still runs — but with no reviewer, nothing stops it.
Set it up before the first real publish.

### 1.2 Get the Buffer credentials

1. Buffer → `publish.buffer.com/settings/api` → create an API key.
2. Connect the three channels (YouTube, Facebook Page, TikTok) in Buffer.
3. Copy the **channel id** for each — they are per-network, not per-account.

### 1.3 Add repository secrets

`Settings → Secrets and variables → Actions → New repository secret`

| secret | what it is |
|---|---|
| `BUFFER_API_KEY` | the key from 1.2 |
| `BUFFER_CHANNEL_YOUTUBE` | channel id of the YouTube channel |
| `BUFFER_CHANNEL_FACEBOOK` | channel id of the Facebook Page |
| `BUFFER_CHANNEL_TIKTOK` | channel id of the TikTok account |
| `BUFFER_ORGANIZATION_ID` | only needed to list channels from CI |

`GITHUB_TOKEN` is provided by Actions; no setup.

### 1.4 Find the channel ids without leaving CI

```
Actions → Publish pilot → Run workflow
  targets: youtube        (any value)
  dry_run: true
```
The step still needs channel ids to run, so the practical order is: get the ids
from Buffer's own UI (each channel's settings page shows its id), then dry-run.

---

## 2. Publishing a film

```
Actions → "Publish pilot to YouTube / Facebook Reel / TikTok" → Run workflow
```

| input | default | notes |
|---|---|---|
| `video_path` | `10_FILM/final/ODDCHAPTER_PILOT_001_CAPTIONS_1080x1920_29s.mp4` | must be in the repo |
| `release_tag` | `pilot-001` | also the public host path |
| `title` | ODDCHAPTER — Kisah nyata… | YouTube title, ≤ 100 chars |
| `caption` | Setiap minggu, satu kisah nyata… | post text for all three |
| `targets` | `youtube,facebook,tiktok` | any subset |
| `thumbnail_offset_ms` | `2000` | frame used as the video thumbnail |
| `dry_run` | **`true`** | prints the exact JSON payloads, sends nothing |

Sequence:

1. `verify` — file exists, under the 100 MB release-asset limit, sha256 printed.
2. **approval** — the `production` environment waits for a reviewer.
3. host — creates/updates the GitHub Release `pilot-001` and uploads the MP4.
4. url check — `curl -L` must return `200` and a video content type.
5. publish — `node .github/scripts/buffer-publish.mjs` calls Buffer once per network.
6. summary — tag, targets, dry-run flag, approver, final URL in the run summary.

Run it once with `dry_run: true` and read the printed payloads before the first
real publish.

---

## 3. Why a GitHub Release, not the Drive link

Buffer has **no upload endpoint**. It fetches media itself, so an asset must be
**public, direct, HTTPS and stable** — Google Drive share links are explicitly
rejected by Buffer (they render a preview page, not the file).

A GitHub Release asset is the cheapest stable host that travels with this repo
(~1.2 MB, public download URL, never expires). `dry_run` output shows the URL it
will use.

If the URL check ever fails, or Buffer reports it cannot fetch the media, point
`--video-url` at any of these instead (Buffer's own documented options):

- Cloudinary delivery URL (`https://res.cloudinary.com/...`) — free tier
- Cloudflare R2 public bucket URL — free tier

Both are drop-in: `node .github/scripts/buffer-publish.mjs --video-url <url> …`.

---

## 4. What is verified and what is not

| claim | status |
|---|---|
| Buffer accepts a video via `assets:[{video:{url}}]` | **VERIFIED** — Buffer API docs, `Create Video Post` |
| YouTube needs `metadata.youtube.title` + `categoryId` | **VERIFIED** — `YoutubePostMetadataInput` |
| Facebook Reel = `metadata.facebook.type: "reel"` | **VERIFIED** — `FacebookPostMetadataInput` |
| Endpoint is GraphQL `POST https://api.buffer.com`, `Authorization: Bearer` | **VERIFIED** — docs |
| A GitHub Release asset URL satisfies Buffer's fetch | **LIKELY, untested** — it is a 302 to a CDN file; the workflow's `curl -L` proves reachability, but only a real publish proves Buffer's fetch |
| Your channels accept vertical 1080×1920 MP4, 29.2 s | **LIKELY** — within YouTube Shorts / Reels / TikTok limits |
| TikTok posts land without a manual "publish" tap | **UNKNOWN** — depends on your TikTok account type and Buffer's connection permissions |
| Each network's first post succeeds end-to-end | **UNKNOWN until the first approved run** |

If a network fails, the script prints Buffer's own `MutationError` message per
target and exits non-zero, so a partial publish is visible rather than silent.

---

## 5. Rollback

- Buffer dashboard → delete the post before it publishes (posts created with
  `mode: shareNow` go out immediately, so check the run summary).
- Repo side: `gh release delete pilot-001` removes the public asset; nothing else
  is mutated by the workflow.
