'''
This script scrapes LaTercera.cl
'''
import urllib, urllib2
import bs4,pprint,datetime,sys,os


def get_html(url):
    return urllib2.urlopen(url).read()


def get_titulares(html):
    '''
        Esto busca todos los links a noticias que estan en un "DIV" 
        de clase BoxContenedor Titular
    '''
    soup = bs4.BeautifulSoup(html)
    titulares = [a.attrs.get('href') for a in soup.select('div.titular a')]
    return list(set(titulares))


def get_noticias(titulares):
    '''
        Con una lista de URLs a titulares
        este metodo devuelve una lista donde cada elemento es 
        un diccionario {'titular': '...','fecha':'YYY-MM-DD', 'texto':texto de la noticia}
    '''
    # por cada titular, obtener el html.
    n=[]
    for titular in titulares:
        try:
            html = urllib.urlopen(titular).read()
            n.append(get_meta(html))
        except:
            print datetime.datetime.now(),"Could not read",titular
    return n


def get_meta(html):
    soup = bs4.BeautifulSoup(html)
    titulo = soup.select('h1.titularArticulo')[0].text
    print "Processing: ",titulo.encode('utf-8')
    l = soup.find_all('meta')
    fecha = [d.attrs['content'] for d in l if d.get('name','')=='date'][0]
    lede = [d.attrs['content'] for d in l if d.get('name','')=='description'][0]
    parrafos = [p.text for p in soup.select('.articleContent p')]
    return {'titulo':titulo, 'fecha':fecha, 'lede':lede, 'pars':parrafos}



def save_noticias(noticias,fname):
    '''
        Noticias es una lista que viene de get_noticias.
    '''
    f = open(fname,"w")
    f.write(pprint.pformat(noticias).encode('utf-8'))
    f.close()



def process_noticias(url,out_filename):
    h=get_html(url)
    t=get_titulares(h)
    n=get_noticias(t)
    save_noticias(n,out_filename)
    

if __name__=="__main__":
    p = os.path.abspath("/home/fiacobelli/research/umayor/diversity/")
    fname=p+"/tercera-"+str(datetime.datetime.now()).replace(" ","_").replace(":","-")+".txt"
    url_politica = "http://www.latercera.com/canal/politica/674.html"
    process_noticias(url_politica,fname)
        
