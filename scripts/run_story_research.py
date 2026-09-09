"""Run bounded, read-only Claude Code research jobs using existing login."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('batch', choices=['clinical', 'commercial', 'growth'])
    args = parser.parse_args()
    out = ROOT / 'research' / 'runs'
    out.mkdir(parents=True, exist_ok=True)
    prompt = (ROOT / 'research' / 'prompts' / f'{args.batch}.md').read_text()
    env = os.environ.copy()
    # Use the existing Claude subscription, never an API-key override.
    for key in ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL']:
        env.pop(key, None)
    command = [
        'claude', '-p', '--model', 'sonnet', '--effort', 'medium',
        '--safe-mode', '--no-session-persistence',
        '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
        '--tools', 'WebSearch,WebFetch',
        '--allowedTools', 'WebSearch,WebFetch',
        '--permission-mode', 'dontAsk', '--output-format', 'json',
    ]
    started = time.time()
    print(f'Starting {args.batch}: Sonnet, public web research only.', flush=True)
    try:
        result = subprocess.run(command, input=prompt, text=True, capture_output=True,
                                cwd=ROOT, env=env, timeout=900)
        (out / f'{args.batch}.stdout.json').write_text(result.stdout)
        (out / f'{args.batch}.stderr.txt').write_text(result.stderr)
        print(json.dumps({'batch': args.batch, 'exit_code': result.returncode,
                          'elapsed_seconds': round(time.time() - started),
                          'output_bytes': len(result.stdout)}), flush=True)
        if result.returncode:
            print(result.stderr[-2000:], flush=True)
            print(result.stdout[-2000:], flush=True)
    except subprocess.TimeoutExpired as exc:
        data = exc.stdout or b''
        if isinstance(data, bytes):
            data = data.decode(errors='replace')
        (out / f'{args.batch}.partial.txt').write_text(data)
        print(f'{args.batch}: stopped at 15-minute research limit.', flush=True)

if __name__ == '__main__':
    main()
