# AI Fashion Site

AI-generated fashion photography showcase. Updated every 6 hours automatically.

## GitHub Pages

Site: `https://aydannadya31.github.io/ai-fashion-auto-site/`

## How it works

- Python script generates fashion images via Cloudflare AI API
- GitHub Actions runs every 6 hours to create new content
- Site is deployed to GitHub Pages automatically

## Secrets

Required repository secrets for the workflow:
- `CF_API_TOKEN` — Cloudflare API token
- `CF_ACCOUNT_ID` — Cloudflare account ID
