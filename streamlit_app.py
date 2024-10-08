# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Example Streamlit App :cup_with_straw:")
st.write(
    """Choose the fruits you want in your customer Smoothies!
    """)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx=st.connection("snowflake")
mysession = cnx.session
my_dataframe = cnx.query("select fruit_name from smoothies.public.fruit_options")
#my_dataframe = mysession.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        cnx.query(my_insert_stmt)
        #mysession.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
