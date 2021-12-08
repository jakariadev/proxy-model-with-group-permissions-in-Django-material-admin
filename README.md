# proxy-model-with-group-permissions-in-Django-material-admin


![Custom admin lookup](https://github.com/JakariaPUST/proxy-model-with-group-permissions-in-Django-material-admin/blob/main/static/images/custom%20admin.png)

> Proxy model, djagno group permissions.

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [Author Info](#author-info)

---

## Description

In this work, I have combinely used Django Rest API with React to implement proxy model, group, permissions.

#### Technologies

- [Django-Rest-Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [React](https://reactjs.org/)
- [Redux](https://redux.js.org/)
- [PostgreSQL](https://www.postgresql.com/)

---

## How To Use
Make sure Python and pip are available on the system.

#### Installation
- Virtualenvironment: 
    - ```pip install pipenv```

    ##### Activation
    - ```pipenv shell```
    
    ##### Install all packages

    After activating virtual environment. 
    Simply run ``` pip install -r requirements.txt ``` to install all the dependencies.
    
    ##### Postgre config or reset
    ``` sudo apt update```
    ``` sudo apt install postgresql ```
    ##### checking active or not:
    ```
    sudo systemctl is-active postgresql
    sudo systemctl is-enabled postgresql
    sudo systemctl status postgresql 
    ```
    ```sudo pg_isready```
    ##### Creating Database in PostgreSQL
    ```sudo su - postgres```
    ```psql```
    - Now create a new database and a user using the following commands.
    - postgres#: 
    ```
    CREATE USER jakaria WITH PASSWORD 'Jakariapassword';
    CREATE DATABASE jakariadb;
    GRANT ALL PRIVILEGES ON DATABASE jakariadb to jakaria;
    \q
    ```
    ##### Configuring PostgreSQL Client Authentication
    ```sudo vim /etc/postgresql/12/main/pg_hba.conf```
    ##### Restarting: 
    ```sudo systemctl restart postgresql```
    ------------------------------------------------
    ##### pgadmin web
    ##### Install pgadmin4 in ubuntu:
    ```
    curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
    sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
    ```
    **Then instal :**
    ```sudo apt install pgadmin4```
    
 
    ##### for reset email and pass
    ``` $ sudo mv /var/lib/pgadmin/pgadmin4.db /tmp ```
    
    ``` $ sudo /usr/pgadmin4/bin/setup-web.sh ```
    
    ##### Run in browser
    ```http://127.0.0.1/pgadmin4/```

#### Domain and sub domain configuration
- Type in ubuntu terminal ``` sudo nano /etc/hosts ```
- Or in Windows edit your host file in etc folder in c-drive.
- Then add & save e.g. ``` 127.0.0.1    www.jakariaPUST.com ```

---
## Refernce
 -[Postgre& Pgadmin Config.](https://www.tecmint.com/install-postgresql-and-pgadmin-in-ubuntu/)

## Author Info

- [@Jakaria](https://facebook.com/jakaria.pust)

[Back To The Top](#proxy-model-with-group-permissions-in-Django-material-admin)







```
username:fahad12
email:m6@12g.com
first_name:Md fahad 
last_name:hossain
password:abcgdhsgd122@asss1123
password2:abcgdhsgd122@asss1123
phone:+8801702929340
sex:M
avatar:img.jpg
```
