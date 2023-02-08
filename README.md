# Dokumentacja API

***

## Użytkownik

`name` - Nazwa użytkownika lub nazwa akademika<br>
`code` - Kod akademika, lub odpowiedź API w postaci kodu <br>
`jwt` - Json Web Token w którym zawarty jest ID użytkownika <br>

---

### Dodawanie użytkownika
Dodawanie użytkownika jest realizowane metodą `post` i dane są wysyłane w formacie `JSON`. Żeby dodać użytkownika trzeba wysłać 2 argumenty:<br>
```JSON
{
  "name": "Stefan",
  "code": "222222"
}
```
Adres dodawania użytkownika to: [`http://localhost:3000/user/add`](http://localhost:3000/user/add)
<br>Przykładowe odpowiedzi API:<br>

Użytkownik dodany prawidłowo:
```JSON
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0",
    "name": "Akademik 2",
    "code": 201
}
```

Użytkownik już istnieje:
```JSON
{
    "code": 406
}
```

Kod akademika jest błędny:
```JSON
{
    "code": 418
}
```

### Logowanie użytkownika
Logowanie użytkownika jest realizowane metodą `get` i dane są wysyłane w formcie argumentów w linku. Żeby dodać użytkownika trzeba wysłać 2 argumenty:<br>
`email`<br>
`hasło`<br>
Adres logowania użytkownika to: [`http://localhost:3000/user/get`](http://localhost:3000/user/get) lub [`http://localhost:3000/user/login`](http://localhost:3000/user/login)
<br>Przykład linku:
[`http://localhost:3000/user/get?email=stefan@pranie.com&password=stefan123`](http://localhost:3000/user/get?email=stefan@pranie.com&password=stefan123)
<br>Przykładowe odpowiedzi API:<br>

Dane użytkownika prawidłowe:
```JSON
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0",
    "dorm-name": "Akademik 2",
    "username": "Stefan",
    "code": 201
}
```

Email albo hasło nieprawidłowe:
```JSON
{
    "code": 406
}
```
***
## Rezerwacje
`jwt` - Json Web Token w którym jest zawarty ID użytkownika, pozyskany w sekcji Uzytkownik<br>
`date` - Data rezerwacji w formacie RRRR-MM-DD (R - rok, M - miesiąc, D - dzień)<br>
`time` - Godzina rezerwacji GG-MM (G - godziny, M - minuty)<br>
`name` - Nazwa rezerwowanego urządzenia<br>
`code` - Odpowiedź API w postaci kodu<br>
`bookings` - Tablica z rezerwacjami<br>
`bid` - ID rezerwacji<br>
---

### Dodawanie rezerwacji
Dodawanie użytkownika jest realizowane metodą `post` i dane są wysyłane w formacie `JSON`. Żeby dodać rezerwację trzeba wysłać 4 argumenty:<br>
```JSON
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0",
    "date": "2023-02-20",
    "time": "21:37",
    "name": "pralka 2"
}
```
Adres dodawania rezerwacji to: [`http://localhost:3000/booking/add`](http://localhost:3000/booking/add)
<br>Przykładowe odpowiedzi API:<br>

Rezerwacja dodana prawidłowo:
```JSON
{
  "code": 201
}
```

Użytkownik nie istnieje
```JSON
{
  "code": 401
}
```


Urządzenie nie istnieje:
```JSON
{
  "code": 406
}
```

Rezerwacja na dane urządzenie w danym akademiku o danej godzinie i dacie już istnieje:
```JSON
{
  "code": 418
}
```

### Uzyskiwanie rezerwacji akademika
Uzyskiwanie rezerwacji jest realizowane metodą `get` i dane są wysyłane w formacie `JSON`. Żeby uzyskać rezerwacje trzeba wysłać 1 argument:<br>
```JSON
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0"
}
```
Adres uzyskiwania rezerwacji to: [`http://localhost:3000/booking/get`](http://localhost:3000/booking/get)
<br>Przykładowe odpowiedzi API:<br>

Prawidłowa odpowiedź:
```JSON
{
    "bookings": [
        {
            "bid": 1,
            "date": "2023-02-20 21:37:00"
        }
    ],
    "code": 201
}
```

Brak rezerwacji w akademiku:
```JSON
{
    "bookings": [],
    "code": 201
}
```

Użytkownik nie istnieje:
```JSON
{
  "code": 401
}
```
***
## Maszyny/Kontakty

---

### Uzyskaj kontakty 
Uzyskiwanie kontaktów jest realizowane metodą `get` i dane są wysyłane w formacie `JSON`. Żeby uzyskać kontakty trzeba wysłać 1 argumnt:
```JSON
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0"
}
```
Adres uzyskiwania kontaktów to: [`http://localhost:3000/machine/get`](http://localhost:3000/machine/get)<br>
Przykładowe odpowiedzi API:

Prawidłowa odpowiedź:
```JSON
{
    "machines": [
        {
            "turn_on": false,
            "name": "pralka 1"
        },
        {
            "turn_on": true,
            "name": "pralka 2"
        }
    ],
    "code": 201
}
```

Brak urządzeń w akademiku:
```JSON
{
    "machines": [],
    "code": 201
}
```

Użytkownik nie istnieje:
```JSON
{
  "code": 401
}
```