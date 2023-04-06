# Dokumentacja API
***
# Check — Sprawdzanie maila i hasła
### URL
`GET /check?email=:email&password=:password`
### Parametry
| Nazwa parametru | Typ    | Opis                                        |
|-----------------|--------|---------------------------------------------|
| email           | String | Adres e-mail, którego dostępność sprawdzamy |
| password        | String | Hasło, które sprawdzamy                     |
### Odpowiedź
```JSON
{
  "message": {
    "name": "Nie znaleziono użytkownika"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                                       |
|----------------|------------------------------------------------------------|
| 404            | Sukces - Adres email jest dostępny i hasło jest prawidłowe |
| 200            | Błąd - Adres email NIE jest dostępny                       |
| 400            | Błąd - Adres email NIE jest w prawidłowym formacie         |
| 422            | Błąd - Hasło jest niepoprawne                              |
# Users — Rejestracja użytkownika
### URL
`POST /users`
### Parametry
| Nazwa parametru | Typ    | Opis                     |
|-----------------|--------|--------------------------|
| email           | String | Adres e-mail użytkownika |
| password        | String | Hasło użytkownika        |
| name            | String | Nazwa użytkownika        |
### Zapytanie
```JSON
{
  "email": "stefan@gmail.com",
  "password": "S1lneH4sło!",
  "name": "stefcio"
}
```
### Odpowiedź
```JSON
{
  "message": {
    "name": "Użytkownik utworzony!"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                            |
|----------------|-------------------------------------------------|
| 201            | Sukces - Użytkownik został dodany               |
| 400            | Błąd - Użytkownik już istnieje                  |
| 409            | Błąd - Użytkownik nie potwierdził adresu E-mail |
### Informacje
Ta funkcja powoduje wysłanie na podany adres E-mail kodu (6 cyfr) weryfikacyjnego
# Users - Weryfikacja adresu e-mail
### URL
`PUT /users`
### Parametry
| Nazwa parametru | Typ    | Opis                                           |
|-----------------|--------|------------------------------------------------|
| email           | String | Adres E-mail użytkownika                       |
| code            | String | Kod użytkownika który został wysłany na E-mail |
### Zapytanie
```JSON
{
  "email": "stefan@gmail.com",
  "code": "111111"
}
```
### Odpowiedź
```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjJ9.z3KDaNlqVgez4hQ64Gyi_tSoV1pzIWtOb09rbGMU9Nk"
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                        |
|----------------|---------------------------------------------|
| 200            | Sukces - Użytkownik zweryfikowany           |
| 404            | Błąd - Użytkownik NIE istnieje              |
| 400            | Błąd - Podany kod weryfikacyjny jest błędny |
# Users — Dodawanie użytkownika do akademika
### URL
`PATCH /users`
### Parametry
| Nazwa parametru | Typ    | Opis                |
|-----------------|--------|---------------------|
| token           | String | Token autoryzacyjny |
| code            | String | Kod akademika       |
### Zapytanie
```JSON
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjF9.v1d8M_O74uyT_OJxTnUEbwzSZEVJR_vCMEuLKuiaPeo",
  "code": "1111111"
}
```
### Odpowiedź
```JSON
{
    "dorm_name": "Akademik 1"
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                                                        |
|----------------|-----------------------------------------------------------------------------|
| 200            | Sukces - Kod akademika poprawny, użytkownik dodany do akademika `dorm-name` |
| 401            | Błąd - Podany token jest nieprawidłowy                                      |
| 400            | Bład - Podany kod jest nieprawidłowy                                        |

### Autoryzacja
Aby korzystać z tego endpointu, należy pozyskać `token` można go pozyskać z weryfikacji adresu e-mail albo logowania
# Users — Logowanie
### URL
`GET /users?email=:email&password=:password`
### Parametry
| Nazwa Parametru | Typ    | Opis                     |
|-----------------|--------|--------------------------|
| email           | String | Adres e-mail użytkownika |
| password        | String | Hasło użytkownika        |
### Odpowiedź
```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjF9.v1d8M_O74uyT_OJxTnUEbwzSZEVJR_vCMEuLKuiaPeo",
    "username": "Stefan",
    "dorm_name": "Akademik 1"
}
```
### Kod odpowiedzi
| Kod odpowiedzi | Opis                                             |
|----------------|--------------------------------------------------|
| 200            | Sukces - Dane autoryzacyjne poprawne             |
| 400            | Błąd - Adres e-mail albo hasło są NIE prawidłowe |
# Password-reset — Wysyłanie kodu weryfikacyjnego
### URL
`PATCH /password-reset/send-code`
### Parametry
| Nazwa parametru | Typ    | Opis                                                 |
|-----------------|--------|------------------------------------------------------|
| email           | String | Adres e-mail użytkownika który chce zresetować hasło |
### Zapytanie
```JSON
{
  "email": "stefan@gmail.com"
}
```
### Odpowiedź
```JSON
{
  "message": {
    "name": "Mail wysłany"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                                   |
|----------------|--------------------------------------------------------|
| 200            | Sukces - E-mail z kodem został wysłany                 |
| 404            | Błąd - Nie znaleziono użytkownika z tym adresem e-mail |
# Password-reset — Weryfikacja kodu resetu hasła
### URL
`GET /password-reset/?email=:email&code=:code`
### Parametry
| Nazwa parametru | Typ    | Opis                                     |
|-----------------|--------|------------------------------------------|
| code            | String | Kod weryfikacyjny do resetu hasła        |
| email           | String | Adres e-mail na który został wysłany kod |
### Odpowiedź
```JSON
{
  "message": {
    "name": "Kod jest prawidłowy"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                       |
|----------------|--------------------------------------------|
| 200            | Sukces - Kod prawidłowy                    |
| 404            | Błąd - Nie znaleziono użytkownika          |
| 400            | Błąd - Podany kod weryfikacyjny jest błędy |
# Password-reset — Ustawianie nowego hasła
### URL
`PATCH /password-reset`
### Parametry
| Nazwa parametru | Typ    | Opis                              |
|-----------------|--------|-----------------------------------|
| email           | String | Adres e-mail użytkownika          |
| new_password    | String | Nowe hasło które ma być ustawione |
### Zapytanie
```JSON
{
    "email": "stefan@gmail.com",
    "new_password": "NoweHasło"
}
```
### Odpowiedź
```JSON
{
  "message": {
    "name": "Hasło zostało zmienione"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                              |
|----------------|-----------------------------------|
| 200            | Sukces - Hasło zostało zmienione  |
| 404            | Błąd - Nie znaleziono użytkownika |
# Machines — Listowanie maszyn
### URL
`GET /machines?token=:token`
### Parametry
| Nazwa parametru | Typ    | Opis                |
|-----------------|--------|---------------------|
| token           | String | Token autoryzacyjny |
### Odpowiedź
```JSON
{
    "machines": [
        {
            "turn_on": false,
            "name": "Pralka 1",
            "type": "0"
        },
        {
            "turn_on": false,
            "name": "Suszarka 2",
            "type": "1"
        }
    ]
}
```
| Nazwa odpowiedzi | Opis                                    |
|------------------|-----------------------------------------|
| turn_on          | Czy włączone                            |
| name             | Nazwa urządzenia                        |
| type             | Typ urządzenia 0 - Pralka, 1 - Suszarka |
### Kod Odpowiedzi
| Kod Odpowiedzi | Opis                              |
|----------------|-----------------------------------|
| 200            | Sukces - Dane prawidłowe          |
| 401            | Błąd - Błędny token autoryzacyjny |
### Autoryzacja
Aby korzystać z tego endpointu, należy pozyskać `token` można go pozyskać z weryfikacji adresu e-mail albo logowania
# Raport — Uzyskiwanie listy raport
### URL
`GET /raport?token=:token?lang=:lang`
### Parametry
| Nazwa parametry | Typ    | Opis                      |
|-----------------|--------|---------------------------|
| token           | String | Token autoryzacyjny       |
| lang            | String | Język użytkownika [pl,en] |
### Odpowiedź
`Zawartość jsona z listą problemów dla akademika który jest przypisany do użytkownika`
### Kod Odpowiedzi:
| Kod odpowiedzi | Opis                                         |
|----------------|----------------------------------------------|
| 200            | Sukces - Przekazano JSON'a z listą problemów |
| 401            | Błąd - Token autoryzacyjny jest błędy        |
