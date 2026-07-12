# Nasza Kuchnia 🍲

Prosta aplikacja PWA z przepisami zgodnymi z dietą mamy karmiącej:
z nabiałem, bez cebuli/czosnku, bez ostrych przypraw, bez warzyw wzdymających
i owoców drażniących, oparta na chudym mięsie (indyk, cielęcina, królik, kurczak,
chuda wołowina) i rybach bez tuńczyka. **105 przepisów.**

Interfejs jest zaprojektowany pod osobę ~70 lat: duże przyciski, czytelne komunikaty,
prosty przepływ.

## Jak to działa

1. Użytkownik wybiera posiłek (pierwsze / drugie śniadanie, obiad, podwieczorek, kolacja).
2. Zaznacza produkty, które ma w domu (lista generuje się **automatycznie z przepisów**,
   więc każdy produkt zawsze prowadzi do co najmniej jednego przepisu — brak martwych kliknięć).
3. Dostaje 3 dopasowane przepisy, wybiera jeden. Przycisk „Pokaż inne propozycje" cykluje kolejne.
4. Przepis zawiera: **gramatury na 1 osobę, alergeny, kaloryczność** i kroki przygotowania.
5. „Wyślij przepis" otwiera systemowy panel udostępniania (Web Share API); gdy niedostępny —
   kopiuje treść do schowka.
6. „Zapisz przepis" odkłada go do zakładki **Moje przepisy**, pogrupowanej w kategoriach.

## Pliki

```
index.html              # cała aplikacja (HTML + CSS + JS + dane) — to hostujemy
manifest.webmanifest    # manifest PWA
sw.js                   # service worker (offline)
icon-192/512, maskable, apple-touch-icon.png
recipes_data.py         # ŹRÓDŁO przepisów (edytuj tutaj)
build.py                # generator: składa index.html z recipes_data.py
```

## Uruchomienie lokalnie

```bash
# w katalogu projektu
python3 -m http.server 8080
# otwórz http://localhost:8080
```
(Service worker i „Dodaj do ekranu głównego" działają po HTTPS — czyli na Netlify.)

## Wrzucenie na GitHub

```bash
git init
git add .
git commit -m "Nasza Kuchnia — PWA z przepisami"
git branch -M main
git remote add origin git@github.com:piomajko-apps/nasza-kuchnia.git
git push -u origin main
```

## Hosting na Netlify

**Opcja A — z GitHuba (zalecane):** w Netlify → *Add new site* → *Import from Git* →
wskaż repo. Build command: *(puste)*. Publish directory: `.` (katalog główny).

**Opcja B — przeciągnij i upuść:** wejdź na app.netlify.com, przeciągnij cały katalog
na pole „Deploy". Gotowe.

Netlify daje HTTPS automatycznie, więc PWA (offline + instalacja) działa od razu.
Na telefonie: otwórz stronę → menu przeglądarki → **Dodaj do ekranu głównego**.

## Dodawanie / zmiana przepisów

Najproościej edytować `recipes_data.py` i przebudować:

```bash
python3 build.py   # nadpisze index.html, manifest, sw.js
```

Format jednego przepisu:

```python
{"t":"Nazwa przepisu","m":["ob"],"c":"Mięso","al":["mleko"],"kcal":600,
 "ing":[("indyk","180 g"),("ryż","60 g")],
 "steps":["Krok 1.","Krok 2."]},
```

- `m` (posiłki): `s1` pierwsze śniadanie, `s2` drugie śniadanie, `ob` obiad, `pw` podwieczorek, `ko` kolacja
- `c` (kategoria dla „Moje przepisy"): np. Śniadania, Nabiał, Kanapki, Mięso, Ryby, Zupy, Owoce i desery, Kasze i dodatki
- `al` (alergeny): `gluten`, `mleko`, `jaja`, `ryby`, `orzechy`
- lista wyboru produktów tworzy się sama z pola `ing` (pomijane są przyprawy i tłuszcze bazowe)

## Gdzie trzymane są zapisane przepisy

W `localStorage` przeglądarki — **na urządzeniu, bez logowania i bez kont**. To celowe:
apka jest prosta, działa offline i nie wymaga żadnej konfiguracji ani Firebase.

Jeśli w przyszłości mama i babcia mają widzieć **tę samą** listę na dwóch telefonach,
wtedy warto dołożyć Firebase (Firestore + anonimowe logowanie) i zsynchronizować klucz
`mk_saved`. Kod zapisu jest odizolowany w obiekcie `store` w `index.html`, więc podmiana
warstwy zapisu na Firestore to jedno miejsce.

## Dieta — co jest, czego nie ma

**Jest:** indyk, cielęcina, królik, kurczak, chuda wołowina; łosoś, dorsz, pstrąg, sandacz,
mintaj, morszczuk; nabiał (mleko, jogurt, kefir, maślanka, twaróg, serek, ser łagodny, masło);
łagodne warzywa (marchew, cukinia, dynia, ziemniaki, bataty, ogórek, sałata, buraki, pietruszka,
szpinak); owoce (jabłko, gruszka, banan, borówki, brzoskwinia); kasze, ryż, pieczywo orkiszowe/żytnie.

**Nie ma:** tuńczyka; cebuli i czosnku; ostrych przypraw; warzyw wzdymających (kalafior, brokuł,
kapusta, fasola, groch); owoców drażniących (truskawki, maliny, kiwi, cytrusy, ananas).
