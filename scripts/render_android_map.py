"""Render the canonical SVG unchanged for the native Android map (requires Inkscape)."""
from pathlib import Path
import hashlib
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'design/svg/mapa_liceo_concepto.svg'
output = ROOT / 'design/android/mapa_liceo_concepto.png'
output.parent.mkdir(parents=True, exist_ok=True)
profile = ROOT / '.local/inkscape-profile'
profile.mkdir(parents=True, exist_ok=True)
env = {**os.environ, 'INKSCAPE_PROFILE_DIR': str(profile)}
subprocess.run(['inkscape', str(source), '--export-type=png', '--export-area-page',
                '--export-width=2760', '--export-filename=' + str(output)], env=env, check=True)
output.with_name('mapa_liceo_concepto.svg.sha256').write_text(hashlib.sha256(source.read_bytes()).hexdigest() + '\n')
print('Mapa Android generado desde el SVG original:', output)
