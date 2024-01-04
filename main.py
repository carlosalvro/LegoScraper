import pandas as pd
from functions import *

if __name__=="__main__":
  #Obtenemos los temas
  soup = get_soup(url_temas)
  temas = get_temas(soup)
  temas_dt = pd.DataFrame(temas)

  #Obtenemos los sets
  data = []
  for index, row in temas_dt.iterrows():
    print(f"Descargando {row['name']} ...")

    soup = get_soup(row['url'])
    n_toys, n_pages = get_toys_pages(soup)
    data_tema = []
    print(f"Descargando {n_toys} juguetes")

    for i in range(1, n_pages + 1):
      soup = get_soup(row['url'], page=i)
      data_tema += get_toys_values(soup, row['name'])
      print(f"Se obtuvieron {len(data_tema)} datos, faltan {n_toys-len(data_tema)}")
    print(f"{row['name']} Terminado")
    data += data_tema


  #Guardamos los datos
  data_dt = pd.DataFrame(data)
  data_dt.to_csv("lego_data.csv")