## Dustin King

I'm an IT director by day and a builder the rest of the time. I write code, run a homelab, and ship side projects spanning web apps, AI tooling, infrastructure automation, embedded hardware, and tabletop game tech. Most of my work lives in private repos, but the breadth is real.

### What I build

**AI and agents.** I've shipped a Slack-native agent that helps a marketing team turn quick prompts into publishable LinkedIn posts and on-brand graphics, and a dual-mode RAG chatbot for an arts and crafts business — a public widget for customers and a password-gated internal mode for staff. I write Model Context Protocol servers (the one for Foundry VTT lets language models query and act on a live tabletop game state). I also run a homegrown multi-agent video production pipeline and an M365 admin CLI built for compromised-user triage.

**Tabletop game tech.** I maintain Vitas Nova, a homebrew D&D 5e campaign wiki I publish out of Obsidian through Quartz onto Cloudflare Pages. I run a Foundry VTT server for the campaign and built a session-recording and live-transcription pipeline so we can replay or annotate sessions afterward. There's also a 5e character sheet editor I wrote that produces print-ready PDFs.

**Dev tooling, open-sourced.** I publish small pieces from my daily AI workflow:

- [`claude-statusline`](https://github.com/Gluthoric/claude-statusline) is a compact custom status line for Claude Code.
- [`claude-agents-kit`](https://github.com/Gluthoric/claude-agents-kit) is a set of seven opinionated subagent definitions for code review, debugging, security audits, architecture review, UX review, database analysis, and team orchestration.

**Hardware and systems.** I write ESP32 firmware for things like soil sensors and Wi-Fi scanners, design printable parts in OpenSCAD, and tinker with Hyundai/KIA Gen5W navigation firmware. On the infrastructure side I run a security stack on my home network (Wazuh SIEM, ntopng flow analysis, Pi-hole DNS filtering, UniFi controller) and a Matter-backed Home Assistant deployment for everything that should be talking on the local network.

**Behind all of it,** my Obsidian vault is structured as a shared knowledge base where Claude, Gemini, and Codex each get their own scratchpads, with a memory layer that persists across sessions. That's the workflow that makes the rest of it tractable.

### Homelab

Four bare-metal Ubuntu machines, all meshed over Tailscale:

- a Ryzen 9 9950X / RTX 5090 desktop as the primary workstation;
- a ThinkPad P14s Gen 5 for portable work and game nights;
- a production application server running FastAPI services behind Cloudflare tunnels, backed by Postgres 17 and a local Ollama instance for offline inference;
- a home services box running Pi-hole, UniFi, ntopng, Wazuh, Home Assistant, and a Matter server.

systemd-native, no Docker unless there's a real reason to use it.

### Stack I reach for

Python 3.13, FastAPI, React 19, Postgres 17, Slack Bolt, the Anthropic and OpenAI APIs. Bare-metal Ubuntu on systemd. Tailscale for everything that needs to talk across hosts. Bitwarden Secrets Manager instead of `.env` files in repos. Obsidian for cross-machine notes and AI scratchpads.

### GitHub activity

![Stats](https://github-readme-stats.vercel.app/api?username=Gluthoric&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&hide_title=true)

Most of my work happens in private repos. The contribution graph at the top of this profile reflects that activity when "Include private contributions on my profile" is enabled in GitHub profile settings.

### Reach me

Open to talking about the work. The fastest path is via the projects above or a GitHub issue on one of the open-source repos.
