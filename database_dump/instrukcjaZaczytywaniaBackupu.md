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