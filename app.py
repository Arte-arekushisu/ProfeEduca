# SUSTITUYE TU FUNCIÓN ACTUAL POR ESTA:
def generar_planeacion(tema):
    api_key = st.secrets["GEMINI_API_KEY"]
    # Cambiamos v1beta por v1, que es la ruta estable
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres un experto en el Modelo ABCD de CONAFE. Crea una planeación pedagógica para el tema: {tema}. Incluye un desafío, una meta y una ruta de aprendizaje."}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Esto nos dirá el error exacto si vuelve a fallar
            return f"Error de Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"
