import streamlit as st
import re
from collections import Counter

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
    .sentence-length-indicator {
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        margin-left: 0.5rem;
    }
    .short-sentence { background-color: #d4edda; color: #155724; }
    .medium-sentence { background-color: #fff3cd; color: #856404; }
    .long-sentence { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

def split_into_sentences(text):
    """Разделя текста на изречения с подобрен алгоритъм"""
    if not text.strip():
        return []
    
    # Подобрен патърн за разделяне на изречения
    # Разделя по . ! ? … и след това интервал или нов ред
    sentence_endings = r'(?<=[.!?\…])\s+'
    
    # Разделяне на изречения
    sentences = re.split(sentence_endings, text)
    
    # Филтриране на празни изречения и премахване на водещи/завършващи интервали
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # Обединяване на съкращения, които не са краища на изречения
    cleaned_sentences = []
    i = 0
    while i < len(sentences):
        current_sentence = sentences[i]
        
        # Проверка дали изречението завършва със съкращение (но не е края на изречение)
        if (i < len(sentences) - 1 and 
            re.search(r'\b(г|с|т|др|проф|доц|инж|бл|ал|ул|бул|пл)\.$', current_sentence, re.IGNORECASE)):
            current_sentence += " " + sentences[i + 1]
            i += 2
        else:
            i += 1
        
        cleaned_sentences.append(current_sentence)
    
    return cleaned_sentences

def get_sentence_length_category(word_count):
    """Определя категорията на дължина на изречението"""
    if word_count <= 8:
        return "short", "Късо"
    elif word_count <= 15:
        return "medium", "Средно"
    else:
        return "long", "Дълго"

def analyze_sentence(sentence, sentence_num):
    """Анализира отделно изречение"""
    # Намиране на думите (само букви и цифри)
    words = re.findall(r'\b[а-яА-Яa-zA-Z0-9]+\b', sentence)
    
    characters = len(sentence)
    characters_no_spaces = len(sentence.replace(" ", ""))
    
    # Определяне на категорията на дължина
    length_category, length_label = get_sentence_length_category(len(words))
    
    return {
        'number': sentence_num,
        'text': sentence,
        'words': len(words),
        'characters': characters,
        'characters_no_spaces': characters_no_spaces,
        'word_list': words,
        'length_category': length_category,
        'length_label': length_label
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
    if analyzed_sentences:
        words_per_sentence = [sent['words'] for sent in analyzed_sentences]
        chars_per_sentence = [sent['characters'] for sent in analyzed_sentences]
        
        sentence_stats = {
            'count': len(sentences),
            'avg_words_per_sentence': sum(words_per_sentence) / len(words_per_sentence),
            'avg_chars_per_sentence': sum(chars_per_sentence) / len(chars_per_sentence),
            'min_words': min(words_per_sentence),
            'max_words': max(words_per_sentence),
            'min_chars': min(chars_per_sentence),
            'max_chars': max(chars_per_sentence),
            'short_sentences': len([s for s in analyzed_sentences if s['length_category'] == 'short']),
            'medium_sentences': len([s for s in analyzed_sentences if s['length_category'] == 'medium']),
            'long_sentences': len([s for s in analyzed_sentences if s['length_category'] == 'long'])
        }
    else:
        sentence_stats = {
            'count': 0,
            'avg_words_per_sentence': 0,
            'avg_chars_per_sentence': 0,
            'min_words': 0,
            'max_words': 0,
            'min_chars': 0,
            'max_chars': 0,
            'short_sentences': 0,
            'medium_sentences': 0,
            'long_sentences': 0
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
    
    st.subheader(f"📑 Детайлен анализ на изреченията ({len(sentences)} общо)")
    
    for sentence_data in sentences:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f'<div class="sentence-box">', unsafe_allow_html=True)
                
                # Заглавие с номер и категория на дължина
                col_title1, col_title2 = st.columns([3, 1])
                with col_title1:
                    st.markdown(f'**Изречение {sentence_data["number"]}:**')
                with col_title2:
                    st.markdown(
                        f'<span class="sentence-length-indicator {sentence_data["length_category"]}-sentence">'
                        f'{sentence_data["length_label"]} ({sentence_data["words"]} думи)'
                        f'</span>', 
                        unsafe_allow_html=True
                    )
                
                # Текст на изречението
                st.write(sentence_data['text'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
                st.markdown(f'<span class="word-count-badge">{sentence_data["words"]} думи</span>', unsafe_allow_html=True)
                st.write(f"🔤 {sentence_data['characters']} символа")
                st.write(f"📏 {sentence_data['characters_no_spaces']} без интервали")
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
        show_length_distribution = st.checkbox("Покажи разпределение на дължините", value=True)
        
        st.markdown("---")
        st.header("📏 Категории на дължина")
        st.write("""
        - **Късо:** до 8 думи
        - **Средно:** 9-15 думи  
        - **Дълго:** над 15 думи
        """)
        
        st.markdown("---")
        st.header("ℹ️ Информация")
        st.write("""
        **Характеристики:**
        - 📑 Автоматично разделяне на изречения
        - 🔍 Индивидуален анализ
        - 📊 Статистики за дължина
        - ⚡ Моментален анализ
        - 🎯 Без външни зависимости
        """)
    
    # Основна област
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Текстова област
        st.subheader("🎯 Въведи текст за анализ")
        
        # Примерен текст за демонстрация
        sample_text = """Това е първото изречение. То съдържа няколко думи!
Второто изречение е малко по-дълго и показва как работи разделянето.
Трето ли е това? Четвъртото изречение завършва с удивителен знак!
Това е много дълго изречение, което съдържа много думи и ще бъде категоризирано като дълго изречение за анализ."""

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
                        st.write(f"**Най-кратко изречение:** {stats['min_words']} думи")
                        st.write(f"**Най-дълго изречение:** {stats['max_words']} думи")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Разпределение на дължините
                if show_length_distribution and analysis['sentence_stats']['count'] > 0:
                    with st.expander("📊 Разпределение на дължините"):
                        stats = analysis['sentence_stats']
                        total = stats['count']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Къси", stats['short_sentences'], 
                                     f"{stats['short_sentences']/total*100:.1f}%")
                        with col2:
                            st.metric("Средни", stats['medium_sentences'],
                                     f"{stats['medium_sentences']/total*100:.1f}%")
                        with col3:
                            st.metric("Дълги", stats['long_sentences'],
                                     f"{stats['long_sentences']/total*100:.1f}%")
                
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
