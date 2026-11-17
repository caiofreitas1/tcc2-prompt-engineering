"""Buscas aproximadas de citações para o formulário de conferência (complementam verificar_citacoes_piloto).

Resultado positivo significa só que o trecho provavelmente está no texto extraído; não substitui a leitura do PDF.
"""
import bisect, re
def indice(tt):
    ix={}
    for i,w in enumerate(tt): ix.setdefault(w,[]).append(i)
    return ix
def aprox(tk,ix,salto=80,minimo=0.85):
    """Verdadeiro se ao menos `minimo` dos tokens (>= 3 letras) do trecho aparecem em ordem,
    cada um a no máximo `salto` tokens do anterior (texto em duas colunas intercaladas)."""
    tk=[w for w in tk if len(w)>=3]
    if len(tk)<4: return False
    for a in range(min(3,len(tk))):
        for ini in ix.get(tk[a],[]):
            pos=ini;k=1
            for w in tk[a+1:]:
                l=ix.get(w)
                if not l: continue
                j=bisect.bisect_right(l,pos)
                if j<len(l) and l[j]-pos<=salto:
                    pos=l[j];k+=1
            if k/len(tk)>=minimo: return True
    return False

def compacto(t): return re.sub(r'[\W_]+','',t)
def blocos(tk,ct,n=3,salto=700,minimo=0.85):
    """Verdadeiro se ao menos `minimo` dos blocos de `n` palavras do trecho, sem espaços,
    aparecem em ordem no texto sem espaços, cada um a até `salto` caracteres do anterior.
    Cobre palavras coladas e linhas intercaladas de duas colunas."""
    ch=[compacto(''.join(tk[i:i+n])) for i in range(0,len(tk),n)]
    ch=[c for c in ch if len(c)>=6]
    if len(ch)<2: return False
    ini=ct.find(ch[0]);
    starts=[]
    while ini!=-1 and len(starts)<200: starts.append(ini); ini=ct.find(ch[0],ini+1)
    for a in range(min(2,len(ch))):
        if a==1:
            starts=[];ini=ct.find(ch[1])
            while ini!=-1 and len(starts)<200: starts.append(ini); ini=ct.find(ch[1],ini+1)
        for s in starts:
            pos=s+len(ch[a]);k=1
            for c in ch[a+1:]:
                j=ct.find(c,pos)
                if j!=-1 and j-pos<=salto: pos=j+len(c);k+=1
            if k/len(ch)>=minimo: return True
    return False
