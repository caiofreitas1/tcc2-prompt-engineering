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
                   metadados_conferidos='nao',fonte_primaria='nao_conferido')
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
    def test_source_path_cannot_escape_repository(self):
        self.assertFalse(module.relative_file(self.root,'../fora.txt'))
        self.assertFalse(module.relative_file(self.root,str(ROOT/'README.md')))

if __name__=='__main__':
    unittest.main()
