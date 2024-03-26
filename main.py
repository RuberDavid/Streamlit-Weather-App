import sqlite3
import streamlit as st
import os
import pandas as pd
import modules.weather as we
import modules.dboperations as db
import modules.validations as val


DB_FILENAME = 'weather.db'
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH_FILENAME = os.path.join(base_dir, "databases", DB_FILENAME)
db.create_users_table(DB_PATH_FILENAME)

MAX_LONGITUDE = 179.99
MIN_LONGITUDE = -179.99
MAX_LATITUDE = 89.99
MIN_LATITUDE = -89.99
MAX_NAME_LEN = 40
MAX_EMAIL_LEN = 254

# END HEADER
##########################################################################################

st.title("Current and last month weather")

with st.form("user_form"):
    first_name = st.text_input("first name", max_chars=MAX_NAME_LEN)
    last_name = st.text_input("last name", max_chars=MAX_NAME_LEN)
    name = first_name + " " + last_name

    email = st.text_input("email", max_chars=MAX_EMAIL_LEN)

    try:
        if len(email) != 0 and not val.val_email(email):
            raise val.EmailNotValidError(email + "is not a valid email", errors={"email": email})
    except val.EmailNotValidError as errorMsg:
        print(str(errorMsg))
        st.text(str(errorMsg))

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input("latitude", max_value=MAX_LATITUDE, min_value=MIN_LATITUDE)#, format="%.2f", value=0.01, step=0.01)
    with col2:
        longitude = st.number_input("longitude", max_value=MAX_LONGITUDE, min_value=MIN_LONGITUDE)#, format="%.2f", value=0.01, step=0.01)
    location = {"latitude": latitude, "longitude": longitude}

    submitted = st.form_submit_button("Submit and get weather data")
    if submitted:
        if len(first_name) ==0 or len(last_name) == 0:
            st.write("first name and last name cannot be empty")
        elif not val.val_email(email):
            st.write("please provide a valid email")
        else:
            #look for weather data
            try:
                current_weather = we.get_current_weather(location)
                min_temp_last_month, max_temp_last_month, avg_temp_last_month = we.get_last_month_weather(location)

                # extract the db supported data
                # TODO: save JSON IN  db
                current_temperature = current_weather["current_temperature_2m"]
                current_weather_code = current_weather["current_weather_code"]

                # insert into DB
                try:
                    db.insert_into_users(DB_PATH_FILENAME, (name, email, latitude, longitude, current_temperature, current_weather_code ))
                    # show new data
                    st.subheader("")
                    st.markdown(f"""
                    
                            **name** : { name}
                            
                            **location**
                            - latitude : {latitude: }
                            - longitude : {longitude:}
                            
                            **Current temperature** : {current_temperature}°C
                            
                            **Last month weather data**
                            - Max  temperature: {max_temp_last_month:}°C
                            - Average temperature: { avg_temp_last_month:}°C
                            - Min temperature: { min_temp_last_month:}°C
                        """)
                    column_names, results = db.select_all_users(DB_PATH_FILENAME)
                    df_result = pd.DataFrame(results, columns=column_names)
                    #show all records
                    st.subheader("database entries:")
                    st.write(df_result)

                    #show all records
                except sqlite3.Error as e:
                    print(str(e))
                    st.write("couldn't store in database")
                    # show data
            except Exception as err:
                st.write("couldn't fetch weather data")
                st.write(err)
