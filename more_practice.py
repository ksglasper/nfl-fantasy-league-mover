from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


prefix = "https://content.codecademy.com/courses/beautifulsoup/"
webpage_response = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')

webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

# print(soup)
chocolate_ratings = soup.find_all(attrs={"class": "Rating"})

ratings = []

for rating in chocolate_ratings[1:]:
    ratings.append(float(rating.get_text()))

plt.hist(ratings)
plt.show()

# print(ratings)

names = []
company_names = soup.select(".Company")
# print(company_names)
for name in company_names[1:]:
    names.append(name.get_text())

# print(names)
    
d = {"Company" : names, "Ratings" : ratings}
chocolate_df = pd.DataFrame.from_dict(d)
print(chocolate_df.nlargest(4, 'Ratings', keep='all'))
average_rating = chocolate_df.groupby(['Company']).Ratings.mean()
top_ten = average_rating.nlargest(10)
print(top_ten)

