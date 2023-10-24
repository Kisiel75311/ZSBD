# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Odczytaj plik variables.yaml
env_vars = YAML.load_file('enviroments/variables.yaml')

Vagrant.configure("2") do |config|
  config.vm.box = "eurolinux-vagrant/oracle-linux-8"
  config.ssh.insert_key = false

  # Konfiguracja dla węzła db-node
  config.vm.define "db-node" do |db|
    db.vm.hostname = env_vars['db-node']['network']['hostname']
    db.vm.network "forwarded_port", guest: env_vars['db-node']['network']['forwarded_port']['guest'], host: env_vars['db-node']['network']['forwarded_port']['host']
    db.vm.network "private_network", ip: env_vars['db-node']['network']['private_ip']
    db.vm.provision "shell", inline: "bash /vagrant/provisioning/db.sh 2>&1 | tee /vagrant/provisioning/db.log"
    # # Backup podczas zatrzymywania
    # config.trigger.before :halt do |trigger|
    #   trigger.name = "Creating backup of database..."
    #   trigger.run_remote = {inline: "bash /path_to_your_backup_script.sh"}
    # end
  end
  
end
