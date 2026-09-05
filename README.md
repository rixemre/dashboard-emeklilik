# TSB 1Ç26 Dashboard – Flask Giriş Ekranı

Yüklediğiniz dashboard'u (`templates/dashboard.html`) session tabanlı, basit bir
giriş ekranının arkasına alan bir Flask uygulaması.

## Klasör yapısı

```
tsb-dashboard-flask/
├── app.py                  # Flask uygulaması ve route'lar
├── requirements.txt
├── templates/
│   ├── login.html          # Dashboard ile aynı tasarım diline sahip giriş ekranı
│   └── dashboard.html      # Yüklediğiniz dashboard + üstte kullanıcı/çıkış rozeti
```

## Kurulum ve çalıştırma

```bash
pip install -r requirements.txt
python app.py
```

Sonra tarayıcıda **http://127.0.0.1:5000** adresini açın. Giriş yapmadan
`/dashboard`'a gitmeye çalışırsanız otomatik olarak `/login`'e yönlendirilirsiniz.

## Varsayılan giriş bilgileri

```
kullanıcı adı: admin
şifre:         changeme123
```

Bunu mutlaka değiştirin — aşağıya bakın.

## Kullanıcı adı / şifreyi değiştirme

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

## Neden GitHub Pages ile çalışmıyor?

GitHub Pages **sadece statik dosya** sunar (HTML/CSS/JS). `app.py` sunucu
tarafında çalışan bir Python programı; Pages bunu hiç çalıştırmaz, sadece
klasördeki dosyaları olduğu gibi tarayıcıya gönderir. Bu yüzden giriş/şifre
kontrolü olan bu proje Pages'te **çalışamaz** — session, `USERS` sözlüğü,
`check_password_hash` gibi hiçbir şey devreye girmez.

Gerçek bir giriş ekranı istiyorsanız Python çalıştırabilen bir servise
deploy etmeniz gerekir. Aşağıda ücretsiz ve kolay olan **Render**'ı
anlatıyoruz; Railway ve PythonAnywhere de benzer şekilde çalışır.

## Render'a deploy etme (önerilen, ücretsiz)

1. Bu repoyu GitHub'da tutun (zaten `dashboard-emeklilik` içinde).
   `rixemre-patch-1` dalını `main`'e merge edin ya da Render'da doğrudan o
   dalı seçin.
2. [render.com](https://render.com) → GitHub hesabınızla giriş yapın →
   **New +** → **Web Service** → bu repoyu seçin.
3. Ayarlar:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
4. **Environment** sekmesinden şu değişkenleri ekleyin:
   - `SECRET_KEY` → rastgele uzun bir metin
     (`python -c "import secrets; print(secrets.token_hex(32))"` ile üretebilirsiniz)
   - `ADMIN_PASSWORD` → gerçekte kullanacağınız admin şifresi
5. **Create Web Service**'e tıklayın. Birkaç dakika içinde
   `https://dashboard-emeklilik.onrender.com` gibi bir adres verir; artık
   giriş ekranı gerçekten orada çalışır.
6. GitHub Pages ayarınızı (Settings → Pages) kapatabilir ya da
   dokunmadan bırakabilirsiniz — artık kullanmayacağınız için bir zararı
   olmaz, sadece kafa karıştırmasın diye "Build and deployment: None"
   yapmanızı öneririz.

> Not: Render'ın ücretsiz katmanı 15 dakika hareketsiz kalınca uykuya
> geçer; bir sonraki istek geldiğinde ~30-50 saniye "uyanma" süresi olur.
> Bu normaldir, hata değildir.

### Alternatifler
- **Railway.app** — Render ile hemen hemen aynı akış, GitHub'dan otomatik deploy.
- **PythonAnywhere** — ücretsiz katmanda Flask'ı manuel WSGI ayarıyla barındırır, biraz daha fazla elle kurulum ister.

## Prod'a almadan önce

- `SECRET_KEY`'i ortam değişkeninden okuyun ve rastgele/uzun bir değer verin
  (yukarıdaki Render adımında zaten böyle yapıldı).
- Gerçek deploy'da `gunicorn` devreye girer (bkz. `Procfile`); `app.py`
  içindeki `debug=True` yalnızca yerel geliştirme içindir, Render/Railway
  gibi servisler bu satırı hiç çalıştırmaz.
- Site otomatik olarak HTTPS arkasında olacaktır (Render/Railway varsayılan
  olarak sağlar) — bu önemli, aksi halde şifreler ağda açık metin dolaşır.
- İstersen `session.permanent` süresini (`PERMANENT_SESSION_LIFETIME`,
  şu an 14 gün) ihtiyacına göre kısalt/uzat.

## Tasarım notları

`login.html`, dashboard'daki `:root` renk/gölge/radius değişkenlerini,
Inter fontunu, koyu "hero" gradyanını ve rozet (badge) bileşenlerini yeniden
kullanır; böylece iki ekran aynı ürünün parçası gibi görünür. Dashboard
şablonuna eklenen tek şey, sağ üstte sabit duran kullanıcı adı rozeti ve
"Çıkış Yap" bağlantısıdır — mevcut dashboard kodunuza dokunulmadı.
