# 🚨 Incident Management System

A web-based Incident Management System built with **Flask**, **SQLite**, and **Bootstrap**, designed for tracking, viewing, and exporting incident reports. Easily deployable using **Docker**.

---

## 🐳 Docker Command & Usage Screens

### 1. Docker Commands  
![Docker Commands](Screenshots/1_Docker_cmds.png)

### 2. Running Docker Container  
![Docker Container](Screenshots/2_Docker_container.png)

### 3. Docker Image  
![Docker Image](Screenshots/3_Docker_image.png)

---

## 📦 Features

- Create, view, edit, and delete incidents
- Filter and sort incidents by various parameters
- View incident details on a separate page
- Export incident data to **CSV**
- Admin-only delete capability
- Fully Dockerized setup for easy deployment
- SMTP email Notifications
- SQLITE3 Database for storing incidents

---

## 🖥️ App Screenshots

### Main Page  
![Main Page](Screenshots/4_main_page.png)

### Incident Detail View  
![View Page](Screenshots/5_view_page.png)

### Export to CSV  
![Export CSV](Screenshots/6_Export_CSV_Faclity.png)



### SMTP Services  
![SMTP Services](Screenshots/7_SMTP_Services.png)

### SQLite3 Database  
![SQLite3](Screenshots/8_SQLite3.png)

---

## 🐳 Docker Setup

### 1. Build the Docker Image
```bash
docker-compose build
docker-compose up



