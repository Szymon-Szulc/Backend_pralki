# Dokumentacja API
***
## USERS
***
### Rejestracja
***
#### Rejestracja
Endpoint:
>POST /api/v1/users/register

Argumenty:
>email - adres email <br>
>password - hasło

Kody HTTP:
> 400 - niepoprawny format email<br>
> 422 - niepoprawny format hasła<br>
> 403 - Użytkownik już istnieje<br>
> 403 - Użytkownik istnieje, ale nie potwierdził emaila<br>
> 201 - Użytkownik zarejestrowany pomyślnie
<hr>

#### Potwierdzenie adresu E-mail
Endpoint:
>PUT /api/v1/users/register/verify

Argumenty:
> email - adres email <br>
> code - kod weryfikacyjny <br>
> name - nazwa użytkownika

Kody HTTP:
> 400 - podany kod weryfikacyjny jest błędny<br>
> 200 - konto zweryfikowane pomyślnie

Pakiet:
> (200) token - token autoryzacyjny JWT
```JSON
{
  "token": "example-token"
}
```
<hr>

#### Dołączanie użytkownika do akademika
Endpoint:
> PATCH /api/v1/users/register/join

Argumenty:
> token - token autoryzacyjny JWT<br>
> code - kod akademika

Kody HTTP:
> 401 - podany kod autoryzacyjny JWT jest błędny<br>
> 404 - akademik o podanym kodzie nie istnieje<br>
> 200 - użytkownik został dodany do akademika

Pakiet:
> (200) dorm_name - nazwa akademika
```JSON
{
  "dorm_name": "Przykładowy Akademik"
}
```
***
### Logowanie
***
#### Logowanie
Endpoint:
> GET /api/v1/users/login

Argumenty:
> email - adres email<br>
> password - hasło

Kody HTTP:
> 400 - podany kod autoryzacyjny JWT jest błędny<br>
> 404 - akademik o podanym kodzie nie istnieje<br>
> 200 - użytkownik został dodany do akademika

Pakiet:
> (200) dorm_name - nazwa akademika
```JSON
{
  "dorm_name": "Przykładowy Akademik"
}
``` 
***
### Reset Hasła
***
### Wysyłanie maila
Endpoint:
> PATCH /api/v1/users/reset-password/send

Argumenty:
> email - adres e-mail

Kody HTTP:
> 400 - niepoprawny adres e-mail<br>
> 404 - nieznaleziono użytkownika o podanym adresie e-mail<br>
> 200 - mail został wysłany do użytkownika, użytkownik został oznaczony w bazie danych flagą resetu hasła
<hr>

### Weryfikacja kodu
Endpoint:
> GET - /api/v1/users/reset-password/verify

Argumenty:
> email - adres e-mail
> code - kod weryfikacyjny

Kody HTTP:
> 400 - niepoprawny e-mail<br>
> 401 - podany kod jest błędny<br>
> 404 - nieznaleziono użytkownika o podanym adresie e-mail z flagą resetu hasła<br>
> 200 - podany kod jest prawidłowy
<hr>

### Ustawienie nowego hasła
Endpoint:
> PATCH /api/v1/users/reset-password

Argumenty:
> email - adres e-mail
> code - kod weryfikacyjny
> password - hasło które ma być ustawione

Kody HTTP:
> 400 - niepoprawny e-mail<br>
> 401 - podany kod jest błędny<br>
> 404 - nieznaleziono użytkownika o podanym adresie e-mail z flagą resetu hasła<br>
> 422 - niepoprawne hasła<br>
> 201 - hasło zostało zmienione