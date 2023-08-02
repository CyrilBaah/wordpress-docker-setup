#!/usr/bin/env python3
import os
import subprocess
import sys

def check_installed(command):
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

def modify_hosts_entry(site_name):
    # Modify /etc/hosts entry (This will work inside the container but not on the host)
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write(f"127.0.0.1 {site_name}\n")

def create_wordpress_site(site_name):
    # Creating required directories
    if not os.path.exists("wordpress-docker"):
        os.makedirs("wordpress-docker")
    os.chdir("wordpress-docker")

    # Creating nginx configuration file
    nginx_config_content = """
events {}
http {
    server {
        listen 80;
        server_name $host;
        root /usr/share/nginx/html;
        index  index.php index.html index.html;

        location / {
            try_files $uri $uri/ /index.php?$is_args$args;
        }

        location ~ \.php$ {
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_pass phpfpm:9000;
            fastcgi_index   index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }
    }
} 
"""
    if not os.path.exists("nginx"):
        os.makedirs("nginx")
    with open("nginx/default.conf", "w") as nginx_conf_file:
        nginx_conf_file.write(nginx_config_content)

    # Creating index.php file in public
    if not os.path.exists("public"):
        os.makedirs("public")
    with open("public/index.php", "w") as index_file:
        index_file.write("<?php\nphpinfo();\n")

    # Creating docker-compose.yml file
    docker_compose_content = """
version: '3'

services:
  #databse
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: password
    networks:
      - wpsite
  #php-fpm
  phpfpm:
    image: php:fpm
    depends_on:
      - db
    ports:
      - '9000:9000'
    volumes: ['./public:/usr/share/nginx/html']
    networks:
      - wpsite
  #phpmyadmin
  phpmyadmin:
    depends_on:
      - db
    image: phpmyadmin/phpmyadmin
    restart: always
    ports:
      - '8080:80'
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: password
    networks:
      - wpsite
  #wordpress
  wordpress:
    depends_on: 
      - db
    image: wordpress:latest
    restart: always
    ports:
      - '8000:80'
    volumes: ['./:/var/www/html']
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    networks:
      - wpsite
  #nginx
  proxy:
    image: nginx:1.17.10
    depends_on:
      - db
      - wordpress
      - phpmyadmin
      - phpfpm
    ports:
      - '8001:80'
    volumes: 
      - ./:/var/www/html
      - ./nginx/default.conf:/etc/nginx/nginx.conf
    networks:
      - wpsite
networks:
  wpsite:
volumes:
  db_data:
"""
    with open("docker-compose.yml", "w") as docker_compose_file:
        docker_compose_file.write(docker_compose_content)

    # Starting the Docker containers
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print(f"Servers for '{site_name}' have been created successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        sys.exit(1)

def main():
    if not check_installed("docker-compose"):
        print("Docker Compose is not installed. Please make sure Docker Compose is installed and in the system PATH.")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: ./create_wordpress_site.py <site_name>")
        sys.exit(1)

    site_name = sys.argv[1]
    modify_hosts_entry(site_name)
    create_wordpress_site(site_name)

if __name__ == "__main__":
    main()