# Automated Review System

A Django-based web application that allows users to submit, view, and analyze reviews.  
It integrates machine learning models to provide insights such as aggregated ratings and predictions.

---

## 🚀 Features
- Add and manage reviews
- Aggregate ratings with statistics (average, count per star rating)
- Machine Learning integration for predictions
- REST APIs built with Django REST Framework
- Secure environment handling with `.env` files

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (development) 
- **ML Models:** TensorFlow / Pickle
- **Frontend:** React 
- **Other Tools:** Git, Virtualenv

---

## 📂 Project Structure
automated-review-system/
│── backend/ # Django project files
│── review/ # Review app (models, views, serializers)
│── manage.py # Django entry point
│── requirements.txt # Dependencies
│── .gitignore # Ignored files


## ⚙️ Installation & Setup

1. Clone the repository:
   git clone https://github.com/1Jayakrishnan/automated-review-system.git
   cd automated-review-system

2. Create a virtual environment:
   python -m venv venv
   
3. Activate the environment:
   windows : venv\Scripts\activate
   mac/linux : source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run migrations:
   python manage.py migrate

6. Start the development server:
   python manage.py runserver

7. Visit:
   http://127.0.0.1:8000
