import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Display the table on the page.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table filtered
streamlit.dataframe(fruits_to_show)

#New Section to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
    # normalize the response 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # shows the response as a table
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

    






streamlit.stop()
streamlit.header("The fruit load list contains!:")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my__cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


#Second entry box
fruit_add = streamlit.text_input('What fruit would you like to add?','Jackfruit')
fruit_add_str = str(fruit_add)
my_cur.execute("INSERT INTO fruit_load_list VALUES (%s)", (fruit_add_str,))
streamlit.write('Thanks for adding ', fruit_add)


