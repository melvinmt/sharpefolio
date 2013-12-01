# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :forwarded_port, guest: 3306, host: 3306
  config.vm.network :private_network, ip: "192.168.33.10"

  config.vm.synced_folder ".", "/home/vagrant/app"

  config.vm.provider :virtualbox do |vb|
    # Don't boot with headless mode
    vb.gui = true

    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provider :lxc do |lxc, override|
    override.vm.box = "lxc-precise64"
    override.vm.box_url = "http://dl.dropbox.com/u/13510779/lxc-precise-amd64-2013-05-08.box"
  end

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "vagrant/cookbooks"
    chef.roles_path     = "vagrant/roles"
    chef.data_bags_path = "vagrant/data_bags"
    chef.add_role "sharpefolio-vagrant"
  end
end
