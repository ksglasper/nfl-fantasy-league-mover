# import codecademylib3_seaborn
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
prefix = "https://content.codecademy.com/courses/beautifulsoup/"
webpage_response = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')

webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

# print(soup)
chocolate_ratings = soup.find_all(attrs={"class": "Rating"})

ratings = []

for rating in chocolate_ratings:
    if(rating.get_text() == 'Rating'):
        continue
    ratings.append(float(rating.get_text()))


# print(ratings)
    
plt.hist(ratings)
plt.show()
