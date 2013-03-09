import StringIO
import gzip
import urllib2
from bs4 import BeautifulSoup
from unicodedata import normalize 

# Funcao que extrai a lista de ingredientes de uma html de receitas do receitas.com
def PegarIngredientes(url,blacklist):
    
    html  = urllib2.urlopen(url) # abre a pagina
    sucesso = False # para verificar se a pagina tinha receita

    # verifica se a pagina veio 'zipada'
    if html.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO( html.read()) # se sim, le em modo buffer
        gzip_f = gzip.GzipFile(fileobj=buf) # para poder passar ao objeto gzip
        html_doc = gzip_f.read() # que entao extrai o conteudo correto
    else:
        html_doc = html.read()
        
    soup = BeautifulSoup(html_doc) # BeautifulSoup eh um parser de html

    NomeReceita = ''.join(soup.title.contents).replace(' ','_').replace('|','').replace('\n','') # o nome da receita esta no titulo da pagina, remove os espacos e |
    

    ListaIngredientes = soup.find_all(itemprop=u'ingredients')   # procura por todas as tags com itemprop='ingredients'
    if len(ListaIngredientes) > 0:
        sucesso = True                             # se existe alguma tag assim, entao eh uma receita
        fw = open('receitas\\'+NomeReceita+'.txt','w')   # escreve a receita no diretorio 'receitas'
        for ingrediente in ListaIngredientes:            # para cada ingrediente da lista
            ingredienteStr = ''.join(ingrediente.contents)     # gera a string com o conteudo da tag
            ingredienteStr = normalize('NFKD', ingredienteStr).encode('ASCII','ignore')  # substitui os caracteres acentuados 
            try:
                fw.write(ingredienteStr)    # escreve o ingrediente no arquivo
            except:
                print ingredienteStr
            fw.write('\n')
        fw.close()

    blacklist.append(url)  # coloca essa url na blacklist, nao queremos visita-la novamente
    ListaReceitas = []
    ListaLinks = soup.find_all("a") # busca por todas as tags <a> que representam urls
    for link in ListaLinks:
        if link.has_key('href'):      # se eh uma url, vai ter a opcao href
            url_novo = link['href']

            # se a url esta na pasta receitas do servidor do receita.com
            # e for completa (comeca com http://
            # e nao estiver na blacklist
            if url_novo.find('/receitas/') > -1 and url_novo.find('http://') > -1  and url_novo not in blacklist:
                ListaReceitas.append(url_novo)  # armazena na lista de urls

    
    return ListaReceitas, sucesso, blacklist # retorna a lista de receitas, se essa era uma receita e a nova blacklist
        

qtde = input('Quantas receitas? ')
url_init = 'http://tvg.globo.com/receitas/lasanha-de-presunto-e-queijo-50de0706c5a6453794000046'
ListaReceitas = set()
(novaLista,sucesso,blacklist)= PegarIngredientes(url_init,[])
ListaReceitas=ListaReceitas.union(set(novaLista))
it = 1

while it < qtde:
    url = ListaReceitas.pop()
    (novaLista, sucesso,blacklist) = PegarIngredientes(url,blacklist)
    ListaReceitas=ListaReceitas.union(set(novaLista))
    if sucesso:
        it += 1
