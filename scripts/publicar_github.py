#!/usr/bin/env python3
"""Publicar o projeto e suas tarefas. Sem --execute, somente exibir o plano."""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(*args, capture=False):
    return subprocess.run(args,cwd=ROOT,check=True,text=True,capture_output=capture).stdout

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true',help='Criar e enviar repositório privado e issues')
    args=p.parse_args()
    config=json.loads((ROOT/'projeto.json').read_text())
    repo=config['github_repository']
    if not re.fullmatch(r'[A-Za-z0-9-]+/[A-Za-z0-9_.-]+',repo):
        raise SystemExit('Nome de repositório inválido.')
    tasks=json.loads((ROOT/'tarefas/backlog.json').read_text())
    print(f'Plano: repositório PRIVADO {repo}; enviar commit atual; criar {len(tasks)} issues sem atribuição automática.')
    if not args.execute:
        for task in tasks: print(task['title'])
        print('Simulação concluída; nenhuma alteração remota.');return
    if not shutil.which('gh'): raise SystemExit('Instalar GitHub CLI (gh) e autenticar antes de executar.')
    login=run('gh','api','user','--jq','.login',capture=True).strip()
    if login!=repo.split('/')[0]: raise SystemExit(f'Conta autenticada {login} difere do proprietário configurado.')
    run('python3','scripts/verificar.py')
    if run('git','status','--porcelain',capture=True).strip():
        raise SystemExit('Há alterações sem commit. Revisar e criar commit antes de publicar.')
    probe=subprocess.run(['gh','repo','view',repo,'--json','nameWithOwner,isPrivate'],cwd=ROOT,text=True,capture_output=True)
    if probe.returncode:
        # Falhas de acesso não são contornadas: create falha caso o nome já exista.
        run('gh','repo','create',repo,'--private','--description','TCC II — RSL de engenharia de prompt para codificação e implementação','--source',str(ROOT),'--remote','origin','--push')
    else:
        info=json.loads(probe.stdout)
        if info.get('isPrivate') is not True: raise SystemExit('O repositório existente não é privado; interrompido.')
        current=subprocess.run(['git','remote','get-url','origin'],cwd=ROOT,text=True,capture_output=True)
        valid={f'https://github.com/{repo}.git',f'https://github.com/{repo}',f'git@github.com:{repo}.git'}
        if current.returncode:
            # Evitar enviar a um repositório existente que possa pertencer a outro projeto.
            raise SystemExit('Repositório remoto existente e origem local ausente. Conferir o destino antes de vinculá-lo.')
        if current.stdout.strip() not in valid: raise SystemExit('Origem local diferente do destino configurado.')
        run('git','push','-u','origin','main')
    existing=json.loads(run('gh','issue','list','--repo',repo,'--state','all','--limit','1000','--json','title,number,url',capture=True))
    by_title={x['title']:x for x in existing}
    mapping=[]
    for task in tasks:
        if task['title'] in by_title:
            item=by_title[task['title']]
        else:
            body=ROOT/'tarefas'/f'{task["id"]}.md'
            # Arquivos estáveis já versionados preservam as quebras de linha do corpo.
            url=run('gh','issue','create','--repo',repo,'--title',task['title'],'--body-file',str(body),capture=True).strip()
            item={'title':task['title'],'url':url,'number':int(url.rsplit('/',1)[1])}
        mapping.append(dict(id=task['id'],dependencies=task['dependencies'],**item))
        (ROOT/'tarefas/github-issues.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
        print(f'{task["id"]}: {item["url"]}')
    print(f'Publicado: https://github.com/{repo}')

if __name__=='__main__':
    main()
