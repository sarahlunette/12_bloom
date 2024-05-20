import streamlit as st

#un get the data, randomly sur des indices qu'on n'a pas encore
#un display de la trajectoire avec pêche supposée en fonction de la vitesse
#un bouton qui nous permette de labeller: retourner un nouveau record avec la trajectoire et 0 ou 1 à inscrire dans une nouvelle base de données (BQ)


#Start labelling button
#un bouton si clicked on change d'image et on renvoie 0
#un bouton si clicked on change d'image et on renvoie 1

st.title("Trajectoires de pêche")

if st.button('Start labelling'):
  #instantiate
  #choose a record at random
  #create plot
  #st.pyplot(#trajectory)
  st.button('Fishing')
  st.button('Not Fishing')
  if st.button('Fishing'):
    #add record to csv with 1
    #change the record
    #check record is not in the csv
    #change figure (fig facile de changer)
    #st.session_state = False (unclick button to check)
  elif st.button('Not Fishing'):
    #add record to csv with 0
    #change the record
    #check record is not in the csv
    #change figure (fig facile de changer)
    #st.session_state = False (unclick button to check)

  # ou utiliser st.button("Submit", on_click=display_text), display_text is a function

