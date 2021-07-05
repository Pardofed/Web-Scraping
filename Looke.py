from json import dump
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import csv



URL = "https://www.looke.com.br"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#Revisar la direccion del chromedriver.exe
driver = webdriver.Chrome("./chromedriver.exe",chrome_options=options)


def GetLinks(gen):
    driver.get("https://www.looke.com.br/home")
    botonmenu = driver.find_element_by_id('menu-item-genero')
    hover = ActionChains(driver).move_to_element(botonmenu)
    hover.perform()
    secondLevelMenu = driver.find_element_by_xpath("//a[contains(text(),'"+ gen + "')]")
    secondLevelMenu.click()

    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    SCROLL_PAUSE_TIME = 1

    
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        
        time.sleep(SCROLL_PAUSE_TIME)

       
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(4)

    links = []
    items = driver.find_elements_by_xpath("//img[@itemprop='image' and contains(@class,'imgBase')]")

    for i in items:
        url = i.get_attribute('onclick')
        url = url.split('\'')
        links.append(URL + str(url[1]))
    
    return links
    
def GetDetails(url):
    driver.get(url)
    details = driver.find_elements_by_class_name("detailsMedia")
    
    for detail in details:
        titulo = detail.find_element_by_class_name("detailTitle").text
        detailsYear = detail.find_element_by_class_name("detailsYear").text
        generos = detail.find_element_by_class_name("detailsGenre").text
        movieActorsContainer = detail.find_elements_by_tag_name("a")

        actores = []
        for act in movieActorsContainer:
            actores.append(act.get_attribute('innerHTML'))

        actores = ",".join(actores) 
        detailsYear = detailsYear.split('|')
        anio = detailsYear[0]
        duracion = detailsYear[2].strip()
        
        
        print("Titulo:"+titulo)
        print("Anio:"+anio)
        print("Duracion:"+duracion)
        print("Genero:"+generos)
        print("Actores:"+actores)

        
        peli = [titulo, int(anio), generos, str(duracion), actores]

    return peli
        


# #########################################
# Obtener lista de todos los generos para utilizarlo en acceso a links
# #########################################

def GetGenres():
    driver.get(URL)
    filmes_gener = driver.find_elements_by_xpath("//div[contains(@class,'genero')]")
    

    generos = []

    for ele in filmes_gener:
        tag_a = ele.find_elements_by_tag_name('a')
        for a in tag_a:
            generos.append(a.get_attribute('innerHTML'))
    return generos

def InsertInDB(titulo,anio,genero,duracion,reparto):
    query = "INSERT INTO peliculas (titulo,anio,genero,duracion,reparto) VALUES (?,?,?,?,?);"
    values = (titulo,anio,genero,duracion,reparto)
    cur = con.cursor()
    cur.execute(query,values)
    con.commit()
    cur.close()

def ExportToCSV(data):
    hearder = ['Titulo','Anio','Genero','Duracion','Reparto']

    with open('peliculas.csv','w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(hearder) #Escribir encabezado
        writer.writerows(data) # Utilizar lista de lista


# ---------------------------------------------------------

generos = GetGenres() 
films_links = []
lista_pelis = []

for genero in generos:
    links_obtenidos = GetLinks(genero)  

    for link in links_obtenidos:
        films_links.append(link)    

films_links = list(set(films_links)) 

for link in films_links:
    lista_pelis.append(GetDetails(link))



ExportToCSV(lista_pelis)




