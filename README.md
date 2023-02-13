# Dokumentacja API

Liczba w nawasie (200) oznacza kod który api zwraca

***

## Użytkownik

`dorm_name` - Nazwa akademika<br>
`username` `name` - Nazwa użytkownika<br>
`message` `name` - Pisemna informacja odpowiedzi API<br>
`code` - Kod akademika, lub kod weryfikacyjny <br>
`token` - Json Web Token w którym zawarty jest ID użytkownika <br>
`email` - Adres email użytkownika<br>
`password` - hasło użytkownika<br>

---

### Rejestracja
Rejestracja jest realizowane metodą `POST` i dane są wysyłane w formacie `JSON`. 
Żeby dodać użytkownika trzeba wysłać 3 argumenty:<br>
```JSON
{
  "email": "stefan@gmail.com",
  "password": "S1lneH4sło!",
  "name": "stefcio"
}
```
>Argument name jest modyfikowany przez api by pierwsza litera była duża przykład:
> > stefcio -> Stefcio

Adres dodawania użytkownika to: [`http://localhost:3000/users`](http://localhost:3000/users)
<br>Przykładowe odpowiedzi API:<br>

Użytkownik dodany prawidłowo (201): 
```JSON
{
  "message": {
    "name": "Użytkownik utworzony!"
  }
}
``` 


Użytkownik już istnieje (400):
```JSON
{
    "message": {
        "name": "Użytkownik już istnieje!"
    }
}
```
Użytkownik nie potwierdził emaila (409):
```JSON
{
    "message": {
        "name": "Użytkownik nie potwierdził emaila!"
    }
}
```

### Weryfikacja emaila
Werykacja adresu email odbywa się metodą `PUT` i dane są wysyłane w formacie `JSON`. Żeby potwierdzić adres email użytkownika trzeba wysłać 2 argumenty:
```JSON
{
  "email": "stefan@gmail.com",
  "code": "111111"
}
```

Adres potwierdzania emaila to: [`http://localhost:3000/users`](http://localhost:3000/users)<br>
Przykładowe odpowiedzi API:

Prawidłowy kod i email (200):
```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjJ9.z3KDaNlqVgez4hQ64Gyi_tSoV1pzIWtOb09rbGMU9Nk"
}
```
Użytkownik nieistnieje w bazie niezweryfikowanych emaili (404):
```JSON
{
    "message": {
        "name": "Użytkownik nie istnieje"
    }
}
```
Podany kod weryfikacyjny jest błędny (400):
```JSON
{
    "message": {
        "name": "Podany kod weryfikacyjny jest błędny"
    }
}
```

### Dołączanie do akademika
Werykacja adresu email odbywa się metodą `PATCH` i dane są wysyłane w formacie `JSON`. Żeby potwierdzić adres email użytkownika trzeba wysłać 2 argumenty:
```JSON
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjF9.v1d8M_O74uyT_OJxTnUEbwzSZEVJR_vCMEuLKuiaPeo",
  "code": "1111111"
}
```

Adres dołączanie do akademika to: [`http://localhost:3000/users`](http://localhost:3000/users)<br>
Przykładowe odpowiedzi API<br>

Kod i token prawidłowy (200):
```JSON
{
    "dorm_name": "Akademik 1"
}
```
Token nieprawidłowy (401):
```JSON
{
    "message": {
        "name": "Token błędny"
    }
}
```
Kod akademika błędny (400):
```JSON
{
    "message": {
        "name": "Błędny kod akademika"
    }
}
```

### Logowanie użytkownika
Logowanie użytkownika jest realizowane metodą `get` i dane są wysyłane w formcie argumentów w linku. Żeby dodać użytkownika trzeba wysłać 2 argumenty:<br>
`email`<br>
`hasło`<br>
Adres logowania użytkownika to: [`http://localhost:3000/users`](http://localhost:3000/users)
<br>Przykład linku:
[`http://localhost:3000/users?email=stefan@gmail.com&password=S1lneH4asło!`](http://localhost:3000/users?email=stefan@gmail.com&password=S1lneH4asło!)
<br>Przykładowe odpowiedzi API:<br>

Dane użytkownika prawidłowe (200):
```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjF9.v1d8M_O74uyT_OJxTnUEbwzSZEVJR_vCMEuLKuiaPeo",
    "username": "Stefan",
    "dorm_name": "Akademik 1"
}
```

Email albo hasło nieprawidłowe (400):
```JSON
{
    "message": {
        "name": "Email albo hasło nieprawidłowe"
    }
}
```

***

## Maszyny/Kontakty

---

### Uzyskaj kontakty 
Uzyskiwanie kontaktów jest realizowane metodą `get` i dane są wysyłane w formacie argumentów w linku. Żeby uzyskać kontakty trzeba wysłać 1 argument `token`:<br>
Adres uzyskiwania kontaktów to: [`http://localhost:3000/machines`](http://localhost:3000/machines)<br>
Przykładowy adres: [`http://localhost:3000/machines?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0`](http://localhost:3000/machines?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjV9.1ll_3UI5Hi83OMcX-9S4NA0lMbRQtxlx99mgZTy1vC0)<br>
Przykładowe odpowiedzi API:

Prawidłowa odpowiedź (200):
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
    ]
}
```

Brak urządzeń w akademiku (200):
```JSON
{
    "machines": []
}
```

Użytkownik nie istnieje (401):
```JSON
{
  "message": {
    "name": "Użytkownik nie istnieje"
  }
}
```