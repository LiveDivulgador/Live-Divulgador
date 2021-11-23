<i> Essa documentação de instalação é um PREVIEW </i>

<details>
    <summary>🇺🇸 English version</summary>

# How to Install

The bot has 2 possible installation methods:

- [Running inside a container](#running-inside-a-container)
- [Development on your local machine](#development-on-your-local-machine)

## Running inside a container

This is a very straightforward method. In order to be able to run the bot inside a container you need to have the following requirements:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker-compose](https://docs.docker.com/compose/install/)

Simply run `docker-compose up` to start the bot.

## Development on your local machine

Use this method only if you intend to help developing this project.

### Pre-requirements

This method will require that you previously install the MariaDB development driver dependencies on your system.

- [LibmariaDB-devel](https://www.mariadb.org/mariadb-enterprise/downloads/library/)

#### Debian based systems

If you are using a Debian system, you can install it by running the following command:

```sh
apt-get install libmariadb-dev
```

This may require **superuser** privileges.

#### Fedora

If you are running Fedora, you can install it by running the following command:

```sh
dnf install mariadb-devel
```

### Development build

Please, consider reading the pre-requirements section before proceeding.

Simply run:

```sh
sh scripts/install.sh
```

This should install the python `venv`, the bot components and the bot CLI `divulgador` on you local system.

### Building custom images

When you are developing the bot, you can build a custom image by running the following command:

First, set a custom tag release:

```sh
export TAG_RELEASE=<your-tag-id>
```

And then run the following command:

```sh
sh scripts/container_build.sh
```

This will build 2 docker images. You can check your custom built images by running the following command:

```sh
docker image ls
```

This should return the images you have built:

- An app image with the bot components called `divulgador_app:<your-tag-id>`
- A Database image with the MariaDB database `divulgador_db:<your-tag-id>`

You can also customize the [installation scripts](../scripts/common.sh) with your credentials and tag release.

#### Running the bot locally

Execute the following command to run the bot:

```sh
divulgador run
```

</details>

<details open >
    <summary>🇧🇷 Versão em português</summary>

# Como instalar

O bot possui dois métodos de instalação:

- [Rodando em um conteiner](#rodando-em-um-conteiner)
- [Desenvolvendo na sua máquina local](#desenvolvendo-na-sua-máquina-local)

## Rodando em um conteiner

O método de instalação é bem simples. Para conseguir rodar o bot em um container você precisa ter as seguintes dependências:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker-compose](https://docs.docker.com/compose/install/)

Execute `docker-compose up` para iniciar o bot.

## Desenvolvendo na sua máquina local

Use este método apenas se você tiver interesse em ajudar a desenvolver este projeto.

### Pré-requisitos

Esse método necessita que você previamente instale o driver de desenvolvimento do MariaDB no seu sistema.

- [LibmariaDB-devel](https://www.mariadb.org/mariadb-enterprise/downloads/library/)

#### Debian based systems

Se você estiver usando um sistema Debian, você pode instalá-lo executando o seguinte comando:

```sh
apt-get install libmariadb-dev
```

Talvez precise de privilégios de **superusuário**.

#### Fedora

Se estiver rodando Fedora, você pode instalá-lo executando o seguinte comando:

```sh
dnf install mariadb-devel
```

### Build de desenvolvedor

Considere ler os [pré-requisitos](#pré-requisitos) antes de prosseguir.

Execute:

```sh
sh scripts/install.sh
```

Isso instalará o `venv`, os componentes do bot e o CLI `divulgador` no seu sistema.

### Construindo imagens customizadas

Quando você estiver desenvolvendo o bot, você pode construir uma imagem customizada executando o seguinte comando:

Primeiramente, defina um tag de release:

```sh
export TAG_RELEASE=<your-tag-id>
```

E então execute o seguinte comando:

```sh
sh scripts/container_build.sh
```

Isso deve construir 2 imagens. Você pode ver as imagens customizadas construídas executando o seguinte comando:

```sh
docker image ls
```
Isso deve retornar as imagens que você construiu:

- Uma appimage com os componentes do bot chamada `divulgador_app:<your-tag-id>`
- A base de dados MariaDB chamada `divulgador_db:<your-tag-id>`

Você poderá também customizar os [scripts de instalação](../scripts/common.sh) com as suas credenciais e tag release.

#### Rodando o bot localmente

Execute o seguinte comando para rodar o bot:

```sh
divulgador run
```

</details>
