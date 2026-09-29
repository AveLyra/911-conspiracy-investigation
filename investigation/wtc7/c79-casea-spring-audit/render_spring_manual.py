"""Render admitted manual pages locally; no source mutation or network use."""
import hashlib
import pathlib
import subprocess
import sys

SOURCE = pathlib.Path('/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf')
PIN = 'f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d'
POPPLER = '/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'

def main():
    assert hashlib.file_digest(SOURCE.open('rb'), 'sha256').hexdigest() == PIN
    pages = [int(p) for p in sys.argv[1:]]
    assert pages and all(1 <= p <= 2206 for p in pages)
    out = pathlib.Path(__file__).parent / 'manual-renders'
    out.mkdir(exist_ok=True)
    for page in pages:
        prefix = out / ('p' + str(page))
        assert not prefix.with_suffix('.png').exists(), 'create-only render'
        subprocess.run([POPPLER, '-f', str(page), '-l', str(page), '-singlefile', '-scale-to', '1600', '-png', str(SOURCE), str(prefix)], check=True, stdout=subprocess.DEVNULL)
        print(page, prefix.with_suffix('.png'))
    assert hashlib.file_digest(SOURCE.open('rb'), 'sha256').hexdigest() == PIN

if __name__ == '__main__':
    main()
