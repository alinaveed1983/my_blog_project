
Here's a straightforward project idea that covers both front-end and back-end development, suitable for beginners learning full stack development using Django (Python) for the back end, MySQL for the database, and a simple HTML/CSS/JavaScript front end.


Project: Personal Blog Website
Description: Create a basic blogging platform where users can:


 1. View a list of blog posts.
 2. Read individual blog posts.
 3. Create, edit, and delete blog posts (admin feature).
 4. This project will give you hands-on experience with:


Front-end development (HTML/CSS/JavaScript).
Back-end development (Python with Django).
Database management (MySQL).
Full stack integration.
Project Features
Home Page: Displays a list of all blog posts.
Blog Post Page: Displays the content of a single blog post.
Admin Page: Allows the admin user to create, edit, or delete blog posts.
Contact Page: A simple form for users to send messages.


Technologies to Use

    Back-End: Python, Django
    Database: MySQL
    Front-End: HTML, CSS, JavaScript (Bootstrap for styling, optional)
    Tools: Django Template Engine for rendering HTML


![image](https://github.com/user-attachments/assets/ff7e19b3-925e-41b5-94b3-7f3fa3d8808a)







Basic Production Setup (2 EC2 Instances)

    Components:
    EC2 Instance 1: Hosts the Django application.
    EC2 Instance 2: Hosts the MySQL database.

    Pros:
    Separates the application and database for better performance and security.
    Easier to scale the application server independently of the database.

    Cons:
    Slightly more complex to set up.
    Higher cost (two EC2 instances).
    Recommended EC2 Instance Types:
    Application Server: t2.micro or t3.micro (for small projects).
    Database Server: t2.micro or t3.micro.



Deployment Steps:
    
    EC2 Instance 1:
     1. Install Django, Gunicorn, and Nginx.
     2. Set up the Django application.

    EC2 Instance 2:
     1. Install MySQL and configure the database.
     2. Allow remote access from the application server (update MySQL settings and security group).
     3. Update Django’s settings.py to connect to the MySQL database on EC2 Instance 2.


MySQL Installation:
    ![image](https://github.com/user-attachments/assets/53c6b4c1-50f2-4660-bc9c-571dab3f372e)


    # Step 1: Update the System
    sudo apt update && sudo apt upgrade -y
    # Step 2: Install Prerequisites (Alien and libaio1)
    sudo apt install alien  libaio-dev -y
    # Step 3: Download MySQL 8.0 RPM Package
    wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
    # Step 4: Convert the RPM Package to DEB Format
    sudo alien -d mysql80-community-release-el8-1.noarch.rpm
    # Step 5: Install the Converted DEB Package
    sudo dpkg -i mysql80-community-release_0el8-2_all.deb
    # Step 6: Install MySQL Server
    sudo apt update
    sudo apt install mysql-server -y
    # Step 7: Start MySQL Service
    sudo systemctl enable mysql
    sudo systemctl start mysql
    sudo systemctl status mysql
    # Step 8: Find the Temporary Root Password
    cat /var/log/mysql/error.log
    [Warning] [MY-010453] [Server] root@localhost is created with an empty password! Please consider switching off the --initialize-insecure option.
    # Step 9: Log in to MySQL with the Temporary Password
    sudo mysql -u root
    # Step 10: Change the Root Password (Inside MySQL Shell)
    CREATE USER 'root'@'%' IDENTIFIED BY 'root@1234';
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    # Edit MySQL Configuration File to Allow Remote Access
    sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
    # Comment out the bind-address line:
    # bind-address = 127.0.0.1
    # Restart MySQL Service
    sudo systemctl restart mysql
    # Optional Step 2: Configure Firewall to Allow MySQL Traffic
    sudo ufw allow 3306
    sudo ufw reload
    # Verify MySQL Status Again
    sudo systemctl status mysql
    # Create database "my_blog_db" for the project
    sudo mysql -u root -p
    create database my_blog_db;
    show databases;
     

Django (EC2):
    ![image](https://github.com/user-attachments/assets/02665ea3-fb51-4f4c-a053-f1840ca4e631)


    sudo apt update && sudo apt upgrade -y
    sudo apt install pkg-config libmysqlclient-dev -y
    sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx net-tools -y
    mkdir ~/my_blog_project
    cd ~/my_blog_project
    git clone https://github.com/alinaveed1983/my_blog_project.git .
    python3 -m venv venv
    source venv/bin/activate
    (venv) pip install django mysqlclient gunicorn
    
    #Test MySQL Client Connection
    (venv) python
    import MySQLdb
    try:
        conn = MySQLdb.connect(
            host="172.31.38.173",
            user="root",
            password="root@1234",
            database="my_blog_db",
            connect_timeout=10
        )
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

    # Configure gunicorn  
    sudo vi /etc/systemd/system/gunicorn.service
    [Unit]
    Description=Gunicorn daemon for Django project
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/my_blog_project
    ExecStart=/home/ubuntu/my_blog_project/venv/bin/gunicorn --access-logfile - --workers 3 --bind 127.0.0.1:8001 my_blog.wsgi:application
    UMask=0007
    

    [Install]
    WantedBy=multi-user.target

    sudo systemctl daemon-reload
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl status gunicorn

    # Generate a Self-Signed Certificate [ test/dev environments ]:
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
    
    # Configure Nginx
    sudo vi /etc/nginx/sites-available/my_blog
    server {
			     listen 443 ssl;
			     server_name ec2-54-166-237-50.compute-1.amazonaws.com;

			     ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
			     ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

		     location / {
			     proxy_pass http://127.0.0.1:8001;
			     proxy_set_header Host $host;
			     proxy_set_header X-Real-IP $remote_addr;
			     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			     proxy_set_header X-Forwarded-Proto $scheme;
		   }

			     location /static/ {
				        alias /home/ubuntu/my_blog_project/static/;
			     }
		    }


    sudo rm /etc/nginx/sites-enabled/default
    sudo ln -s /etc/nginx/sites-available/my_blog /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ss -tuln | grep 443
    sudo netstat -tuln | grep 443

    
    # Apply Migrations and Collect Static Files
    (venv) python manage.py check
    (venv) python manage.py makemigrations blog_app
    (venv) python manage.py migrate
    (venv) python manage.py collectstatic
    (venv) python manage.py createsuperuser

    # Test the transfer data from or to a server using HTTPs
    curl -I -k https://ec2-184-72-129-63.compute-1.amazonaws.com
    
    # Test the Django Application
    (venv) python manage.py runserver 0.0.0.0:8000

    # Execute in browser
    http://44.223.52.232:8000
    https://ec2-54-166-237-50.compute-1.amazonaws.com

    # Admin Access
    http://44.223.52.232:8000/admin


