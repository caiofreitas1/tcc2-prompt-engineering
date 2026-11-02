import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('analisar_piloto',ROOT/'scripts/analisar_piloto.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def arq(*decisoes):
    return {f'S{n}':{'estudo_id':f'S{n}','decisao':d} for n,d in enumerate(decisoes,1)}

class Piloto(unittest.TestCase):
    def test_kappa_known_value(self):
        # Exemplo calculado à mão: po=0,7; pe=0,5 ⇒ κ=0,4.
        x=['segue']*5+['sai']*5
        y=['segue']*4+['sai']+['segue']*2+['sai']*3
        self.assertAlmostEqual(module.kappa(x,y,module.BINARIO),0.4)

    def test_union_excludes_only_with_both(self):
        self.assertEqual(module.uniao('excluir','excluir'),'sai')
        self.assertEqual(module.uniao('excluir','duvida'),'segue')
        self.assertEqual(module.uniao('incluir','excluir'),'segue')

    def test_loss_is_author_include_excluded_by_both(self):
        r=module.analisar(arq('incluir','incluir','duvida','excluir'),
                          arq('excluir','incluir','excluir','excluir'),
                          arq('excluir','excluir','excluir','excluir'))
        self.assertEqual(r['perdas'],['S1'])
        self.assertEqual(r['perdas_duvida'],['S3'])
        self.assertEqual(r['revocacao'],(1,2))
        self.assertEqual(r['revocacao_complementar'],(1,3))

    def test_different_studies_are_rejected(self):
        with self.assertRaises(ValueError):
            module.analisar(arq('incluir'),arq('incluir','excluir'),arq('incluir'))

class Recuo(unittest.TestCase):
    def test_task_block_matches_title_only(self):
        self.assertTrue(module.tarefa_no_titulo('Self-Debugging with LLMs'))
        self.assertTrue(module.tarefa_no_titulo('A Transpiler for Rust'))
        self.assertTrue(module.tarefa_no_titulo('Bug-fixing via prompts'))
        self.assertFalse(module.tarefa_no_titulo('Code review with LLMs'))

    def test_counts_only_titles_with_task(self):
        estudos={'S1':{'titulo':'Code generation'},'S2':{'titulo':'Agents'},'S3':{'titulo':'Debugging'}}
        linhas=[{'estudo_id':'S1','autor':'incluir','ia_a':'excluir','ia_b':'excluir','uniao':'sai'},
                {'estudo_id':'S2','autor':'incluir','ia_a':'excluir','ia_b':'excluir','uniao':'sai'}]
        r=module.recuo(linhas,estudos)
        self.assertEqual((r['candidatos'],r['candidatos_no_titulo'],r['amostra_no_titulo']),(3,2,1))
        self.assertEqual(r['perdas_no_titulo'],['S1'])
        self.assertEqual(r['autor_incluir_fora'],1)

if __name__=='__main__':
    unittest.main()
