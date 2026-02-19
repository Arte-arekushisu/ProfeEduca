# SUSTITUYE TU FUNCIÓN ACTUAL POR ESTA:
def generar_con_gemini(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Cambiamos la URL a la versión de producción que acepta tu llave AIza...
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Actúa como tutor CONAFE experto en el Modelo ABCD. Para el tema '{tema}', genera un desafío, una meta y una ruta de aprendizaje clara."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Esto te dirá exactamente qué dice Google si algo falla
            error_detalle = response.json().get('error', {}).get('message', 'Error desconocido')
            return f"Error de Google ({response.status_code}): {error_detalle}"
    except Exception as e:
        return f"Error de conexión: {e}"
