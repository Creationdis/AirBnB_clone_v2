# instal and configure nginx
exec { 'update':
  command     => '/usr/bin/apt-get update',
  onlyif      => '/usr/bin/which nginx',
}
-> package { 'nginx':
  ensure => installed,
}
-> exec { 'run1':
  command => '/usr/bin/mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"',
}
-> exec { 'run2':
  command => '/usr/bin/echo "Hi!" | sudo tee /data/web_static/releases/test/index.html > /dev/null',
}
-> exec { 'run3':
  command => '/usr/bin/rm -rf /data/web_static/current',
}
-> exec { 'run4':
  command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
}
-> exec { 'run5':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}
-> exec { 'add_lines':
  command => 'sudo sed -i "s|server_name _;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" /etc/nginx/sites-enabled/default',
  provider => shell,
}
-> exec { 'run6':
  command => '/usr/sbin/service nginx restart',
}
