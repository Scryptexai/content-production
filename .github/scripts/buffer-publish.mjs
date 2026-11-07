/**
 * buffer-publish.mjs — post one vertical video to YouTube, a Facebook Reel and
 * TikTok through Buffer's GraphQL API.
 *
 * Nothing here holds a credential: the API key and channel ids arrive as
 * environment variables from GitHub Secrets.
 *
 *   node .github/scripts/buffer-publish.mjs --list-channels
 *   node .github/scripts/buffer-publish.mjs --video-url https://… --targets youtube,facebook,tiktok
 *   ... add --dry-run to print the payloads and send nothing.
 *
 * API reference: https://developers.buffer.com (GraphQL, POST https://api.buffer.com)
 */
import process from "node:process";

const API = "https://api.buffer.com";

const argv = process.argv.slice(2);
const arg = (name, fallback = undefined) => {
  const i = argv.indexOf(`--${name}`);
  return i === -1 ? fallback : argv[i + 1] ?? true;
};
const flag = (name) => argv.includes(`--${name}`);

const KEY = process.env.BUFFER_API_KEY;
const DRY = flag("dry-run");

const CHANNELS = {
  youtube: process.env.BUFFER_CHANNEL_YOUTUBE,
  facebook: process.env.BUFFER_CHANNEL_FACEBOOK,
  tiktok: process.env.BUFFER_CHANNEL_TIKTOK,
};

const videoUrl = arg("video-url");
const caption = arg("caption", "");
const title = arg("title", "ODDCHAPTER");
const thumbnailOffset = Number(arg("thumbnail-offset", 2000));
const targets = String(arg("targets", "youtube,facebook,tiktok"))
  .split(",")
  .map((s) => s.trim().toLowerCase())
  .filter(Boolean);

async function gql(query, variables) {
  const res = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${KEY}`,
    },
    body: JSON.stringify({ query, variables }),
  });
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`Buffer returned non-JSON (${res.status}): ${text.slice(0, 400)}`);
  }
  if (!res.ok || json.errors) {
    throw new Error(`Buffer rejected the request (${res.status}): ${JSON.stringify(json.errors ?? json).slice(0, 800)}`);
  }
  return json.data;
}

/** Each network needs its own metadata block; the asset is the same video URL. */
function buildInput(target, channelId) {
  const base = {
    channelId,
    text: caption,
    // "automatic" lets Buffer publish; "shareNow" posts immediately instead of queueing.
    schedulingType: "automatic",
    mode: "shareNow",
    assets: [{ video: { url: videoUrl, metadata: { thumbnailOffset } } }],
  };

  if (target === "youtube") {
    return {
      ...base,
      metadata: {
        youtube: {
          title: title.slice(0, 100), // YouTube hard limit
          categoryId: "24", // Entertainment
          privacy: "public",
          madeForKids: false,
          notifySubscribers: true,
        },
      },
    };
  }
  if (target === "facebook") {
    return { ...base, metadata: { facebook: { type: "reel" } } };
  }
  if (target === "tiktok") {
    return { ...base, metadata: { tiktok: { isAiGenerated: false } } };
  }
  throw new Error(`unknown target: ${target}`);
}

const CREATE = `
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}`;

const LIST_CHANNELS = `
query GetChannels($organizationId: ID!) {
  channels(input: { organizationId: $organizationId }) {
    id
    name
    displayName
    service
  }
}`;

async function main() {
  if (!KEY) throw new Error("BUFFER_API_KEY is not set (add it as a GitHub Secret)");

  if (flag("list-channels")) {
    const org = process.env.BUFFER_ORGANIZATION_ID;
    if (!org) throw new Error("BUFFER_ORGANIZATION_ID is not set");
    const data = await gql(LIST_CHANNELS, { organizationId: org });
    for (const c of data.channels) {
      console.log(`${String(c.service).padEnd(12)} ${c.id}  ${c.displayName ?? c.name}`);
    }
    return;
  }

  if (!videoUrl) throw new Error("--video-url is required (public, direct, https, stable)");
  const missing = targets.filter((t) => !CHANNELS[t]);
  if (missing.length) {
    throw new Error(
      `no channel id for: ${missing.join(", ")} — set ${missing
        .map((t) => `BUFFER_CHANNEL_${t.toUpperCase()}`)
        .join(", ")}`,
    );
  }

  const results = [];
  for (const target of targets) {
    const input = buildInput(target, CHANNELS[target]);
    if (DRY) {
      console.log(`\n[dry-run] ${target}\n${JSON.stringify(input, null, 2)}`);
      results.push({ target, ok: true, dryRun: true });
      continue;
    }
    try {
      const data = await gql(CREATE, { input });
      const payload = data.createPost;
      if (payload.message) {
        results.push({ target, ok: false, message: payload.message });
        console.error(`FAIL ${target}: ${payload.message}`);
      } else {
        results.push({ target, ok: true, postId: payload.post?.id });
        console.log(`OK   ${target}: post ${payload.post?.id}`);
      }
    } catch (err) {
      results.push({ target, ok: false, message: String(err.message ?? err) });
      console.error(`FAIL ${target}: ${err.message ?? err}`);
    }
  }

  console.log(`\n${JSON.stringify({ videoUrl, results }, null, 2)}`);
  if (results.some((r) => !r.ok)) process.exit(1);
}

main().catch((err) => {
  console.error("publish failed:", err.message ?? err);
  process.exit(1);
});
