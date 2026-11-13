"""Verificação aproximada de citações literais no texto extraído em duas colunas (D101).

Retorna contiguo, intercalado ou nao; nao significa só que a busca falhou, não que o trecho não exista no PDF.
"""
import re,unicodedata
def norm(t):
    t=unicodedata.normalize('NFKC',t)
    t=re.sub(r'-\s*\n\s*','',t)
    t=re.sub(r'[‘’]',"'",t); t=re.sub(r'[“”]','"',t); t=re.sub(r'[–—]','-',t)
    return re.sub(r'\s+',' ',t).strip().lower()
def toks(t): return re.findall(r'\w+',t)
def subseq(tk,tt,i,lim):
    j=i;k=0
    while j<len(tt) and j<lim and k<len(tk):
        w=tt[j]
        if w==tk[k]: k+=1
        elif len(w)>=2 and tk[k].startswith(w):   # palavra hifenizada no meio da linha
            resto=tk[k][len(w):]
            for j2 in range(j+1,min(j+60,len(tt))):
                if tt[j2]==resto or tt[j2].startswith(resto) and False: break
            else: j+=1; continue
            k+=1; j=j2
        elif tk[k] in w and len(tk[k])>=4: k+=1      # palavras coladas no texto extraído
        j+=1
    return k==len(tk)
def verif(trecho,texto,tt):
    n=norm(trecho)
    if n and n in texto: return 'contiguo'
    tk=toks(n)
    if not tk: return 'nao'
    for i,x in enumerate(tt):
        if (x==tk[0] or (len(tk[0])>=4 and tk[0] in x)) and subseq(tk,tt,i,i+8*len(tk)+40): return 'intercalado'
    return 'nao'
