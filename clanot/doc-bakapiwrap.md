# BakApiWrap Dokumentace

## Příprava:
### import
Pokud modul jmenuje `bakapiwrap` použijte tehle kod:

```python
import bakapiwrap as baka
```

*Pokud se modul nejmenuje `bakapiwrap`  nahraďte ho validním jménem*

### Login(Url,Username,Password)
Url: `Adresa bakalářů bez / na konci`
Username: `Uživatelské jméno jako string`
Password: `Heslo v typu string`

Výstup: `Dictonary s tokenem a refresh tokenem`

##### Příklad:
```python
import bakapiwrap as baka
out = baka.Login("sbakalary.example.cz","jméno","12345678")
print(out)
```
###### výstup:
```python
{'token': "nějaký token", 'refresh': "Refresh token"}
```
