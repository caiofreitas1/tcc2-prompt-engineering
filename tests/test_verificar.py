import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verificar',ROOT/'scripts/verificar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ScientificDataChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        for folder in ['dados','fontes','monografia']:
            shutil.copytree(ROOT/folder,self.root/folder)
        shutil.copyfile(ROOT/'projeto.json',self.root/'projeto.json')
        # Os testes usam dados sintéticos, independentemente do avanço da revisão.
        # make check valida os dados reais antes de executar esta suíte.
        study=dict(id='S1',titulo='Estudo sintético',identificador='sintetico',
                   versao='teste',ano='2025',origem='fixture_teste',corpus='piloto',
                   metadados_conferidos='nao',fonte_primaria='nao_conferido',
                   acesso_aberto='nao_conferido')
        for name,fields in module.HEADERS.items():
            with (self.root/'dados'/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
                writer=csv.DictWriter(f,fieldnames=fields)
                writer.writeheader()
                if name=='estudos': writer.writerow(study)
        (self.root/'dados/extracoes.jsonl').write_text('',encoding='utf-8')
    def tearDown(self):
        self.tmp.cleanup()
    def extraction(self,**changes):
        row=dict(id='E_TEST',estudo_id='S1',tarefa='geracao',tecnica='teste_sintetico',modelo='sintetico',benchmark='sintetico',metrica='teste',unidade='percentual',comparador='sintetico',resultado={'baseline':40,'intervencao':50},localizador='Tabela sintética',fonte='fontes/artigos/sintetico.txt',status='nao_conferido',revisao_humana='pendente')
        row.update(changes)
        (self.root/'dados/extracoes.jsonl').write_text(json.dumps(row)+'\n')
        return row
    def test_bootstrap_is_valid_but_not_releasable(self):
        self.assertEqual([],module.verify(self.root)[0])
        self.assertTrue(module.verify(self.root,release=True)[0])
    def test_unknown_study_is_rejected(self):
        self.extraction(estudo_id='S_INEXISTENTE')
        self.assertTrue(any('estudo desconhecido' in x for x in module.verify(self.root)[0]))
    def test_checked_original_passes_structural_checks(self):
        source=self.root/'fontes/artigos/sintetico.txt'
        source.parent.mkdir(parents=True,exist_ok=True)
        source.write_text('Fonte sintética exclusiva do teste; não integra a revisão.')
        p=self.root/'dados/estudos.csv'
        with p.open(newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        rows[0]['metadados_conferidos']='sim'
        rows[0]['fonte_primaria']='fontes/artigos/sintetico.txt'
        with p.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
        self.extraction(status='conferido_original')
        self.assertEqual([],module.verify(self.root)[0])
    def test_invalid_percent_is_rejected(self):
        self.extraction(resultado={'baseline':0,'intervencao':120})
        self.assertTrue(any('percentual fora' in x for x in module.verify(self.root)[0]))
    def test_original_requires_source_and_metadata(self):
        self.extraction(status='conferido_original')
        errors=module.verify(self.root)[0]
        self.assertTrue(any('fonte primária' in x for x in errors))
        self.assertTrue(any('metadados não conferidos' in x for x in errors))
    def test_human_review_needs_identity(self):
        self.extraction(revisao_humana='confirmada')
        self.assertTrue(any('responsável/data' in x for x in module.verify(self.root)[0]))
    def test_supported_claim_requires_checked_evidence(self):
        self.extraction()
        with (self.root/'dados/afirmacoes.csv').open('a',newline='') as f:
            writer=csv.writer(f)
            writer.writerow(['A_TEST','Afirmação sintética','E_TEST','','monografia/main.tex','sustentada','',''])
        self.assertTrue(any('não conferida' in x for x in module.verify(self.root)[0]))
    def test_legacy_cannot_be_original_article(self):
        self.extraction(status='conferido_original',fonte='fontes/legado/analise-inicial.docx')
        self.assertTrue(any('legado não é artigo' in x for x in module.verify(self.root)[0]))
    def test_imported_sources_are_immutable(self):
        p=self.root/'fontes/legado/analise-inicial.docx'
        p.write_bytes(b'arquivo alterado no teste')
        self.assertTrue(any('legado alterado' in x for x in module.verify(self.root)[0]))
    def screening(self,**changes):
        row=dict(estudo_id='S1',fase='texto_completo',decisao='incluir',criterio='I1;I2;I3;I4;I5;I6',motivo='sintético',responsavel='ia-A',natureza='ia',prompt_versao='tc-v1',data='2026-10-27')
        row.update(changes)
        with (self.root/'dados/triagem.csv').open('a',newline='',encoding='utf-8') as f:
            csv.DictWriter(f,fieldnames=module.HEADERS['triagem']).writerow(row)
    def set_study(self,**changes):
        p=self.root/'dados/estudos.csv'
        with p.open(newline='',encoding='utf-8') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        rows[0].update(changes)
        with p.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    def test_ai_inclusion_does_not_define_corpus(self):
        self.set_study(corpus='definitivo',acesso_aberto='sim')
        self.screening()
        self.assertTrue(any('sem inclusão no texto completo' in x for x in module.verify(self.root)[0]))
        self.screening(responsavel='autor',natureza='humano',prompt_versao='')
        self.assertEqual([],module.verify(self.root)[0])
    def test_definitive_corpus_requires_open_access(self):
        self.set_study(corpus='definitivo')
        self.screening(responsavel='autor',natureza='humano',prompt_versao='')
        self.assertTrue(any('sem texto aberto' in x for x in module.verify(self.root)[0]))
    def test_screening_uses_protocol_criteria(self):
        self.screening(fase='titulo_resumo',decisao='excluir',criterio='I2')
        errors=module.verify(self.root)[0]
        self.assertTrue(any('exclusão sem critério X' in x for x in errors))
        self.screening(fase='titulo_resumo',decisao='excluir',criterio='X9')
        self.assertTrue(any('critério fora do protocolo' in x for x in module.verify(self.root)[0]))
    def test_ai_screening_requires_prompt_version(self):
        self.screening(prompt_versao='')
        self.assertTrue(any('sem versão do prompt' in x for x in module.verify(self.root)[0]))
    def test_record_requires_known_search(self):
        with (self.root/'dados/registros.csv').open('a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(['R1','B_INEXISTENTE','Título sintético','2025','','','S1'])
        self.assertTrue(any('busca desconhecida' in x for x in module.verify(self.root)[0]))
    def test_summary_requires_known_study(self):
        with (self.root/'dados/resumos.csv').open('a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(['S_INEXISTENTE','','openalex','Resumo sintético.'])
        self.assertTrue(any('resumos: estudo desconhecido' in x for x in module.verify(self.root)[0]))
    def test_altered_capture_is_rejected(self):
        folder=self.root/'dados/brutos/sintetico'
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'pagina-001.xml').write_text('captura sintética',encoding='utf-8')
        (folder/'manifesto.txt').write_text('0'*64+'  pagina-001.xml\n',encoding='utf-8')
        with (self.root/'dados/buscas.csv').open('a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(['B_TESTE','2026-10-29','arxiv','consulta sintética','filtros','0','dados/brutos/sintetico/manifesto.txt','teste'])
        self.assertTrue(any('captura alterada' in x for x in module.verify(self.root)[0]))
    def test_deduplication_decision_must_be_valid(self):
        with (self.root/'dados/deduplicacao.csv').open('a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(['titulosintetico','R1;R2','talvez','evidência','fonte','teste','ia','2026-10-29'])
        self.assertTrue(any('deduplicacao: decisão inválida' in x for x in module.verify(self.root)[0]))
    def contract2(self,quote):
        text=self.root/'fontes/textos/sintetico.txt'
        text.parent.mkdir(parents=True,exist_ok=True)
        text.write_text('O método atingiu Pass@1 de 50,0% no bench-\nmark sintético.',encoding='utf-8')
        source=self.root/'fontes/artigos/sintetico.txt'
        source.parent.mkdir(parents=True,exist_ok=True)
        source.write_text('Fonte sintética exclusiva do teste.')
        self.set_study(metadados_conferidos='sim',fonte_primaria='fontes/artigos/sintetico.txt')
        self.extraction(status='conferido_original',contrato=2,texto_fonte='fontes/textos/sintetico.txt',
                        citacoes=[{'trecho':quote,'localizador':'Tabela sintética'}],riscos=[],mitigacoes=[],prompt_versao='ex-v1')
    def test_contract2_quote_must_exist_in_source_text(self):
        self.contract2('Pass@1 de 50,0% no benchmark sintético')
        self.assertEqual([],module.verify(self.root)[0])
        self.contract2('Pass@1 de 75,0% no benchmark sintético')
        self.assertTrue(any('citação não encontrada' in x for x in module.verify(self.root)[0]))
    def test_contract2_requires_quotes(self):
        self.extraction(contrato=2,texto_fonte='',citacoes=[],riscos=[],mitigacoes=[],prompt_versao='ex-v1')
        self.assertTrue(any('citações literais' in x for x in module.verify(self.root)[0]))
    def test_source_path_cannot_escape_repository(self):
        self.assertFalse(module.relative_file(self.root,'../fora.txt'))
        self.assertFalse(module.relative_file(self.root,str(ROOT/'README.md')))

if __name__=='__main__':
    unittest.main()
