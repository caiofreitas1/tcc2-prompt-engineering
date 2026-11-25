"""Barreiras da tradução do artigo para o inglês (D141): cada arquivo de monografia/capitulos/ tem um par
em monografia/capitulos-en/ com os mesmos rótulos, citações, identificadores e números."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
import verificar_traducao as v  # noqa: E402

PT = r'''\subsection{Seleção}\label{sec:x}
% AFIRMACAO: A1
Em 17/11/2026, \citetexto{Hou et al.}{hou2024slr} contaram 2.304 estudos; a taxa foi de 3,2\% (S6-C1), como
mostra a Seção~\ref{sec:y}~\citep{page2021prisma}. De janeiro de 2021 a 09/2026, $\kappa = 0{,}745$.
'''
EN = r'''\subsection{Selection}\label{sec:x}
% AFIRMACAO: A1
On 17 November 2026, \citet{hou2024slr} counted 2,304 studies; the rate was 3.2\% (S6-C1), as
Section~\ref{sec:y} shows~\citep{page2021prisma}. From January 2021 to September 2026, $\kappa = 0.745$.
'''


class Traducao(unittest.TestCase):
    def test_par_equivalente_nao_tem_divergencia(self):
        self.assertEqual(v.comparar(PT, EN), [])

    def test_numero_trocado_e_acusado(self):
        erros = v.comparar(PT, EN.replace('2,304', '2,340'))
        self.assertTrue(any(e.startswith('números') for e in erros), erros)

    def test_decimal_trocado_e_acusado(self):
        erros = v.comparar(PT, EN.replace('0.745', '0.754'))
        self.assertTrue(any(e.startswith('números') for e in erros), erros)

    def test_data_trocada_e_acusada(self):
        erros = v.comparar(PT, EN.replace('17 November', '17 October'))
        self.assertTrue(any(e.startswith('números') for e in erros), erros)

    def test_identificador_perdido_e_acusado(self):
        erros = v.comparar(PT, EN.replace(' (S6-C1)', ''))
        self.assertTrue(any(e.startswith('identificadores') for e in erros), erros)

    def test_citacao_remissao_e_marca_perdidas_sao_acusadas(self):
        erros = v.comparar(PT, EN.replace(r'~\citep{page2021prisma}', ''))
        self.assertTrue(any(e.startswith('citações') for e in erros), erros)
        erros = v.comparar(PT, EN.replace(r'\ref{sec:y}', r'\ref{sec:z}'))
        self.assertTrue(any(e.startswith('remissões') for e in erros), erros)
        erros = v.comparar(PT, EN.replace('% AFIRMACAO: A1\n', ''))
        self.assertTrue(any(e.startswith('marcas') for e in erros), erros)

    def test_trecho_omitido_muda_a_estrutura(self):
        erros = v.comparar(PT + '\\begin{itemize}\n\\item um\n\\end{itemize}\n', EN)
        self.assertTrue(any(e.startswith('estrutura') for e in erros), erros)

    def test_capitulos_versionados_nao_tem_divergencia(self):
        self.assertEqual(v.verificar(RAIZ), [], 'tradução divergente: execute python3 scripts/verificar_traducao.py')

    def test_todo_capitulo_tem_traducao(self):
        pt = {p.name for p in (RAIZ / 'monografia/capitulos').glob('*.tex')} - {'00-resumo.tex'}
        en = {p.name for p in (RAIZ / 'monografia/capitulos-en').glob('*.tex')}
        self.assertEqual(pt, en)


if __name__ == '__main__':
    unittest.main()
