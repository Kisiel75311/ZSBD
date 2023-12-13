# ZSBD

Skrypty wypełniające baze znajdują się w katalogu 'scritps'.
Nazwy skryptów odpowiadają nazwom tabel w bazie danych.

W katalogu enviroments znajdują się pliki konfiguracyjne dla środowiska wirtualnego.

## Uruchomienia bazy
Polecenie
```bash
vagrant up
```
## Instrukcja zaczytywania backupu
Link do backupu:  https://file.io/N21AwxnJzWq8 \
Dodać plik backup.dmp do folderu database_dump
wykonać polecenia: 

polecenie do stworzenia backup:
```bash
expdp 'c##zsbd/zsbd@XE' DIRECTORY=dump_directory DUMPFILE=backup.dmp SCHEMAS=c##zsbd LOGFILE=export.log
```
polecenie do zaczytania backupu do kopi bazy danych:
```bash
impdp 'system/SysPassword1@XE' DIRECTORY=dump_directory DUMPFILE=backup.dmp REMAP_SCHEMA=c##zsbd:c##zsbd_copy LOGFILE=import.log
```

Wszystko oczywiście na maszynie vagrant 
