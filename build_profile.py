"""Build README.md from profile_template.md, filling in live activity sections.

Sections are delimited by HTML comment markers:
    <!-- START:KEY -->
    ...generated content...
    <!-- END:KEY -->

The script never touches anything outside those markers, so the static prose in
profile_template.md is authoritative and only the dynamic blocks regenerate.

Uses GITHUB_TOKEN from the workflow env if available. Without it, falls back to
the unauthenticated public API (lower rate limits, no private repos).
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

USER = 'Gluthoric'
ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / 'profile_template.md'
OUTPUT = ROOT / 'README.md'

PROFILE_TOKEN = os.environ.get('PROFILE_TOKEN', '')
FALLBACK_TOKEN = os.environ.get('GITHUB_TOKEN', '')
TOKEN = PROFILE_TOKEN or FALLBACK_TOKEN
HEADERS = {'Accept': 'application/vnd.github+json'}
if TOKEN:
    HEADERS['Authorization'] = f'Bearer {TOKEN}'


def fetch_all_repos() -> list[dict]:
    """Return every repo the token can see.

    /user/repos lists private repos but requires a user-scoped token (a PAT or
    GitHub App user token). The default GITHUB_TOKEN inside Actions is repo-
    scoped and will 403 on /user/repos, so we only hit that endpoint when a
    dedicated PROFILE_TOKEN is provided.
    """
    repos: list[dict] = []
    if PROFILE_TOKEN:
        url = 'https://api.github.com/user/repos?per_page=100&affiliation=owner&sort=pushed'
    else:
        url = f'https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed'
    while url:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not isinstance(batch, list):
            print(f'unexpected payload: {batch}', file=sys.stderr)
            break
        repos.extend(batch)
        link = r.headers.get('Link', '')
        next_url = None
        for part in link.split(','):
            if 'rel="next"' in part:
                next_url = part[part.find('<') + 1:part.find('>')]
                break
        url = next_url
    return repos


def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    return (datetime.now(timezone.utc) - dt).days


def render_activity(repos: list[dict]) -> str:
    public = [r for r in repos if not r['private']]
    private = [r for r in repos if r['private']]

    def active(repos: list[dict], days: int) -> list[dict]:
        return [r for r in repos if (days_since(r.get('pushed_at')) or 9999) <= days]

    pub_7, prv_7 = active(public, 7), active(private, 7)
    pub_30, prv_30 = active(public, 30), active(private, 30)
    pub_90, prv_90 = active(public, 90), active(private, 90)

    table = [
        '| Window | Active repos | Public | Private |',
        '|--------|-------------:|-------:|--------:|',
        f'| Last 7 days  | {len(pub_7) + len(prv_7)} | {len(pub_7)} | {len(prv_7)} |',
        f'| Last 30 days | {len(pub_30) + len(prv_30)} | {len(pub_30)} | {len(prv_30)} |',
        f'| Last 90 days | {len(pub_90) + len(prv_90)} | {len(pub_90)} | {len(prv_90)} |',
    ]

    totals = f'\n**Total repos visible to this profile build:** {len(public)} public, {len(private)} private.'

    if not PROFILE_TOKEN:
        totals += '\n\n_Private counts above are zero because this build does not have a `PROFILE_TOKEN` secret with private-repo read scope. Add one to surface real private activity counts._'

    return '\n'.join(table) + '\n' + totals


def render_languages(repos: list[dict]) -> str:
    counts: Counter[str] = Counter()
    for r in repos:
        lang = r.get('language')
        if lang:
            counts[lang] += 1
    if not counts:
        return '_No language data._'
    top = counts.most_common(8)
    total = sum(c for _, c in top)
    lines = []
    for name, count in top:
        bar_width = round(20 * count / max(1, total))
        bar = '█' * bar_width + '░' * (20 - bar_width)
        lines.append(f'`{bar}` **{name}** — {count} repos')
    return '\n\n'.join(lines)


def render_recent_public(repos: list[dict], limit: int = 6) -> str:
    public = [r for r in repos if not r['private'] and not r.get('fork')]
    public.sort(key=lambda r: r.get('pushed_at') or '', reverse=True)
    if not public:
        return '_No public repos found._'
    lines = []
    for r in public[:limit]:
        name = r['name']
        url = r['html_url']
        desc = (r.get('description') or '').strip() or '_no description_'
        when = (r.get('pushed_at') or '')[:10]
        lang = r.get('language') or '—'
        lines.append(f'- [`{name}`]({url}) — {desc} _(last push {when}, {lang})_')
    return '\n'.join(lines)


def replace_section(template: str, key: str, content: str) -> str:
    pattern = re.compile(
        rf'(<!-- START:{re.escape(key)} -->).*?(<!-- END:{re.escape(key)} -->)',
        re.DOTALL,
    )
    return pattern.sub(rf'\1\n{content}\n\2', template)


def main() -> int:
    if not TEMPLATE.exists():
        print(f'template missing at {TEMPLATE}', file=sys.stderr)
        return 1

    repos = fetch_all_repos()
    print(f'fetched {len(repos)} repos (token={"yes" if TOKEN else "no"})', file=sys.stderr)

    template = TEMPLATE.read_text(encoding='utf-8')
    template = replace_section(template, 'ACTIVITY', render_activity(repos))
    template = replace_section(template, 'LANGUAGES', render_languages(repos))
    template = replace_section(template, 'RECENT_PUBLIC', render_recent_public(repos))
    template = replace_section(
        template,
        'UPDATED',
        f'Last rebuilt {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} via a GitHub Action that runs every hour.',
    )

    OUTPUT.write_text(template, encoding='utf-8')
    print(f'wrote {OUTPUT}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
