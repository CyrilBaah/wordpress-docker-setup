# Overview | WordPress Docker Setup

This Python script automates the setup of a WordPress site using Docker with a LEMP stack  (Linux, Nginx, Mysql, PHP) inside containers. It provides a convenient way to create, enable, disable, or delete WordPress sites without the need for manual configuration.

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/ "docker")
- [docker-compose](https://docs.docker.com/compose/install/ "docker-compose")
- [Python 3](https://www.python.org/downloads/ "python")

## Installation and Usage

1. Clone this repository:
```sh
  git clone https://github.com/your-username/wordpress-docker-setup.git
  cd wordpress-docker-setup
```
2. Create new WordPress site:
```sh
  python3 create_wordpress_site.py <site_name>
```
3. Disable site:
```sh
  python3 create_wordpress_site.py <site_name> disable
```
4. Enable site:
```sh
  python3 create_wordpress_site.py <site_name> enable
```
4. Delete site:
```sh
  python3 create_wordpress_site.py <site_name> delete
```