# T3 AI BDM - DoRA Finetuning

## Takım Adı: Renicames-291239
- 👤 Recep Bülbül
- 👤 Mehmet Arzu

**T3AI**, T3AI BDM modelinin Renicames tarafından geliştirilmiş 26,447 veriden oluşan bir veri setiyle eğitilerek hazırlanmış bir Yapay Zeka Danışmanlık Hizmeti (ChatBot) projesidir. Bu proje, kullanıcıların Türk hukuku, Türk eğitim sistemi, tarım ve sürdürülebilirlik konuları ile ilgili sorularına doğru ve hızlı yanıtlar sunmayı amaçlamaktadır.

## Projenin Amacı ve Motivasyonu

Projenin amacı, T3 AI BDM modelinin DoRA (Weight-Decomposed Low-Rank Adaptation) yöntemiyle optimize edilerek yapay zekâ modellerinin daha verimli ve etkili bir şekilde adapte olmasını sağlamaktır. Bu projede, sınırlı veri setleri ve kaynaklarla büyük dil modellerini hızla eğitmek ve spesifik görevler için uyarlamak hedeflenmiştir. Hackathon kapsamında bu yaklaşımın uygulamalı olarak test edilmesi, hem gerçek dünya problemlerine çözümler üretmek hem de AI modellerinin özelleştirilme sürecinde hız ve esneklik kazandırmayı amaçlamıştır.

Projenin motivasyonu, yapay zekâ uygulamalarının hızla büyüyen ihtiyaçlarına cevap verebilmek için daha az kaynakla daha verimli modeller yaratmak ve modelleri spesifik görevlere adapte etme sürecini hızlandırmaktır.


## Proje Arayüzü 
![image](https://github.com/recepbulbul/Veri_Bilimi_Dersi/blob/main/Ads%C4%B1z.png)


## Veri Seti Geliştirme Süreci

Veri setimizin geliştirilme süreci aşağıdaki adımları içermektedir:

1. **Araştırma**: Türk Anayasası, çeşitli hukuk siteleri ve diğer yasal belgeler kapsamlı bir şekilde incelenmiştir. Ayrıca, Türk eğitim sistemi için Milli Eğitim Bakanlığı'nın yayınladığı PDF dokümanlar ve tarım sektörü için Tarım ve Orman Bakanlığı'nın resmi sitesi baz alınmıştır.
2. **Veri Toplama**: Resmi kaynaklardan hukuki, eğitim ve tarıma ilişkin veriler titizlikle toplanmıştır. Sürdürülebilirlik verileri ise ilgili sitelerdeki metinlerin yapay zeka araçları kullanılarak doğru formata getirilmesiyle oluşturulmuştur.
3. **Veri Temizleme**: Toplanan veriler, tekrar eden bilgilerden arındırılarak yapılandırılmıştır.
4. **Veri Seti Oluşturma**: Temizlenmiş veriler, modelin eğitimi için kullanılmak üzere JSON formatında bir veri setine dönüştürülmüştür. Veri setinde toplam 26,447 soru-cevap çifti bulunmaktadır.

## Veri Seti
Veri Setine erişmek için [buraya tıklayabilirsiniz](https://huggingface.co/datasets/Renicames/turkish-law-chatbot).


## Kullanım

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Bu projeyi klonlayın:
   ```sh
   git clone https://github.com/Renicames/T3-AI-BDM
   ```

2. Gerekli bağımlılıkları yükleyin:
   ```sh
   cd T3-AI-BDM
   pip install -r requirements.txt
   ```

3. İnce Ayarlama Süreci Başlatma:
   ```sh
   python finetune.py
   ```

4. Chatbot'u başlatın/Sınama Görevi:
   ```sh
   cd LLMFace
   python app.py
   ```

## Lisans

Bu proje Apache 2.0 Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.

---


