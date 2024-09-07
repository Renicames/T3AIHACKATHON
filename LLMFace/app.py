from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import requests
from datetime import datetime

WEATHER_API_KEY = "c78db10e6a80079fa036ddc053c87735"  # OpenWeatherMap API Anahtarı
CURRENCY_API_KEY = "977936fed3a9fd47cb0e7cd9"  # ExchangeRate API Anahtarı

app = Flask(__name__, template_folder='templates', static_folder='static')

# Model ve tokenizer'ı yükleyin
tokenizer = AutoTokenizer.from_pretrained("t3ai-org/pt-model")
model_name = "/home/ubuntu/results/merged/v4"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def get_response():
    user_input = request.json.get('message', '')  # request.json.get ile güvenli hale getirildi
    if not user_input:  # Eğer user_input boşsa
        return jsonify({'response': 'Lütfen bir mesaj girin.'})

    if "hava durumu" in user_input.lower():  # Küçük harfe çevirme ile duyarlılığı azalttık
        response = call_weather_api(user_input)
    elif "döviz kuru" in user_input:
        response = call_currency_api(user_input)
    elif "saat kaç" in user_input:
        response = call_world_time_api(user_input)
    else:
        response = ask_question_with_improved_answer(user_input, model, tokenizer)

    return jsonify({'response': response})

def ask_question_with_improved_answer(question, model, tokenizer, max_length=300):
    # Prepare the input text
    input_text = f"Question: {question}\nAnswer:"

    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)

    # Generate the response using the model
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            top_p=0.9,  # Nucleus sampling
            top_k=50,   # Top-k sampling
            temperature=0.7,  # Adding randomness
            repetition_penalty=1.2,  # Penalize repetition
            num_return_sequences=1,
            pad_token_id=tokenizer.pad_token_id
        )

    # Decode the generated text
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract the answer portion
    answer = answer.split("Answer:")[1].strip()

    # Post-process to remove redundant sentences
    sentences = answer.split('. ')
    seen = set()
    filtered_answer = '. '.join([sentence for sentence in sentences if not (sentence in seen or seen.add(sentence))])

    # Check if the last sentence is incomplete and remove it if necessary
    if not filtered_answer.endswith('.'):
        filtered_answer = filtered_answer.rsplit('.', 1)[0] + '.'

    # Return the improved answer
    return filtered_answer

def call_weather_api(user_input):
    city = extract_city_from_input(user_input)
    if city:  # Eğer şehir varsa API çağrısı yap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            weather_tr = translate_weather_description(weather)  # Hava durumu açıklamasını Türkçeye çevir
            return f"{city} için hava durumu: {weather_tr}, sıcaklık: {temp}°C."
        else:
            return f"{city} için hava durumu bilgisi alınamadı. (Hata: {response.status_code})"
    else:
        return "Şehir ismi çıkarılamadı. Lütfen geçerli bir şehir adı belirtin."

def extract_city_from_input(user_input):
    # Örneğin: "Ankara'da hava durumu nedir?" -> Ankara
    words = user_input.split()
    cities = [
    'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara', 'Antalya', 'Ardahan', 
    'Artvin', 'Aydın', 'Balıkesir', 'Bartın', 'Batman', 'Bayburt', 'Bilecik', 'Bingöl', 'Bitlis', 
    'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli', 'Diyarbakır', 'Düzce', 
    'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 
    'Hakkari', 'Hatay', 'Iğdır', 'Isparta', 'İstanbul', 'İzmir', 'Kahramanmaraş', 'Karabük', 'Karaman', 
    'Kars', 'Kastamonu', 'Kayseri', 'Kırıkkale', 'Kırklareli', 'Kırşehir', 'Kilis', 'Kocaeli', 'Konya', 
    'Kütahya', 'Malatya', 'Manisa', 'Mardin', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 
    'Osmaniye', 'Rize', 'Sakarya', 'Samsun', 'Şanlıurfa', 'Siirt', 'Sinop', 'Şırnak', 'Sivas', 'Tekirdağ', 
    'Tokat', 'Trabzon', 'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak'
]
 # Şehir listesi genişletilebilir
    for word in words:
        if word.capitalize() in cities:  # Şehir listesi içindeki şehirlerle eşleşiyor mu?
            return word.capitalize()
    return None  # Eğer şehir bulunamazsa None döndür

def translate_weather_description(weather):
    # İngilizce hava durumu açıklamalarının Türkçe karşılıkları
    translations = {
        "clear sky": "açık hava",
        "few clouds": "az bulutlu",
        "scattered clouds": "parçalı bulutlu",
        "broken clouds": "kırık bulutlar",
        "shower rain": "sağanak yağış",
        "rain": "yağmur",
        "thunderstorm": "gök gürültülü fırtına",
        "snow": "kar",
        "mist": "sis",
        "overcast clouds": "kapalı bulutlar",
        "light rain": "hafif yağmur"
    }
    # Eğer açıklama çeviri tablosunda yoksa varsayılan olarak İngilizce döner
    return translations.get(weather.lower(), weather)

def extract_currencies_from_input(user_input):
    # Örneğin: "100 USD to TRY döviz kuru nedir?" -> USD, TRY, 100
    words = user_input.split()
    amount = 1  # Varsayılan olarak 1 birim alınır
    for word in words:
        if word.isdigit():
            amount = int(word)
    
    if "USD" in user_input and "TRY" in user_input:
        return "USD", "TRY", amount
    return "USD", "EUR", amount  # Varsayılan para birimleri

def call_currency_api(user_input):
    from_currency, to_currency, amount = extract_currencies_from_input(user_input)  # Dövizleri ve miktarı çıkar
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['conversion_rates'].get(to_currency)
        if rate:
            converted_amount = amount * rate  # Miktar üzerinden dönüşüm yapılır
            return f"{amount} {from_currency}, {converted_amount:.2f} {to_currency} değerindedir."
        else:
            return f"{to_currency} için döviz kuru bilgisi alınamadı."
    else:
        return f"{from_currency} için döviz kuru bilgisi alınamadı."
    
def extract_country_from_input(user_input):
    # Örneğin: "İngiltere'de saat kaç?" -> İngiltere
    words = user_input.split()
    countries = {
        'ingiltere': ('Europe/London', 'İngiltere'),
        'almanya': ('Europe/Berlin', 'Almanya'),
        'türkiye': ('Europe/Istanbul', 'Türkiye'),
        'japonya': ('Asia/Tokyo', 'Japonca'),
        'abd': ('America/New_York', 'Amerika'),
        'fransa': ('Europe/Paris', 'Fransa'),
        'rusya': ('Europe/Moscow', 'Rusya'),
        # Diğer ülke ve şehirleri buraya ekleyebilirsiniz
    }

    for word in words:
        lower_word = word.lower().replace('\'', '')
        if lower_word in countries:
            return countries[lower_word]  # Zaman dilimi ve şehir adını birlikte döndür
    return None, None  # Eğer ülke bulunamazsa None döndür

def call_world_time_api(user_input):
    timezone, city_name = extract_country_from_input(user_input)
    if timezone:  # Eğer zaman dilimi varsa API çağrısı yap
        url = f"http://worldtimeapi.org/api/timezone/{timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            datetime_str = data['datetime']  # Zaman bilgisini al
            time = datetime_str.split('T')[1].split('.')[0]  # Saat kısmını ayıkla (HH:MM:SS formatında)
            return f"{city_name}'de şu an saat: {time}"
        else:
            return f"{city_name} için saat bilgisi alınamadı. (Hata: {response.status_code})"
    else:
        return "Ülke veya şehir ismi çıkarılamadı. Lütfen geçerli bir yer adı belirtin."

@app.route('/save-feedback', methods=['POST'])
def save_feedback():
    data = request.json
    user_message = data.get('user_message')
    bot_message = data.get('bot_message')

    feedback_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_message': user_message,
        'bot_message': bot_message
    }

    try:
        with open('feedback.json', 'a') as f:
            json.dump(feedback_data, f)
            f.write('\n')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
