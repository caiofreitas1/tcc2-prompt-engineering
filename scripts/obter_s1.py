#!/usr/bin/env python3
"""Obter a cópia de S1 usada em T02, sem versionar ou executar o PDF."""
import hashlib
import sys
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / 'fontes/artigos/S1-arxiv-2303.06689v5.pdf'
URL = 'https://arxiv.org/pdf/2303.06689v5'
SHA256 = '75c03e2aaa0f837431890f270a86714ea018041992691d5e25846ef0a8998fd0'
LIMITE_BYTES = 20 * 1024 * 1024


def conferir(conteudo):
    if not conteudo.startswith(b'%PDF-'):
        raise ValueError('a resposta não é um PDF')
    obtido = hashlib.sha256(conteudo).hexdigest()
    if obtido != SHA256:
        raise ValueError(
            f'SHA-256 divergente: {obtido}; esperado {SHA256}. '
            'Preserve a cópia e confira a versão antes de alterar o registro.'
        )


def obter(destino=DESTINO):
    if destino.exists():
        conferir(destino.read_bytes())
        print(f'Fonte já disponível e íntegra: {destino}')
        return
    with urlopen(URL, timeout=60) as resposta:
        conteudo = resposta.read(LIMITE_BYTES + 1)
    if len(conteudo) > LIMITE_BYTES:
        raise ValueError('resposta excede o limite de 20 MiB')
    conferir(conteudo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Não sobrescrever arquivo criado por outro processo durante o download.
    with destino.open('xb') as arquivo:
        arquivo.write(conteudo)
    print(f'Fonte obtida e SHA-256 conferido: {destino}')


if __name__ == '__main__':
    try:
        obter()
    except (OSError, ValueError) as exc:
        print(f'ERRO: {exc}', file=sys.stderr)
        raise SystemExit(1)
