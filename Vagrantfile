# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Odczytaj plik variables.yaml
env_vars = YAML.load_file('enviroments/variables.yaml')

Vagrant.configure("2") do |config|
  config.vm.box = env_vars['general']['box']

  # Forwarded ports
  env_vars['forwarded_ports'].each do |port|
    config.vm.network "forwarded_port", guest: port['guest'], host: port['host']
  end

  config.vm.network "private_network", ip: env_vars['general']['public_ip']

  config.vm.provider "virtualbox" do |vb|
    vb.memory = env_vars['general']['mem_size']
    vb.cpus   = env_vars['general']['cpus']
    vb.name   = env_vars['general']['vm_name']

    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', '0', '--nonrotational', env_vars['general']['non_rotational']]
  end

  config.vm.provision "shell", inline: <<-SHELL
    sh /vagrant/scripts/setup.sh
  SHELL
end
