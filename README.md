# 🌐 MiniSocialMediaAPI

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-4.x-darkgreen?logo=django&logoColor=white)](https://www.djangoproject.com/) 
[![DRF](https://img.shields.io/badge/DRF-API-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue?logo=postgresql)](https://www.postgresql.org/)  

<p>
  <img src="https://skillicons.dev/icons?i=python,django,git,github,windows,vscode,postman,postgres">
</p>

📖 Description

**MiniSocialMediaAPI** is a mini project built with **Django** and **Django REST Framework (DRF)**.
It provides a set of **RESTful APIs** for a simple **social media** platform where users can:
- Create and manage accounts
- Share posts with text, images, or videos
- Interact with the platform through a clean and extensible API

This project is a great starting point for learning **Django** + **DRF** and can be expanded into a full-featured **social media application**.

🔑 Key points:
- Backend built with **Django** + **DRF**  
- API documentation generated with **drf-spectacular**  
- **JWT authentication system** for secure access  

---

## ✨ Features
- 👤 User Management – **Create, update, and manage** user accounts.
- 📤 Post Uploads – Share posts with **text, images, or videos** and manage them easily.
- 🤝 Follow & Unfollow – Connect with other **users** by **following or unfollowing** them.
- 🔖 Save Posts – **Save or unsave posts** shared by other users.
- 🔍 Explore – **Discover new posts and users** through the explore section.

---

## 🛠️ Requirements
- **Python 3.9+**  
- **PostgreSQL** (running locally or remote)  
- **Virtual environment** tool: `venv`

---

## ⚙️ Installation & Usage
```bash
1️⃣ Clone the repository
`git clone https://github.com/Amirhosein-Rezaie/MiniSocialMediaAPI.git`
`cd MiniSocialMediaAPI`

2️⃣ Create a virtual environment
`python -m venv .venv`
# Activate:
source `.venv/bin/activate`   # Linux/Mac
`.venv\Scripts\activate`     # Windows

3️⃣ Install dependencies
`pip install -r requirements.txt`

4️⃣ Apply migrations
`python manage.py makemigrations`
`python manage.py migrate`

5️⃣ Run the server
`python manage.py runserver`

6️⃣ use documents
after running the server open you browser and go to `http://127.0.0.1:8000/api/docs`
```
