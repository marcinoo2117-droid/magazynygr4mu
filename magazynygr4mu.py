import streamlit as st
import uuid

# Ustawienie tytułu i podstawowej konfiguracji strony
st.set_page_config(page_title="Prosta Lista Produktów", layout="centered")
st.title("🛍️ Prosta Lista Produktów")
st.markdown("Dodawaj i usuwaj produkty z listy. Dane **nie** są zapisywane trwale.")

# Inicjalizacja listy produktów w Streamlit Session State
# Używamy Session State, aby lista przetrwała przeładowania interfejsu Streamlit
# Każdy produkt to słownik z unikalnym ID i nazwą.
if 'product_list' not in st.session_state:
    st.session_state.product_list = [
        {"id": str(uuid.uuid4()), "name": "Mleko"},
        {"id": str(uuid.uuid4()), "name": "Chleb"},
        {"id": str(uuid.uuid4()), "name": "Jajka"},
    ]

# --- Funkcje do zarządzania listą ---

def add_product(new_product_name):
    """Dodaje nowy produkt do listy."""
    if new_product_name:
        st.session_state.product_list.append({
            "id": str(uuid.uuid4()),  # Generowanie unikalnego ID
            "name": new_product_name
        })

def delete_product(product_id_to_delete):
    """Usuwa produkt o podanym ID z listy."""
    st.session_state.product_list = [
        item for item in st.session_state.product_list
        if item["id"] != product_id_to_delete
    ]

# --- Sekcja dodawania produktu ---

st.header("➕ Dodaj Produkt")
# Utworzenie formularza do wprowadzania nowego produktu
with st.form(key='add_product_form'):
    # Pole tekstowe na nazwę produktu
    new_product_name = st.text_input("Nazwa nowego produktu:", key="new_product_input")
    # Przycisk do zatwierdzenia formularza
    submitted = st.form_submit_button("Dodaj do Listy")

    # Obsługa dodania produktu po kliknięciu przycisku
    if submitted:
        if new_product_name.strip(): # Sprawdzenie, czy pole nie jest puste
            add_product(new_product_name.strip())
            # Opcjonalnie: wyczyszczenie pola tekstowego po dodaniu
            st.session_state.new_product_input = ""
            st.rerun() # Ponowne uruchomienie, aby odświeżyć listę

# --- Sekcja wyświetlania i usuwania produktów ---

st.header("📋 Aktualna Lista Produktów")

if st.session_state.product_list:
    # Użycie st.container i st.columns do lepszej organizacji wizualnej
    for item in st.session_state.product_list:
        col1, col2 = st.columns([0.8, 0.2]) # Dwie kolumny: na nazwę i na przycisk

        with col1:
            st.write(f"**{item['name']}**") # Wyświetlenie nazwy produktu

        with col2:
            # Przycisk "Usuń" z unikalnym kluczem
            if st.button("Usuń", key=f"delete_{item['id']}", type="secondary"):
                delete_product(item["id"])
                st.rerun() # Ponowne uruchomienie, aby odświeżyć listę po usunięciu
else:
    st.info("Lista jest pusta. Dodaj pierwszy produkt!")

# --- Informacja o użyciu ---
st.markdown("---")
st.caption("Aplikacja zbudowana w Pythonie z użyciem Streamlit. Używa 'Session State' do utrzymania danych w trakcie sesji.")
