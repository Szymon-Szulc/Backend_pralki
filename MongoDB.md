# Pomoc do mongoDB
***
### Bazy danych `laundry`

* dorms
* machines
* bookings
* users
---
### Import
W repozytorium znajdują się przykładowe pliki `JSON` w folderze `MongoDB` do importu w MongoDB Compass, nazwy baz danych **MUSZĄ** się pokrywać z listą powyżej!

---

# Dane

***

### Akademik
W przykładowej kolekcji są dwa akademiki

| Nazwa      | Kod    | ID_Akademika |
|------------|--------|--------------|
| Akademik 1 | 111111 | 1            |
| Akademik 2 | 222222 | 2            |

---

### Kontakty
W przykładowej kolekcji są dwa kontakty, ale trzeba ją zedytować o własne ID kontaktów (`KID`) i klucze lokalne (`localKey`)!<br>
IP i Status są przypisywane automatycznie przez backend

| ID_Kontaktu            | ID_Akademika | Klucz_Lokalny    | Nazwa    |
|------------------------|--------------|------------------|----------|
| bf842f6b49fba9f5a0xm1f | 2            | f10126d401e6acdb | pralka 1 |
| bfa4dbe0186f514c6e6l4m | 2            | 1071206da06ba6ab | pralka 2 |

---

### Rezerwacje

Rezerwacje można całkowicie dodawać przez backend przez co import kolekcji `Rezerwacje` nie jest wymagany!<br>
Przykładowa kolekcja z rezerwacjami

| ID_Akademika | ID_Rezerwacji | ID_Kontaktu            | ID_Użytkownika | Data                          |
|--------------|---------------|------------------------|----------------|-------------------------------|
| 2            | 6             | bfa4dbe0186f514c6e6l4m | 2              | 2023-01-30T21:37:00.000+00:00 |
| 2            | 7             | bf842f6b49fba9f5a0xm1f | 2              | 2023-01-30T21:37:00.000+00:00 |

---

### Student

Studentów można całkowicie dodawać przez backend przez co import kolekcji `user` nie jest wymagany!<br>
Przykładowa kolekcja z studentami

| Nazwa   | ID_Użytkownika | ID_Akademika | Email             | Hasło             |
|---------|----------------|--------------|-------------------|-------------------|
| Stefan  | 1              | 1            | stefan@pranie.com | stefan123         |
| Andrzej | 2              | 2            | andrzej@duda.com  | KotJarkaNajlepszy |

