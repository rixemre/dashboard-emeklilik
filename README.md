TSB 1Ç26 Dashboard – Flask Giriş Ekranı
Yüklediğiniz dashboard'u (`templates/dashboard.html`) session tabanlı, basit bir
giriş ekranının arkasına alan bir Flask uygulaması.
Klasör yapısı
```
tsb-dashboard-flask/
├── app.py                  # Flask uygulaması ve route'lar
├── requirements.txt
├── templates/
│   ├── login.html          # Dashboard ile aynı tasarım diline sahip giriş ekranı
│   └── dashboard.html      # Yüklediğiniz dashboard + üstte kullanıcı/çıkış rozeti
```
Kurulum ve çalıştırma
```bash
pip install -r requirements.txt
python app.py
```
Sonra tarayıcıda http://127.0.0.1:5000 adresini açın. Giriş yapmadan
`/dashboard`'a gitmeye çalışırsanız otomatik olarak `/login`'e yönlendirilirsiniz.
Varsayılan giriş bilgileri
```
kullanıcı adı: admin
şifre:         changeme123
```
Bunu mutlaka değiştirin — aşağıya bakın.
Kullanıcı adı / şifreyi değiştirme
En hızlı yol, ortam değişkeni ile şifreyi geçmek:
```bash
export ADMIN_PASSWORD="cok-guclu-bir-sifre"
python app.py
```
Birden fazla kullanıcı eklemek isterseniz `app.py` içindeki `USERS` sözlüğüne
yeni girişler ekleyin (şifreler her zaman `generate_password_hash` ile
saklanır, düz metin olarak asla):
```python
USERS = {
    "admin": generate_password_hash("cok-guclu-bir-sifre"),
    "analist": generate_password_hash("baska-bir-sifre"),
}
```
Gerçek bir projede bu sözlük yerine bir veritabanı tablosu (ör. SQLAlchemy ile
bir `users` tablosu) kullanmanızı öneririz — kullanıcı sayısı arttıkça veya
şifre sıfırlama gibi ihtiyaçlar doğduğunda bu şart olur.
Prod'a almadan önce
`SECRET_KEY`'i ortam değişkeninden okuyun ve rastgele/uzun bir değer verin:
`export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"`
`app.run(debug=True)` satırındaki `debug=True`'yu kaldırın; gerçek dağıtımda
gunicorn/uwsgi gibi bir WSGI sunucusu kullanın.
Siteyi HTTPS arkasında sunun (aksi halde şifreler ve session çerezi açık
metin olarak ağda dolaşır).
İstersen `session.permanent` süresini (`PERMANENT_SESSION_LIFETIME`,
şu an 14 gün) ihtiyacına göre kısalt/uzat.
Tasarım notları
`login.html`, dashboard'daki `:root` renk/gölge/radius değişkenlerini,
Inter fontunu, koyu "hero" gradyanını ve rozet (badge) bileşenlerini yeniden
kullanır; böylece iki ekran aynı ürünün parçası gibi görünür. Dashboard
şablonuna eklenen tek şey, sağ üstte sabit duran kullanıcı adı rozeti ve
"Çıkış Yap" bağlantısıdır — mevcut dashboard kodunuza dokunulmadı.
