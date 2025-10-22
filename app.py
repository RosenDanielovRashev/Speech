import streamlit as st
import time
from collections import Counter
import re

# Конфигуриране на страницата
st.set_page_config(
    page_title="Реален Текст Анализатор",
    page_icon="⚡",
    layout="wide"
)

# CSS за по-добър визуален вид
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .real-time-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .word-cloud {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e6e6e6;
    }
</style>
""", unsafe_allow_html=True)

def analyze_text_in_real_time(text):
    """Анализира текста в реално време"""
    if not text.strip():
        return None
    
    # Основна статистика
    words = re.findall(r'\b\w+\b', text.lower())
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    sentences = len(re.findall(r'[.!?]+', text))
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    
    # Допълнителна статистика
    unique_words = len(set(words))
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    avg_sentence_length = len(words) / max(sentences, 1)
    
    # Най-често срещани думи
    word_freq = Counter(words)
    common_words = word_freq.most_common(15)
    
    # Процент на запълване (примерно изчисление)
    reading_time = len(words) / 200  # 200 думи в минута
    
    return {
        'words': len(words),
        'characters': characters,
        'characters_no_spaces': characters_no_spaces,
        'sentences': sentences,
        'paragraphs': paragraphs,
        'unique_words': unique_words,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'common_words': common_words,
        'reading_time': reading_time,
        'word_list': words
    }

def display_real_time_stats(stats):
    """Показва статистиките в реално време"""
    if not stats:
        return
    
    # Основни метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Думи", stats['words'])
    with col2:
        st.metric("🔤 Символи", stats['characters'])
    with col3:
        st.metric("📊 Уникални думи", stats['unique_words'])
    with col4:
        st.metric("⏱️ Време за четене", f"{stats['reading_time']:.1f} мин")

def main():
    # Заглавие с индикатор за реално време
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
        <h1 class="main-header">⚡ Реален Текст Анализатор</h1>
        <span class="real-time-badge">РЕАЛНО ВРЕМЕ</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Сайдбар за настройки
    with st.sidebar:
        st.header("⚙️ Настройки за анализ")
        
        analysis_depth = st.selectbox(
            "Детайлност на анализа:",
            ["Основна", "Разширена", "Пълна"]
        )
        
        auto_refresh = st.checkbox("Автоматично обновяване", value=True)
        show_live_preview = st.checkbox("Показвай текста в реално време", value=True)
        show_word_cloud = st.checkbox("Показвай честота на думи", value=True)
        
        if auto_refresh:
            st.info("Анализът се обновява автоматично при всяка промяна на текста")
        
        st.markdown("---")
        st.header("ℹ️ Информация")
        st.write("""
        Това приложение анализира текста ви в **реално време**.
        
        **Характеристики:**
        - Моментален анализ
        - Без записване на файлове
        - Неограничена дължина на текста
        - Детайлна статистика
        """)
    
    # Основна област
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Текстова област с автоматично обновяване
        st.subheader("🎯 Въведи текст за анализ")
        
        text = st.text_area(
            "Пишете тук:",
            height=400,
            placeholder="Започнете да пишете... Анализът ще се покаже веднага в дясната колона! ✨",
            key="real_time_input",
            label_visibility="collapsed"
        )
        
        # Индикатор за активност
        if text:
            words_count = len(re.findall(r'\b\w+\b', text.lower()))
            st.success(f"✅ Анализирани {words_count} думи в реално време!")
    
    with col2:
        st.subheader("📊 Жива статистика")
        
        # Анализ в реално време
        if text.strip():
            stats = analyze_text_in_real_time(text)
            
            if stats:
                # Показване на основни статистики
                display_real_time_stats(stats)
                
                st.markdown("---")
                
                # Детайлна статистика
                with st.expander("📈 Детайлен анализ", expanded=True):
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Символи без интервали:** {stats['characters_no_spaces']}")
                        st.write(f"**Изречения:** {stats['sentences']}")
                        st.write(f"**Параграфи:** {stats['paragraphs']}")
                    
                    with col2:
                        st.write(f"**Средна дължина на дума:** {stats['avg_word_length']:.1f}")
                        st.write(f"**Средна дължина на изречение:** {stats['avg_sentence_length']:.1f} думи")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Честота на думи
                if show_word_cloud and stats['common_words']:
                    with st.expander("🔤 Често срещани думи", expanded=True):
                        st.markdown('<div class="word-cloud">', unsafe_allow_html=True)
                        for word, count in stats['common_words'][:10]:
                            # Създаваме визуален индикатор за честота
                            percentage = (count / stats['words']) * 100
                            st.write(
                                f"`{word}`: {count} пъти ({percentage:.1f}%)"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Информация за плътност
                with st.expander("📊 Плътност на текста"):
                    if stats['words'] > 0:
                        diversity_ratio = stats['unique_words'] / stats['words']
                        st.write(f"**Разнообразие на думи:** {diversity_ratio:.2%}")
                        
                        if diversity_ratio > 0.7:
                            st.info("🎯 Текстът има високо лексикално разнообразие")
                        elif diversity_ratio > 0.4:
                            st.info("📝 Текстът има средно лексикално разнообразие")
                        else:
                            st.info("🔁 Текстът има ниско лексикално разнообразие")
        
        else:
            # Съобщение, когато няма текст
            st.info("💡 Започнете да пишете в лявата колона...")
            st.markdown("""
            **Ще видите тук:**
            - Брой думи и символи
            - Статистики за четене
            - Често срещани думи
            - И много други...
            """)
    
    # Допълнителна секция за преглед на текста
    if text and show_live_preview:
        st.markdown("---")
        st.subheader("👁️ Преглед на текста")
        
        # Показване на текста с номера на редове
        lines = text.split('\n')
        preview_text = ""
        for i, line in enumerate(lines, 1):
            preview_text += f"{i:3d}. {line}\n"
        
        st.text_area(
            "Текущ текст:",
            preview_text,
            height=200,
            key="preview_area",
            label_visibility="collapsed"
        )

if __name__ == "__main__":
    main()
