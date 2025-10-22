import streamlit as st
import re
from collections import Counter
import nltk
from textblob import TextBlob

# Конфигуриране на страницата
st.set_page_config(
    page_title="Анализатор на Изречения",
    page_icon="🔤",
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
    .sentence-box {
        background-color: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sentence-number {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.9rem;
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
    .word-count-badge {
        background-color: #28a745;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def split_into_sentences(text):
    """Разделя текста на изречения с подобрен алгоритъм"""
    if not text.strip():
        return []
    
    # Патърн за разделяне на изречения (подобрен)
    sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\…)\s'
    
    # Разделяне на изречения
    sentences = re.split(sentence_endings, text)
    
    # Филтриране на празни изречения и премахване на водещи/завършващи интервали
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    return sentences

def analyze_sentence(sentence, sentence_num):
    """Анализира отделно изречение"""
    words = re.findall(r'\b\w+\b', sentence.lower())
    characters = len(sentence)
    characters_no_spaces = len(sentence.replace(" ", ""))
    
    return {
        'number': sentence_num,
        'text': sentence,
        'words': len(words),
        'characters': characters,
        'characters_no_spaces': characters_no_spaces,
        'word_list': words
    }

def analyze_text_in_real_time(text):
    """Анализира текста в реално време с фокус върху изреченията"""
    if not text.strip():
        return None
    
    # Разделяне на изречения
    sentences = split_into_sentences(text)
    
    # Анализ на всяко изречение
    analyzed_sentences = [analyze_sentence(sent, i+1) for i, sent in enumerate(sentences)]
    
    # Обща статистика
    all_words = []
    for sent in analyzed_sentences:
        all_words.extend(sent['word_list'])
    
    total_words = len(all_words)
    total_characters = len(text)
    total_characters_no_spaces = len(text.replace(" ", ""))
    
    # Статистика за изреченията
    sentence_stats = {
        'count': len(sentences),
        'avg_words_per_sentence': total_words / len(sentences) if sentences else 0,
        'avg_chars_per_sentence': total_characters / len(sentences) if sentences else 0,
        'shortest_sentence': min(sentences, key=len) if sentences else "",
        'longest_sentence': max(sentences, key=len) if sentences else ""
    }
    
    # Допълнителна статистика
    unique_words = len(set(all_words))
    avg_word_length = sum(len(word) for word in all_words) / total_words if total_words > 0 else 0
    reading_time = total_words / 200  # 200 думи в минута
    
    # Най-често срещани думи
    word_freq = Counter(all_words)
    common_words = word_freq.most_common(15)
    
    return {
        'sentences': analyzed_sentences,
        'sentence_stats': sentence_stats,
        'total_words': total_words,
        'total_characters': total_characters,
        'total_characters_no_spaces': total_characters_no_spaces,
        'unique_words': unique_words,
        'avg_word_length': avg_word_length,
        'reading_time': reading_time,
        'common_words': common_words,
        'all_words': all_words
    }

def display_sentence_analysis(sentences):
    """Показва детайлен анализ на всяко изречение"""
    if not sentences:
        return
    
    st.subheader(f"📑 Анализ на изреченията ({len(sentences)} общо)")
    
    for sentence_data in sentences:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f'<div class="sentence-box">', unsafe_allow_html=True)
                st.markdown(f'**Изречение {sentence_data["number"]}:**')
                st.write(sentence_data['text'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
                st.markdown(f'<span class="word-count-badge">{sentence_data["words"]} думи</span>', unsafe_allow_html=True)
                st.write(f"🔤 {sentence_data['characters']} символа")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")  # Добавяме малко разстояние

def main():
    # Заглавие
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
        <h1 class="main-header">🔤 Анализатор на Изречения</h1>
        <span class="real-time-badge">РЕАЛНО ВРЕМЕ</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Сайдбар за настройки
    with st.sidebar:
        st.header("⚙️ Настройки за анализ")
        
        show_detailed_sentences = st.checkbox("Покажи детайлен анализ на изреченията", value=True)
        show_sentence_stats = st.checkbox("Покажи статистики за изреченията", value=True)
        show_word_frequency = st.checkbox("Покажи честота на думи", value=True)
        
        st.markdown("---")
        st.header("ℹ️ Информация")
        st.write("""
        **Нови характеристики:**
        - 📑 Разделяне на текст на изречения
        - 🔍 Анализ на всяко изречение поотделно
        - 📊 Статистики за дължина на изречения
        - ⚡ Моментален анализ в реално време
        """)
    
    # Основна област
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Текстова област
        st.subheader("🎯 Въведи текст за анализ")
        
        # Примерен текст за демонстрация
        sample_text = """Това е първото изречение. То съдържа няколко думи!
        Второто изречение е малко по-дълго и показва как работи разделянето.
        Трето ли е това? Четвъртото изречение завършва с удивителен знак!"""
        
        text = st.text_area(
            "Пишете тук:",
            height=300,
            placeholder="Започнете да пишете... Текстът ще бъде автоматично разделен на изречения за анализ.",
            key="real_time_input",
            label_visibility="collapsed",
            value=sample_text
        )
        
        # Индикатор за активност
        if text:
            sentences = split_into_sentences(text)
            st.success(f"✅ Разпознати {len(sentences)} изречения в реално време!")
    
    with col2:
        st.subheader("📊 Обща статистика")
        
        # Анализ в реално време
        if text.strip():
            analysis = analyze_text_in_real_time(text)
            
            if analysis:
                # Основни метрики
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("📝 Общо думи", analysis['total_words'])
                    st.metric("📑 Изречения", analysis['sentence_stats']['count'])
                    st.metric("🔤 Уникални думи", analysis['unique_words'])
                
                with col2:
                    st.metric("📊 Символи", analysis['total_characters'])
                    st.metric("⏱️ Време за четене", f"{analysis['reading_time']:.1f} мин")
                    st.metric("📏 Ср. дължина на дума", f"{analysis['avg_word_length']:.1f}")
                
                # Статистики за изреченията
                if show_sentence_stats and analysis['sentence_stats']['count'] > 0:
                    with st.expander("📈 Статистики за изреченията", expanded=True):
                        st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                        
                        stats = analysis['sentence_stats']
                        st.write(f"**Средно думи на изречение:** {stats['avg_words_per_sentence']:.1f}")
                        st.write(f"**Средно символи на изречение:** {stats['avg_chars_per_sentence']:.1f}")
                        
                        if stats['count'] > 1:
                            st.write("---")
                            st.write("**Най-кратко изречение:**")
                            st.info(stats['shortest_sentence'])
                            
                            st.write("**Най-дълго изречение:**")
                            st.info(stats['longest_sentence'])
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Честота на думи
                if show_word_frequency and analysis['common_words']:
                    with st.expander("🔤 Често срещани думи"):
                        for word, count in analysis['common_words'][:10]:
                            percentage = (count / analysis['total_words']) * 100
                            st.write(f"`{word}`: {count} пъти ({percentage:.1f}%)")
        
        else:
            st.info("💡 Започнете да пишете в лявата колона...")
            st.write("""
            **Ще видите:**
            - Брой изречения
            - Анализ на всяко изречение
            - Статистики за дължина
            - Често срещани думи
            """)
    
    # Детайлен анализ на изреченията
    if text.strip() and show_detailed_sentences:
        st.markdown("---")
        analysis = analyze_text_in_real_time(text)
        if analysis and analysis['sentences']:
            display_sentence_analysis(analysis['sentences'])

if __name__ == "__main__":
    main()
