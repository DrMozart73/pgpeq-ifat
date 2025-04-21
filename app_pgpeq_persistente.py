
import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(layout="centered")

CONFIG_FILE = "config_docente.json"

# Función para guardar configuración en archivo
def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Función para cargar configuración desde archivo
def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

# Variables de sesión
if 'config_docente' not in st.session_state:
    config = cargar_configuracion()
    if config:
        st.session_state['config_docente'] = config
        st.session_state['docente_configurado'] = True
    else:
        st.session_state['docente_configurado'] = False
        st.session_state['config_docente'] = {}

if 'estudiantes_registrados' not in st.session_state:
    st.session_state['estudiantes_registrados'] = []

# Encabezado
def encabezado():
    config = st.session_state['config_docente']
    st.markdown(f"""
    <div style='background-color:#005baa;padding:10px;border-radius:10px;'>
        <h3 style='color:white;margin:0;'>Docente responsable del Curso: {config['curso']}</h3>
        <p style='color:white;margin:0;'>Profesor Dr. Gerson Díaz</p>
    </div>
    """, unsafe_allow_html=True)

# Configuración del docente
def configurar_docente():
    st.title("Configuración Inicial del Docente")

    curso = st.text_input("Nombre del curso")
    examen = st.text_input("Nombre del examen (aparecerá como PGPeq)")
    bloque = st.text_input("Código del bloque activo (ej. M)")
    num_preguntas = st.number_input("Número de preguntas", min_value=1, max_value=20, value=5, step=1)

    claves = []
    for i in range(num_preguntas):
        claves.append(st.selectbox(f"Clave correcta para Pregunta {i+1}", ['A','B','C','D'], key=f"clave_{i}"))

    clave_docente = st.text_input("Crea tu clave personal (solo una vez)", type="password")

    if st.button("Guardar configuración y continuar"):
        st.session_state['config_docente'] = {
            "curso": curso,
            "examen": examen,
            "bloque": bloque.upper(),
            "num_preguntas": num_preguntas,
            "claves": claves,
            "clave_docente": clave_docente
        }
        guardar_configuracion(st.session_state['config_docente'])
        st.session_state['docente_configurado'] = True
        st.rerun()

# Interfaz del estudiante
def interfaz_estudiante():
    st.title("TRAT PGPeq – Ingreso del Estudiante")

    nombre = st.text_input("Nombre del equipo o estudiante")
    bloque = st.text_input("Bloque asignado")

    if st.button("Ingresar"):
        bloque_actual = st.session_state['config_docente']['bloque']
        if bloque.upper() != bloque_actual:
            st.error("Este bloque no está habilitado actualmente.")
            return
        st.success("Ingreso exitoso. Espera el inicio del examen.")
        st.session_state['estudiantes_registrados'].append({
            "nombre": nombre,
            "bloque": bloque.upper(),
            "hora": datetime.datetime.now().strftime("%H:%M:%S"),
            "respuestas": [],
            "puntaje": 0
        })

# Panel docente en tiempo real
def panel_docente():
    st.subheader("Equipos Registrados")
    if st.session_state['estudiantes_registrados']:
        for i, est in enumerate(st.session_state['estudiantes_registrados']):
            st.markdown(f"- **{est['nombre']}** (Bloque {est['bloque']}) – conectado a las {est['hora']}")
    else:
        st.info("Aún no se ha registrado ningún estudiante.")

    if st.button("Iniciar examen (todos los conectados)"):
        st.session_state['iniciar_examen'] = True
        st.rerun()

# App principal
def main():
    if not st.session_state['docente_configurado']:
        configurar_docente()
    else:
        encabezado()
        modo = st.radio("Selecciona tu rol", ["Docente", "Estudiante"])

        if modo == "Docente":
            panel_docente()
        else:
            interfaz_estudiante()

main()
