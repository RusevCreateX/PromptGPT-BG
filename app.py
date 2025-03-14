import streamlit as st
import openai
import os

# Информационен текст преди текстовото поле
st.write("### 📝 Как да използвате този чатбот?")
st.write("""
Инструкции:  

При свалянето на Screenshot-ите от GA4, GSC и BWT се СВАЛЯТ на устройството, а не се копират и се именуват, както следва: 1,2,3,4,5 и т.н.  
Ако се добави информация за самото изображение, чатът структурира данните по-добре **/1.Default Channel Group GA4 main/**  

Когато чатът пропусне изображение, може да се напише команда:  
*"Пропуснати са ХХХХ скрийншоти. Допълни доклада, добавяйки и тях."*  

Промптът е тестван на всички модели ChatGPT и досега най-успешен се оказва **ChatGPT o1 (uses advanced reasoning)**.  
Промптът работи еднакво добре на: [ChatGPT SERPstat SEO Tool](https://chatgpt.com/g/g-DGSpNhxyW-serpstat-seo-tool)  

⚠ **ВАЖНО!** Всяко едно заключение се прави от **НАС**, не от чата. Това е причината в промпта да няма заключения от анализа.  
""")

    
# -- Може да промените този System Prompt според Вашите нужди --
SYSTEM_PROMPT = """
📌 Ти си SEO специалист с дългогодишен опит. Твоята задача е да изготвиш детайлен, професионален и аналитичен отчет за органичния трафик, базиран на предоставените скрийншоти от Google Analytics 4 (GA4), Google Search Console (GSC) и Bing Webmaster Tools (BWT).

📌 Твоят анализ трябва да бъде изцяло базиран на реални данни и добри SEO практики. Не трябва да изразяваш хипотези, препоръки или предложения – единствено задълбочен анализ на тенденциите, процентните промени и корелациите в представянето на сайта.

📌 SEO терминологията остава непреведена, а обяснителният текст се формулира професионално и прецизно. Например: "Branded search" вместо "Брандово търсене".

📌 ДОПЪЛНИТЕЛНИ УСЛОВИЯ, които трябва да следваш стриктно:
🔴 Изрично забранено е комбинирането на анализи от различни изображения в една обща секция. Всяко изображение трябва да бъде анализирано индивидуално, последователно и самостоятелно, спрямо номерацията, която е ясно посочена върху тях.

📌 Допълнителни изисквания:
✔ Page Experience Insights: Анализирай тенденциите и ефекта на Core Web Vitals върху потребителското изживяване.
✔ Bing Webmaster Tools Performance: Извърши детайлен анализ на CTR, Impressions и позиционирането на ключови думи.
✔ 404 Not Found: Всяка грешка 404 трябва да бъде удебелена и маркирана в червено.
✔ Липсващ анализ: Ако някъде липсва задълбочено разглеждане на данни, добави релевантен и пълен анализ.

🔹 1️⃣ Основни изисквания към анализа
Изготви пълен сравнителен анализ спрямо:
📌 Предходния месец
📌 Предходната година

✅ Посочи процентните промени (спадове и ръстове), като използваш цветово кодиране:
🟢 Зелено за положителни стойности
🔴 Червено за отрицателни стойности

✅ Определи пиковете и дъната в представянето на органичния трафик и уточни датите, в които настъпват значителни промени.

🔹 2️⃣ Форматиране на отчета
📌 Организирай анализа в Word документ със следната структура:
✔ Всяка секция започва с номер и заглавие (с два пункта по-голям шрифт от стандартния текст).
✔ Под всяко заглавие добави кореспондиращия скрийншот, ясно номериран и съответстващ само на една секция по следния начин:

✦ Скриншот 1: Google Analytics – Sessions & New Users
✦ Скриншот 2: Google Search Console – Top Queries
✦ Скриншот 3: Bing Webmaster Tools – CTR & Impressions

📌 Форматиране на данните:
✅ Процентните спадове – в червено.
✅ Процентните ръстове – в зелено.
✅ Положителни думи („увеличение“, „подобрение“, „успех“) – в зелено.
✅ Отрицателни думи („спад“, „загуба“, „грешка“) – в червено.
✅ Всички 404 Not Found грешки – удебелени и маркирани в червено.

🔹 3️⃣ Детайлен SEO анализ на органичния трафик
Анализирай всяко изображение поотделно, като включиш:
📌 New users, Active users, Sessions
📌 Engagement rate
📌 Bounce rate
📌 Key events & Conversion rate
📌 Landing pages
📌 Branded search vs. Non-branded search
📌 Top queries (GSC)
📌 Indexed pages
📌 Crawl requests и Googlebot activity
📌 404 Not Found

🔹 4️⃣ Разширен анализ на Page Experience Insights
✔ Core Web Vitals: LCP, FID и CLS.
✔ Тенденции в „Good URLs“ и анализ на „Poor URLs“ (Mobile/Desktop).

🔹 5️⃣ Разширен анализ на Bing Webmaster Tools Performance
✔ CTR, Impressions и позициониране на ключовите думи.
✔ Разлики между Google и Bing.
✔ SERP тенденции.

🔹 6️⃣ Оформление и финални детайли
✅ Всеки скрийншот трябва да бъде номериран и ясно свързан със съответното заглавие.
✅ Форматирай числата и процентите ясно.
✅ Без хипотези – само анализ, базиран на реални SEO данни!
✅ Всички 404 Not Found грешки – удебелени и маркирани в червено!

🚀 Очакван краен резултат:
Изключително детайлен, аналитичен и визуално структуриран SEO отчет, с индивидуален и последователен анализ на всяко изображение.

📌 Важно:
⏳ Изчакай всички скрийншоти да бъдат качени и не предприемай никакви действия, докато не получиш команда "СТАРТ".
"""

st.title("CustomGPT Quick Report")

# Съхраняваме цялата история на чата в сесията,
# за да може всеки потребител да води продължителен разговор
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Съхраняваме качените файлове в сесията (за да не се губят при рестарт на приложението)
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

def generate_response(prompt):
    """
    Извиква OpenAI ChatCompletion API с текущата история на разговора.
    prompt е най-новото съобщение от потребителя.
    """
    # Добавяме най-новото user съобщение към историята
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Взимаме отговора от OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=0.7
    )

    # Текстът от асистента
    reply = response.choices[0].message["content"]

    # Добавяме отговора в историята
    st.session_state.messages.append({"role": "assistant", "content": reply})

    return reply

# Блок за качване на файлове – приемаме множество файлове (screenshots, PDF и т.н.)
uploaded_files = st.file_uploader(
    label="Качи скрийншоти или други файлове:", 
    accept_multiple_files=True,
    type=None  # може да ограничите типа, напр. ["png", "jpg", "pdf"]
)

# Ако има качени нови файлове, добавяме ги към сесията
if uploaded_files:
    for file in uploaded_files:
        # Ако вече не сме го качили преди, го добавяме в списъка
        if file not in st.session_state["uploaded_files"]:
            st.session_state["uploaded_files"].append(file)

# Показваме списъка с качени файлове
if st.session_state["uploaded_files"]:
    st.write("### Качени файлове:")
    for idx, file in enumerate(st.session_state["uploaded_files"], start=1):
        st.write(f"**Файл {idx}:** {file.name}")
        # По избор: ако е изображение, можем да го визуализираме
        # Форматите, които Streamlit поддържа като изображение: png, jpg, jpeg, gif...
        if file.type.startswith("image"):
            st.image(file, caption=file.name)

st.write("---")

# Текстово поле, в което потребителят пише своето съобщение
user_input = st.text_input("Задай въпрос или напиши нещо:")

# Когато натиснат бутона "Изпрати" или Enter
if st.button("Изпрати") and user_input.strip():
    output = generate_response(user_input)
    st.write(f"**Чатбот**: {output}")

# Показваме цялата досегашна история, за да виждат потребителите контекста
st.write("---")
st.write("### История на разговора:")
for msg in st.session_state.messages:
    if msg["role"] == "system":
        st.write(f"**System Prompt**: {msg['content']}")
    elif msg["role"] == "user":
        st.write(f"**Вие**: {msg['content']}")
    else:
        st.write(f"**Чатбот**: {msg['content']}")
