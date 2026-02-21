st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #0f172a 0%, #020617 100%); 
        color: #f8fafc; 
    }

    /* ESTILO DE BOTONES SUAVES (TRANSPARENTES) */
    .stButton>button {
        background-color: rgba(56, 189, 248, 0.05); /* Casi transparente */
        color: #94a3b8; /* Gris azulado suave, no blanco */
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 10px 20px;
        transition: all 0.4s ease;
        font-weight: 500;
        text-align: left;
    }

    /* EFECTO AL PASAR EL MOUSE (HOVER) */
    .stButton>button:hover {
        background-color: rgba(56, 189, 248, 0.15); /* Se ilumina sutilmente */
        border-color: #38bdf8;
        color: #38bdf8; /* El texto brilla en azul claro */
        transform: translateX(5px); /* Desplazamiento suave a la derecha */
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);
    }

    /* Animación del Gusanito (Ajustada para ser más lenta y menos molesta) */
    @keyframes worm-peek {
        0%, 100% { transform: translate(40px, 0px) scale(0); opacity: 0; }
        50% { transform: translate(0px, -45px) rotate(15deg) scale(1.1); opacity: 1; }
    }
    .apple-stage { position: relative; font-size: 7rem; text-align: center; margin: 15px 0; }
    .worm-move { position: absolute; font-size: 2.5rem; animation: worm-peek 6s infinite; left: 47%; top: 15%; }
    
    /* Pestañas (Tabs) más discretas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(56, 189, 248, 0.05);
        border-radius: 8px 8px 0 0;
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
