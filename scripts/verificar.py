#!/usr/bin/env python3
"""Verificar integridade estrutural; a sustentação semântica exige leitura das fontes."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {
    'estudos': ['id','titulo','identificador','versao','ano','origem','corpus','metadados_conferidos','fonte_primaria','acesso_aberto'],
    'buscas': ['id','data','base','consulta','campos_filtros','total_exportado','arquivo_exportacao','executor'],
    'triagem': ['estudo_id','fase','decisao','criterio','motivo','responsavel','natureza','prompt_versao','data'],
    'afirmacoes': ['id','texto','extracao_ids','bibkey','destino','status','revisor','data_revisao'],
    'qualidade': ['estudo_id','criterio','julgamento','localizador','justificativa','avaliador','natureza','data'],
    'fluxos': ['etapa','contagem','denominador','regra','origem','data'],
    'registros': ['id','busca_id','titulo','ano','doi','arxiv','estudo_id'],
    'resumos': ['estudo_id','registro_id','fonte','resumo'],
    'versoes_abertas': ['estudo_id','url','tipo','versao','origem','data'],
    'deduplicacao': ['chave','registros','decisao','evidencia','fonte','responsavel','natureza','data'],
    'correcoes_registros': ['registro_id','campo','valor_capturado','valor_corrigido','evidencia','fonte','responsavel','natureza','data'],
}
# Códigos da seção 3 do protocolo v2.
CRITERIA={f'I{n}' for n in range(1,7)}|{f'X{n}' for n in range(1,8)}
QUALITY={'objetivo','procedimento','comparador','metricas','ameacas','reprodutibilidade','contaminacao'}
UNAVAILABLE = {'','nao_conferido','nao_informado','nao_aplicavel','fonte_indisponivel'}
EXTRACTION_FIELDS = {'id','estudo_id','tarefa','tecnica','modelo','benchmark','metrica','unidade','comparador','resultado','localizador','fonte','status','revisao_humana'}
# Contrato 2: citação literal conferível e campos da QP2.
EXTRACTION_FIELDS_V2 = {'citacoes','texto_fonte','riscos','mitigacoes','prompt_versao'}

def normalized(text):
    # Ignora hífens e quebras de linha: a extração de texto do PDF não distingue
    # hifenização de fim de linha de palavras compostas.
    return re.sub(r'\s+',' ',re.sub(r'-\s*\n\s*|-','',text)).strip()

def relative_file(root, value):
    if not isinstance(value, str) or value in UNAVAILABLE:
        return False
    path = Path(value)
    if path.is_absolute():
        return False
    resolved = (root / path).resolve()
    return resolved.is_relative_to(root.resolve()) and resolved.is_file()

def verify(root=ROOT, release=False):
    root=Path(root)
    errors=[]
    warnings=[]
    tables={}
    for name, fields in HEADERS.items():
        try:
            with (root/'dados'/f'{name}.csv').open(encoding='utf-8',newline='') as f:
                reader=csv.DictReader(f)
                if reader.fieldnames != fields:
                    errors.append(f'{name}: cabeçalho diferente do contrato')
                tables[name]=list(reader)
                if any(None in row or any(v is None for v in row.values()) for row in tables[name]):
                    errors.append(f'{name}: linha com colunas a mais ou a menos')
        except (OSError,csv.Error) as exc:
            errors.append(f'{name}: {exc}')
            tables[name]=[]
    studies={}
    for s in tables['estudos']:
        sid=s.get('id')
        if not sid or sid in studies:
            errors.append(f'estudo duplicado ou sem ID: {sid}')
        studies[sid]=s
        if s.get('corpus') not in {'candidato','piloto','definitivo'}:
            errors.append(f'{sid}: corpus inválido')
        if s.get('metadados_conferidos') not in {'sim','nao'}:
            errors.append(f'{sid}: situação dos metadados inválida')
        if s.get('acesso_aberto') not in {'sim','institucional','nao','nao_conferido'}:
            errors.append(f'{sid}: situação do acesso aberto inválida')
        if s.get('corpus')=='definitivo' and s.get('acesso_aberto') not in {'sim','institucional'}:
            errors.append(f'{sid}: corpus definitivo sem texto acessível (I6, D69)')

    included=set()
    for row in tables['triagem']:
        sid=row.get('estudo_id')
        if sid not in studies: errors.append(f'triagem: estudo desconhecido {sid}')
        if row.get('fase') not in {'titulo_resumo','texto_completo'}: errors.append(f'{sid}: fase inválida')
        if row.get('decisao') not in {'incluir','excluir','duvida'}: errors.append(f'{sid}: decisão inválida')
        if row.get('natureza') not in {'ia','humano'}: errors.append(f'{sid}: natureza inválida')
        if not all(row.get(k) for k in ('criterio','motivo','responsavel','data')): errors.append(f'{sid}: triagem incompleta')
        codes=[x.strip() for x in (row.get('criterio') or '').split(';') if x.strip()]
        if any(c not in CRITERIA for c in codes): errors.append(f'{sid}: critério fora do protocolo')
        if row.get('decisao')=='excluir' and not any(c.startswith('X') for c in codes): errors.append(f'{sid}: exclusão sem critério X')
        if row.get('natureza')=='ia' and not row.get('prompt_versao'): errors.append(f'{sid}: decisão de IA sem versão do prompt')
        if row.get('fase')=='texto_completo' and row.get('natureza')=='humano':
            # Só o autor inclui no corpus (protocolo, seção 6). O último parecer humano
            # determina a inclusão atual; preservar o histórico.
            if row.get('decisao')=='incluir': included.add(sid)
            else: included.discard(sid)
    for sid,s in studies.items():
        if s.get('corpus')=='definitivo' and sid not in included:
            errors.append(f'{sid}: corpus definitivo sem inclusão no texto completo')

    extractions={}
    try:
        lines=(root/'dados/extracoes.jsonl').read_text(encoding='utf-8').splitlines()
    except OSError as exc:
        errors.append(str(exc)); lines=[]
    for number,line in enumerate(lines,1):
        if not line.strip(): continue
        try: e=json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f'extração linha {number}: JSON inválido: {exc.msg}');continue
        if not isinstance(e,dict):
            errors.append(f'extração linha {number}: objeto esperado');continue
        eid=e.get('id')
        if not eid or eid in extractions: errors.append(f'extração duplicada ou sem ID: {eid}')
        extractions[eid]=e
        missing=EXTRACTION_FIELDS-e.keys()
        if missing: errors.append(f'{eid}: faltam campos {sorted(missing)}')
        sid=e.get('estudo_id')
        if sid not in studies: errors.append(f'{eid}: estudo desconhecido {sid}')
        if e.get('status') not in {'nao_conferido','conferido_original','fonte_indisponivel'}:
            errors.append(f'{eid}: status inválido')
        if e.get('revisao_humana') not in {'pendente','confirmada'}:
            errors.append(f'{eid}: revisão humana inválida')
        if e.get('revisao_humana')=='confirmada' and not all(e.get(k) for k in ('revisor','data_revisao')):
            errors.append(f'{eid}: revisão humana sem responsável/data')
        result=e.get('resultado')
        if not isinstance(result,dict) or not {'baseline','intervencao'}<=result.keys():
            errors.append(f'{eid}: resultado deve conter baseline e intervencao'); result={}
        for key in ('baseline','intervencao'):
            value=result.get(key)
            if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float))):
                errors.append(f'{eid}: {key} deve ser número ou null')
            elif isinstance(value,(int,float)):
                if e.get('unidade')=='percentual' and not 0<=value<=100: errors.append(f'{eid}: percentual fora de 0–100')
                if e.get('unidade')=='proporcao' and not 0<=value<=1: errors.append(f'{eid}: proporção fora de 0–1')
        if e.get('unidade') not in {'percentual','proporcao','contagem','tempo','qualitativo'}:
            errors.append(f'{eid}: unidade inválida')
        if e.get('status')=='conferido_original':
            if not relative_file(root,e.get('fonte')): errors.append(f'{eid}: fonte primária não disponível localmente')
            if e.get('localizador') in UNAVAILABLE or not e.get('localizador'): errors.append(f'{eid}: sem localizador')
            if sid in studies:
                if studies[sid].get('metadados_conferidos')!='sim': errors.append(f'{eid}: metadados não conferidos')
                if e.get('fonte')!=studies[sid].get('fonte_primaria'): errors.append(f'{eid}: fonte diferente do estudo')
            if str(e.get('fonte','')).startswith('fontes/legado/'):
                errors.append(f'{eid}: documento legado não é artigo primário')
        if e.get('contrato')==2:
            missing=EXTRACTION_FIELDS_V2-e.keys()
            if missing: errors.append(f'{eid}: contrato 2 sem {sorted(missing)}')
            if not isinstance(e.get('riscos',[]),list) or not isinstance(e.get('mitigacoes',[]),list):
                errors.append(f'{eid}: riscos e mitigacoes devem ser listas')
            quotes=e.get('citacoes')
            if not isinstance(quotes,list) or not quotes or not all(isinstance(q,dict) and q.get('trecho') and q.get('localizador') for q in quotes):
                errors.append(f'{eid}: citações literais com localizador ausentes')
            elif e.get('status')=='conferido_original':
                if not relative_file(root,e.get('texto_fonte')):
                    errors.append(f'{eid}: texto da fonte não disponível localmente')
                else:
                    text=normalized((root/e['texto_fonte']).read_text(encoding='utf-8'))
                    for q in quotes:
                        if normalized(q['trecho']) not in text: errors.append(f'{eid}: citação não encontrada no texto da fonte')
        if release and sid in included and e.get('status')!='conferido_original':
            errors.append(f'{eid}: extração do corpus sem conferência no original')

    bib=(root/'monografia/referencias.bib').read_text(encoding='utf-8')
    bibkeys=set(re.findall(r'@\w+\s*\{\s*([^,\s]+)',bib))
    claims=set()
    for a in tables['afirmacoes']:
        aid=a.get('id')
        if not aid or aid in claims: errors.append(f'afirmação duplicada ou sem ID: {aid}')
        claims.add(aid)
        eids=[x.strip() for x in (a.get('extracao_ids') or '').split(';') if x.strip()]
        if a.get('status') not in {'rascunho','sustentada'}: errors.append(f'{aid}: status inválido')
        for eid in eids:
            if eid not in extractions: errors.append(f'{aid}: extração inexistente {eid}')
        if a.get('status')=='sustentada':
            if not eids: errors.append(f'{aid}: afirmação sem evidência')
            for eid in eids:
                if extractions.get(eid,{}).get('status')!='conferido_original': errors.append(f'{aid}: evidência {eid} não conferida')
            if not a.get('revisor') or not a.get('data_revisao'): errors.append(f'{aid}: revisão sem responsável/data')
            keys=[x.strip() for x in (a.get('bibkey') or '').split(';') if x.strip()]
            if not keys or any(k not in bibkeys for k in keys): errors.append(f'{aid}: chave bibliográfica ausente')
            if not relative_file(root,a.get('destino')): errors.append(f'{aid}: arquivo de destino ausente')
            else:
                text=(root/a['destino']).read_text(encoding='utf-8')
                if not re.search(r'AFIRMACAO:\s*'+re.escape(aid)+r'\b',text): errors.append(f'{aid}: marcador LaTeX ausente')
        if release and a.get('status')!='sustentada': errors.append(f'{aid}: afirmação ainda em rascunho')

    searches={row.get('id') for row in tables['buscas']}
    records=set()
    for row in tables['registros']:
        rid=row.get('id')
        if not rid or rid in records: errors.append(f'registro duplicado ou sem ID: {rid}')
        records.add(rid)
        if row.get('busca_id') not in searches: errors.append(f'registro {rid}: busca desconhecida')
        if row.get('estudo_id') and row.get('estudo_id') not in studies: errors.append(f'registro {rid}: estudo desconhecido')
    for row in tables['buscas']:
        if not relative_file(root,row.get('arquivo_exportacao')): errors.append(f'busca {row.get("id")}: exportação ausente')
        elif row['arquivo_exportacao'].endswith('manifesto.txt'):
            # O manifesto fixa as capturas originais; qualquer alteração aparece aqui.
            manifest=root/row['arquivo_exportacao']
            for line in manifest.read_text(encoding='utf-8').splitlines():
                digest,_,name=line.partition('  ')
                f=manifest.parent/name
                if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:
                    errors.append(f'busca {row.get("id")}: captura alterada ou ausente: {name}')
        try:
            if int(row.get('total_exportado',''))<0: raise ValueError
        except (ValueError,TypeError): errors.append('busca: contagem inválida')
    record_study={r.get('id'):r.get('estudo_id') for r in tables['registros']}
    for name in ('resumos','versoes_abertas'):
        for row in tables[name]:
            if row.get('estudo_id') not in studies: errors.append(f'{name}: estudo desconhecido {row.get("estudo_id")}')
    for row in tables['resumos']:
        if row.get('registro_id') and record_study.get(row['registro_id'])!=row.get('estudo_id'):
            errors.append(f'resumos: registro {row.get("registro_id")} não pertence a {row.get("estudo_id")}')
    # Coletas de verificação têm manifesto próprio, sem linha em buscas.csv.
    searched={(root/r['arquivo_exportacao']).resolve() for r in tables['buscas'] if r.get('arquivo_exportacao')}
    for manifest in sorted((root/'dados/brutos').glob('*/manifesto.txt')):
        if manifest.resolve() in searched: continue
        for line in manifest.read_text(encoding='utf-8').splitlines():
            digest,_,name=line.partition('  ')
            f=manifest.parent/name
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:
                errors.append(f'{manifest.parent.name}: captura alterada ou ausente: {name}')
    record_title={r.get('id'):r.get('titulo') for r in tables['registros']}
    for row in tables['correcoes_registros']:
        rid=row.get('registro_id')
        if rid not in record_title: errors.append(f'correcoes_registros: registro desconhecido {rid}')
        elif row.get('campo')!='titulo': errors.append(f'correcoes_registros: campo não previsto em {rid}')
        elif row.get('valor_capturado')!=record_title[rid]: errors.append(f'correcoes_registros: valor capturado diverge de registros.csv em {rid}')
        if not all(row.get(k) for k in HEADERS['correcoes_registros']): errors.append(f'correcoes_registros: correção incompleta em {rid}')
    for row in tables['deduplicacao']:
        if row.get('decisao') not in {'unir','separar'}: errors.append('deduplicacao: decisão inválida')
        if not all(row.get(k) for k in ('chave','registros','evidencia','responsavel','natureza','data')): errors.append('deduplicacao: adjudicação incompleta')
    for row in tables['qualidade']:
        if row.get('estudo_id') not in studies: errors.append('qualidade: estudo desconhecido')
        if row.get('criterio') not in QUALITY: errors.append('qualidade: critério inválido')
        if row.get('julgamento') not in {'atende','parcial','nao_atende','nao_informado'}: errors.append('qualidade: julgamento inválido')
        if not all(row.get(k) for k in ('localizador','justificativa','avaliador','data')): errors.append('qualidade: registro incompleto')
    for row in tables['fluxos']:
        try:
            if int(row.get('contagem',''))<0: raise ValueError
        except (ValueError,TypeError): errors.append('fluxo: contagem inválida')
        if not all(row.get(k) for k in ('denominador','regra','origem','data')): errors.append('fluxo: origem/denominador ausentes')

    for item in json.loads((root/'fontes/manifesto.json').read_text(encoding='utf-8')):
        p=root/item['arquivo']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            errors.append(f'legado alterado ou ausente: {item["arquivo"]}')

    if release:
        project=json.loads((root/'projeto.json').read_text(encoding='utf-8'))
        for key in ('protocolo_confirmado','template_institucional_confirmado','revisao_humana_final'):
            if project.get(key) is not True: errors.append(f'entrega: {key} pendente')
        if not tables['buscas']: errors.append('entrega: sem buscas registradas')
        if not included: errors.append('entrega: sem corpus incluído no texto completo')
        if not extractions: errors.append('entrega: sem extrações')
        if not tables['afirmacoes']: errors.append('entrega: sem mapa de afirmações')
        if not tables['qualidade']: errors.append('entrega: sem avaliação de qualidade')
        for sid in included:
            if studies.get(sid,{}).get('corpus')!='definitivo': errors.append(f'{sid}: inclusão sem corpus definitivo')
            related=[e for e in extractions.values() if e.get('estudo_id')==sid]
            if not related: errors.append(f'{sid}: estudo incluído sem extração')
            for e in related:
                if e.get('revisao_humana')!='confirmada': errors.append(f'{e.get("id")}: revisão humana pendente')
            criteria={r.get('criterio') for r in tables['qualidade'] if r.get('estudo_id')==sid}
            if criteria!=QUALITY: errors.append(f'{sid}: rubrica incompleta')
        for p in (root/'monografia').rglob('*.tex'):
            # O comando de macro é permitido; chamadas sinalizam conteúdo ainda pendente.
            if re.search(r'\\pendencia\{',p.read_text(encoding='utf-8')): errors.append(f'entrega: pendência em {p.relative_to(root)}')
    if not extractions: warnings.append('Estrutura inicial: nenhuma extração registrada; não há resultados validados por este fluxo.')
    warnings.append('Checagens estruturais não verificam a veracidade das fontes nem a sustentação semântica das afirmações.')
    return errors,warnings

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release',action='store_true')
    args=parser.parse_args()
    try: errors,warnings=verify(release=args.release)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(f'ERRO: não foi possível verificar: {exc}');return 1
    for warning in warnings: print('AVISO:',warning)
    for error in errors: print('ERRO:',error)
    print(f'{len(errors)} erro(s).')
    return bool(errors)

if __name__=='__main__':
    raise SystemExit(main())
