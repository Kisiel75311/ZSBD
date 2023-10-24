#!/bin/bash

echo "Start db-node configuration"

# Ustaw repozytorium Oracle i zainstaluj wymagane pakiety
sudo yum install -y oracle-database-preinstall-18c

# Upewnij się, że narzędzie 'wget' jest zainstalowane
sudo yum install -y wget

# Pobierz instalator Oracle XE
wget https://download.oracle.com/otn-pub/otn_software/db-express/oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm -O oracle-xe.rpm

# Zainstaluj Oracle XE używając rpm
sudo rpm -Uvh oracle-xe.rpm

# Usuń pobrany plik RPM
rm -f oracle-xe.rpm

echo "Installation of Oracle XE completed."
