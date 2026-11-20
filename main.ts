// gta6-meme-x-01 entry (Node 22, standard library only): the entry is the
// X post itself. This repository holds POST.json with the post's address
// ({"url": "https://x.com/<handle>/status/<id>"}) and the meme that was
// posted (meme.png, drawn in code by draw_meme.py: a Vice City sunset with
// make.fun's ghost, the mascot from make.fun's press kit). The house reads
// the post from X; this program only copies POST.json to /output so the
// gate can find it. It runs twice in a sandbox with no network and both
// runs write identical bytes.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const postFile = readFileSync(join(here, 'POST.json'));
writeFileSync(join(outDir, 'POST.json'), postFile);
