# 🚀 Credit Service System

This is a **Django-based Loan Management System** where users can:  
✅ Apply for loans  
✅ Make payments  
✅ View their transaction statements  

---

## 📌 Project Setup Instructions

### 1️⃣ Clone the Repository
git clone <your-repo-url>  
cd <your-project-folder>  

---

### 2️⃣ Create a Virtual Environment
python -m venv venv  
source venv/bin/activate  # For macOS/Linux  
venv\Scripts\activate     # For Windows  

---

### 🔧 Install Dependencies

Run the following command to install all required dependencies:  
pip install django djangorestframework mysqlclient pymysql  

If you face errors with `mysqlclient`, try:  
pip install pymysql  

Then, add the following line to **`credit_service/__init__.py`** to enable MySQL support:  
import pymysql  
pymysql.install_as_MySQLdb()  

---

## 🛠️ MySQL Database Setup

### 3️⃣ Configure MySQL Database

1. **Start MySQL Server**  
2. **Login to MySQL CLI**  
   mysql -u root -p  
3. **Create a Database**  
   CREATE DATABASE credit_service;  
4. **Exit MySQL**  
   EXIT;  

---

## 🔧 Changes to `settings.py`

Open **`credit_service/settings.py`** and update the **DATABASES** configuration:

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'credit_service',  
        'USER': 'root',  
        'PASSWORD': 'your_mysql_password',  
        'HOST': 'localhost',  
        'PORT': '3306',  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }  
}  

---

## 4️⃣ Apply Migrations & Create Superuser

python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  # Create admin user  

---

## 5️⃣ Run the Server

python manage.py runserver  

Your **Django Credit Service System** should now be running at:  
http://127.0.0.1:8000/  

---

## 🛠️ Additional Notes
- Ensure **MySQL Server is running** before applying migrations.  
- If you face **MySQL connection errors**, ensure `mysqlclient` or `pymysql` is installed.  

🚀 **Your Loan Management System is ready!** 🎉  
