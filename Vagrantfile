# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.synced_folder ".", "/srv/www/bushido", create: true
  config.vm.synced_folder "salt/root", "/srv/salt", create: true
  config.vm.synced_folder "salt/pillar", "/srv/pillar", create: true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end
  config.vm.provision :salt do |salt|
    salt.masterless = true
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
    salt.colorize = true
  end
end
