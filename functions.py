import requests
from bs4 import BeautifulSoup

url_main = "https://www.lego.com"
url_temas = "https://www.lego.com/es-mx/themes"

def get_temas(soup):
  temas = soup.find('section').ul
  temas = list(temas.find_all('li'))
  temas_info = []
  for tema in temas:
    tema_dic = {
        'name':tema.h2.span.text,
        'url': url_main + tema.a.get('href')
        }
    temas_info.append(tema_dic)
  return temas_info

def get_soup(url, page=1):
  if page == 1:
    r = requests.get(url)
  else:
    url = url + f"?page={page}&offset=0"
    r = requests.get(url)
  return BeautifulSoup(r.text, 'html.parser')

def get_toys_pages(soup):
  toys_grid = soup.find(id='product-listing-grid')
  try:
    n_toys = toys_grid.next_sibling.p.text
  except:
    n_toys = toys_grid.next_sibling.label.text
  
  n_toys = int(n_toys.split(' ')[-2])

  n_pages = n_toys // 18 + 1
  return n_toys, n_pages

def detect_info_type(data):
  data_n = {
      'age': None,
      'pieces': None,
      'cal': None
  }

  for d in data:
    if "+" in d:
      data_n['age'] = d
    elif "." in d:
      data_n['cal'] = d
    else:
      data_n['pieces'] = d
  return data_n

def discount_price(toy):
  price = toy.h3.find_next('div').text
  if "%" in price:
    r_price = "$" + price.split("$")[1]
    discount = price.split(" ")[-1]
    return r_price, discount
  else:
    return price, 0

def get_toys_values(soup, name):
  toys_grid = soup.find(id='product-listing-grid')
  toys = [li for li in toys_grid.find_all('li') if li.find('article')]
  print(len(toys))
  toys_data=[]
  for toy in toys:
    # print(f"Obteniendo {toy.h3.text}")
    data = list(toy.h3.find_previous_sibling("div").find_all('span')) #div info
    data = [data.text for data in data]
    data = detect_info_type(data)
    # print(data)

    price, discount = discount_price(toy)
    toy_info = {
          'toy_name': toy.h3.text,
          'colection': name,
          "price": price,
          "discount": discount,
          'age': data['age'],
          'pieces': data['pieces'],
          'calification': data['cal']
    }
    toys_data.append(toy_info)
  return toys_data


