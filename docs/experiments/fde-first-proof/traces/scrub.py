#!/usr/bin/env python3
"""Alembic-style scrub for the FDE reasoning traces.
Applies Juni's 2026-08-11 redaction standard. Deterministic, auditable, re-runnable.
KEEP: names (Juni, Matilde), human steering + funny moments, tool-call texture, tool problems.
STRIP: ports, device names, internal links/hostnames, private-repo refs, Discord thread/channel
IDs + the Discord link itself, keys/tokens/credential mechanics, user IDs/snowflakes, internal paths.

Deployment-specific names (machine hostnames, the git bot's app name) are not written in this
file. They are read at run time from the environment and from an untracked file beside it:

    SCRUB_HOSTS="build-box,build-box.local" SCRUB_GIT_BOTS="example-git-app" \\
        python3 scrub.py raw.md out.SCRUBBED.md

or copy scrub.local.example.txt to scrub.local.txt (git-ignored) and list them there.
The run stops if no hostname is configured, so a missing list cannot pass unnoticed;
set SCRUB_NO_LOCAL=1 to run with the generic rules only.
"""
import os, re, sys, json
from pathlib import Path

LOCAL_FILE = Path(__file__).with_name('scrub.local.txt')
ENV_VARS = {'host': 'SCRUB_HOSTS', 'git-bot': 'SCRUB_GIT_BOTS'}


def local_terms() -> dict:
    """Names to scrub that must stay out of the repo, longest first per kind."""
    terms = {kind: [] for kind in ENV_VARS}
    for kind, var in ENV_VARS.items():
        terms[kind] += re.split(r'[,\s]+', os.environ.get(var, ''))
    if LOCAL_FILE.exists():
        for n, line in enumerate(LOCAL_FILE.read_text(encoding='utf8').splitlines(), 1):
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            kind, _, name = line.partition(' ')
            if kind not in terms or not name.strip():
                sys.exit(f'{LOCAL_FILE.name}:{n}: expected "host <name>" or "git-bot <name>"')
            terms[kind].append(name.strip())
    return {kind: sorted({n for n in names if n}, key=len, reverse=True)
            for kind, names in terms.items()}


LOCAL = local_terms()

def scrub(text: str) -> str:
    t = text
    # internal filesystem paths -> generic
    t = re.sub(r'/opt/data/[\w./-]*', '<repo>', t)
    t = re.sub(r'/tmp/[\w./-]*', '<tmp>', t)
    t = re.sub(r'/opt/hermes/[\w./-]*', '<hermes>', t)
    t = re.sub(r'\$HOME/[\w./-]*', '<home>', t)
    t = re.sub(r'~/[\w./-]*', '<home>', t)
    # discord thread/channel/user snowflakes (18-19 digit IDs)
    t = re.sub(r'\b1[0-9]{17,18}\b', '<id>', t)
    # discord invite / cdn links
    t = re.sub(r'https://cdn\.discordapp\.com/\S+', '<discord-attachment>', t)
    # bsky post AT URIs and post rkeys -> generic handle ref (keep the handle, drop the rkey)
    t = re.sub(r'at://([\w.-]+)/app\.bsky\.feed\.post/\w+', r'at://\1/...', t)
    t = re.sub(r'https://bsky\.app/profile/([\w.-]+)/post/\w+', r'https://bsky.app/profile/\1/...', t)
    # credential/auth mechanics
    t = re.sub(r'GH_TOKEN', '<token>', t)
    t = re.sub(r'oauth_token', '<token>', t)
    t = re.sub(r'git credential fill', 'git credential <helper>', t)
    t = re.sub(r'credential.helper', 'credential <helper>', t)
    for bot in LOCAL['git-bot']:
        t = re.sub(re.escape(bot) + r'\[bot\]', '<git-bot>', t)
    t = re.sub(r'hermes_cli\.github_app_token', '<github-app-token-helper>', t)
    # ports / hosts / devices
    for host in LOCAL['host']:
        t = re.sub(re.escape(host) + r'(?::\d+)?', '<host>', t)
    t = re.sub(r'localhost:\d+|127\.0\.0\.1:\d+', '<host:port>', t)
    t = re.sub(r':(\d{4,5})/keys', ':<port>/keys', t)
    return t

def main():
    if not LOCAL['host'] and os.environ.get('SCRUB_NO_LOCAL') != '1':
        sys.exit('scrub.py: no hostnames to scrub. Set SCRUB_HOSTS or create scrub.local.txt '
                 '(see scrub.local.example.txt), or set SCRUB_NO_LOCAL=1 for generic rules only.')
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(src, encoding='utf8') as f:
        body = f.read()
    with open(dst, 'w', encoding='utf8') as f:
        f.write(scrub(body))
    # report what got scrubbed
    counts = {
        'paths': len(re.findall(r'<repo>|<tmp>|<hermes>|<home>', scrub(body))),
        'ids': len(re.findall(r'<id>', scrub(body))),
        'tokens': len(re.findall(r'<token>', scrub(body))),
        'links': len(re.findall(r'<discord-attachment>', scrub(body))),
    }
    print(json.dumps({'dst': dst, 'scrubbed': counts}, indent=2))

if __name__ == '__main__':
    main()
