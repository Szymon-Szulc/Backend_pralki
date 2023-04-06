# Dorms — Dodawanie akademika
### URL
`POST /dorms`
### Parametry
| Nazwa parametru | Typ    | Opis                       |
|-----------------|--------|----------------------------|
| key             | String | Klucz API                  |
| dorm-name       | String | Nazwa dodawanego akademika |
| dorm-code       | String | Kod akademika              |
### Zapytanie
```JSON
{
    "key": "JGuihkjHyuhi./HHUI267e8yuHUYThiu/YUGHIGgvhfuyihhvFYUghi.YUih",
    "dorm-name": "Akademik 3",
    "dorm-code": "333333"
}
```
### Odpowiedź
```JSON
{
  "message":{
    "name": "Akademik dodane!"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                     |
|----------------|--------------------------|
| 201            | Sukces - Akademik dodany |
| 401            | Błąd - Błędny token      |
### Autoryzacja
Aby korzystać z tego endpointu, należy pozyskać `key` można go pozyskać z `GET /api`
# Api — Pozyskanie api key
### URL
`GET /api?email=:email&password=:password`
### Parametry
| Nazwa parametry | Typ    | Opis                  |
|-----------------|--------|-----------------------|
| email           | String | Adres email logowania |
| password        | String | Hasło logowania       |
### Odpowiedź
```JSON
{
  "message": {
    "name": "Mail wysłany"
  }
}
```
### Kod Odpowiedzi
| Kod odpowiedzi | Opis                                                                               |
|----------------|------------------------------------------------------------------------------------|
| 200            | Sukces - Mail wysłany, klucz api jest na mailu                                     |
| 401            | Błąd - Dane są NIE prawidłowe, próba zalogowania została wysłana do administratora |