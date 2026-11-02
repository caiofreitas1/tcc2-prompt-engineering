import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verificar_acm',ROOT/'scripts/verificar_acm.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

ITEM=('<li class="search__item issue-item-container"><input name="10.0000/SINT.1" class="issue-Item__checkbox" type="checkbox">'
      '<div class="issue-heading">research-article</div>'
      '<div class="bookPubDate simple-tooltip__block--b" data-title="Published: 11 September 2026">September 2026</div>'
      '<h4 class="issue-item__title"><span><a href="/doi/10.0000/SINT.1">Título <span>sintético</span></a>: com&nbsp;subtítulo</span></h4></li>')

class AcmPage(unittest.TestCase):
    """HTML sintético no formato da página de resultados da ACM."""
    def test_item_keeps_subtitle_and_publication_date(self):
        self.assertEqual(module.itens('<ul>'+ITEM+ITEM.replace('SINT.1','SINT.2')+'</ul>',1),
            [[51,'research-article','September 2026','10.0000/SINT.1','Título sintético: com subtítulo','2026-09-11'],
             [52,'research-article','September 2026','10.0000/SINT.2','Título sintético: com subtítulo','2026-09-11']])

if __name__=='__main__':
    unittest.main()
