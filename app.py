import streamlit as st
import tempfile
import os
from gtts import gTTS
import base64

# Конфигуриране на страницата
st.set_page_config(
    page_title="Text to Speech App",
    page_icon="🔊",
    layout="wide"
)

# CSS за подобрен интерфейс
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .text-area {
        border-radius: 10px;
        padding: 15px;
        border: 2px solid #ddd;
    }
    .success-message {
        padding: 10px;
        background-color: #d4edda;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Заглавие
st.markdown('<h1 class="main-header">🔊 Text to Speech с gTTS</h1>', unsafe_allow_html=True)

# Описание
st.markdown("""
### Въведи текст и го преобразувай в аудио!
Това приложение използва Google Text-to-Speech (gTTS) за преобразуване на текст в говор.
Няма ограничения за дължина на текста! 📝
""")

# Функция за създаване на аудио файл
def text_to_speech(text, language='bg', slow=False):
    """
    Преобразува текст в аудио файл с gTTS
    """
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Грешка при преобразуването: {str(e)}")
        return None

# Функция за показване на аудио плеър
def display_audio_player(audio_file):
    """
    Показва аудио плеър в Streamlit
    """
    try:
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()
        
        # Кодиране в base64 за по-добро представяне
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'''
            <audio controls autoplay style="width: 100%">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Вашият браузър не поддържа аудио елемент.
            </audio>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Бутон за изтегляне
        st.download_button(
            label="📥 Изтегли аудио файл",
            data=audio_bytes,
            file_name="generated_speech.mp3",
            mime="audio/mp3"
        )
        
        return True
    except Exception as e:
        st.error(f"Грешка при показването на аудио: {str(e)}")
        return False

# Основен интерфейс
col1, col2 = st.columns([2, 1])

with col1:
    # Текстова област за въвеждане
    user_text = st.text_area(
        "Въведи текст тук:",
        height=300,
        placeholder="Въведете текста, който искате да преобразувате в говор...",
        help="Можете да въвеждате неограничено количество текст"
    )

with col2:
    # Настройки
    st.subheader("⚙️ Настройки")
    
    language_options = {
        'Български': 'bg',
        'Английски': 'en',
        'Немски': 'de',
        'Френски': 'fr',
        'Испански': 'es',
        'Италиански': 'it',
        'Руски': 'ru'
    }
    
    selected_language = st.selectbox(
        "Избери език:",
        options=list(language_options.keys()),
        index=0
    )
    
    speed_option = st.radio(
        "Скорост на говора:",
        ["Нормална", "Бавна"],
        help="Бавната скорост е по-ясна за дълги текстове"
    )

# Бутон за преобразуване
if st.button("🎵 Преобразувай в аудио", type="primary", use_container_width=True):
    if user_text.strip():
        with st.spinner("Преобразуване на текста в аудио... Моля, изчакайте."):
            # Преобразуване на текст в аудио
            audio_file = text_to_speech(
                text=user_text,
                language=language_options[selected_language],
                slow=(speed_option == "Бавна")
            )
            
            if audio_file:
                st.markdown('<div class="success-message">✅ Аудио файлът е успешно генериран!</div>', unsafe_allow_html=True)
                
                # Показване на аудио плеър
                display_audio_player(audio_file)
                
                # Почистване на временния файл
                try:
                    os.unlink(audio_file)
                except:
                    pass
                
                # Статистика
                st.info(f"📊 Статистика: {len(user_text)} символа, {len(user_text.split())} думи")
    else:
        st.warning("⚠️ Моля, въведете текст за преобразуване.")

# Допълнителна информация
with st.expander("ℹ️ Информация за приложението"):
    st.markdown("""
    ### Как работи това приложение?
    
    1. **Въвеждате текст** в текстовото поле (няма ограничения за дължина)
    2. **Избирате език** и скорост на говора
    3. **Натискате бутона** за преобразуване
    4. **Слушате резултата** директно в браузъра или го изтегляте
    
    ### Технически детайли:
    - Използва **gTTS (Google Text-to-Speech)** библиотеката
    - Поддържа **множество езици**
    - Генерира **MP3 файлове**
    - **Няма ограничения** за дължина на текста
    - Аудио файловете се генерират в реално време
    
    ### Поддържани езици:
    - Български, Английски, Немски, Френски, Испански, Италиански, Руски и много други
    """)

# Футър
st.markdown("---")
st.markdown("Създадено с ❤️ чрез Streamlit и gTTS")
