# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: veteran MU Online players from Argentina and Latin America who played in
the 2000s (cybercafés, Season 0–6 era) and are coming back. Spanish speakers;
the site speaks Rioplatense Spanish (voseo: "descargá", "entrá", "elegí").
They arrive knowing the game: classes, maps, rates, resets, the WebZen client.
Their job on the site is to decide whether this server is worth installing,
then download the client, create an account and get in.

## Product Purpose

Landing and content site for **OpenMuArg**, a private MU Online server
(Season 6 Episode 3, WebZen client 1.02.00) running on OpenMU. Success is a
returning player going from first visit to logged in-game: download → account →
connect.

## Positioning

Open decision: what OpenMuArg offers that another private server could not
truthfully copy is not defined yet. Current copy leans on "sin ventaja comprada"
(the shop is cosmetic only); treat that as a stated claim in `content/site.yml`,
not a confirmed differentiator.

## Operating Context

- Players read the site on desktop Windows PCs (where the client runs) and on
  phones (from Discord links).
- Community, support and announcements live on Discord.
- Weekly recurring events with countdown; news posts in Markdown.

## Capabilities and Constraints

- Flask + Jinja + Tailwind CSS v4, served by Gunicorn behind Caddy (Docker or
  systemd/serve-local). No JS framework; small vanilla `app/static/js/app.js`.
- v0 has no database: all content lives in `content/` (YAML + Markdown) and is
  edited by the operator without touching code. Templates must keep reading it.
- v1 (planned, `docs/v1-db.md`): OpenMU Postgres for account registration,
  rankings and live server status. The site shows server status only when it is measured live (FEATURE_STATUS); otherwise it shows none.
- Fonts are self-hosted in `app/static/fonts/`; no external CDNs.
- Routes: `/`, `/noticias`, `/noticias/<slug>`, `/descargas`, `/registro`,
  `/faq`, `/reglas`, 404/500.
- Terminology: rates, drop, master level, reset, sub-servidor, Connect Server,
  ServerInfo, launcher.

## Brand Commitments

- Name: **OpenMuArg**.
- Footer disclaimer must stay: not affiliated with Webzen; fan project, non-profit.
- Voice: direct, warm, Rioplatense voseo, no hype or pay-to-win language.

## Evidence on Hand

- Real content: `content/site.yml` (rates, features, steps), `classes.yml`,
  `events.yml`, `downloads.yml`, `faq.yml`, `rules.md`, `news/*.md`.
- Downloads are not published yet (`available: false`, no sha256).
- No real screenshots yet (`app/static/img/gallery/` is empty); gallery shows
  placeholders.
- No player counts, rankings, testimonials or reviews. Do not invent them;
  any illustrative data must be labeled as example.

## Product Principles

1. Get a returning player in-game fast: download and account are never more than one step away. The server's network address is never published (the client ships with ServerInfo configured).
2. Speak to people who already know MU; don't explain the game, show this server.
3. Content stays editable by the operator in `content/`, never hard-coded.
4. Honest by default: no fake population, rankings or claims until v1 provides real data.
