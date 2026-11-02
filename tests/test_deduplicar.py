import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('deduplicar',ROOT/'scripts/deduplicar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

REG=['id','busca_id','titulo','ano','doi','arxiv','estudo_id']

class Deduplication(unittest.TestCase):
    """Dados sintéticos isolados; não usam o corpus da revisão."""
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/'dados').mkdir()
        self.write('estudos.csv',module.CAMPOS_ESTUDOS,[dict(id='S1',titulo='Estudo piloto sintético de referência',
            identificador='arXiv:0000.00001',versao='v1',ano='2024',origem='fixture',corpus='piloto',
            metadados_conferidos='nao',fonte_primaria='nao_conferido',acesso_aberto='nao_conferido')])
    def tearDown(self):
        self.tmp.cleanup()
    def write(self,name,fields,rows):
        with (self.root/'dados'/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
    def read(self,name):
        return (self.root/'dados'/name).read_text(encoding='utf-8')
    def records(self,*rows):
        self.write('registros.csv',REG,[dict(zip(REG,r+('',))) for r in rows])
    def test_rerun_without_identifiers_is_stable(self):
        self.records(('B1-0001','B1','Livro sintético sem identificador A','2025','',''),
                     ('B1-0002','B1','Livro sintético sem identificador B','2025','',''),
                     ('B1-0003','B1','Artigo sintético com DOI conhecido','2024','10.0000/x',''))
        self.assertEqual(module.main(self.root)[0],3)
        antes=(self.read('registros.csv'),self.read('estudos.csv'))
        self.assertEqual(module.main(self.root)[0],3)
        self.assertEqual(antes,(self.read('registros.csv'),self.read('estudos.csv')))
        self.assertNotIn('arXiv:,',self.read('estudos.csv'))
    def test_suspect_title_requires_adjudication(self):
        self.records(('B1-0001','B1','Titulo sintetico identico em duas versoes','2021','10.0000/a',''),
                     ('B2-0001','B2','Titulo sintetico identico em duas versoes','2025','10.0000/b',''))
        grupos,pendentes=module.main(self.root)
        self.assertEqual((grupos,len(pendentes)),(2,1))
        self.write('deduplicacao.csv',['chave','registros','decisao','evidencia','fonte','responsavel','natureza','data'],
                   [dict(chave='titulosinteticoidenticoemduasversoes',registros='B1-0001;B2-0001',
                         decisao='unir',evidencia='mesmos autores',fonte='sintetica',responsavel='teste',natureza='ia',data='2026-10-29')])
        self.assertEqual(module.main(self.root),(1,[]))
    def test_title_correction_groups_without_rewriting_record(self):
        self.records(('B1-0001','B1','Modelo sintetico: escala com caminhos','2022','','0000.00002'),
                     ('B3-0001','B3','Modelo sintetico','2023','10.0000/c',''))
        self.assertEqual(module.main(self.root)[0],2)
        self.write('correcoes_registros.csv',['registro_id','campo','valor_capturado','valor_corrigido','evidencia','fonte','responsavel','natureza','data'],
                   [dict(registro_id='B3-0001',campo='titulo',valor_capturado='Modelo sintetico',
                         valor_corrigido='Modelo sintetico: escala com caminhos',evidencia='subtítulo no HTML',
                         fonte='sintetica',responsavel='teste',natureza='ia',data='2026-11-01')])
        self.assertEqual(module.main(self.root)[0],1)
        self.assertIn('B3-0001,B3,Modelo sintetico,2023',self.read('registros.csv'))
        self.assertEqual(self.read('estudos.csv').count('Modelo sintetico'),1)

if __name__=='__main__':
    unittest.main()
