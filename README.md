# Automated Review Rating System

A Django-based web application that allows users to submit, view, and analyze reviews.  
It integrates deep learning models to provide insights such as aggregated ratings and predictions.

---

## 🚀 Features
- Add and manage reviews
- Aggregate ratings with statistics (average, count per star rating)
- Deep Learning integration for predictions
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

```
automated-review-system/
│── backend/           # Django project files
│── review/            # Review app (models, views, serializers)
    │── ml_models/     # Trained DL models (ignored in GitHub)
│── manage.py          # Django entry point
│── requirements.txt   # Dependencies
│── .gitignore         # Ignored files

```

## Note About ML Models
```markdown
## 🔮 DL Models
The `ml_models/` folder is ignored in version control (`.gitignore`).  
You’ll need to place the required trained models in this folder to enable ML-based predictions.  

Since model files are usually large, they are not pushed to GitHub.  
You can either:
- Train your own models and save them into `ml_models/`, or  
- Request pre-trained models from the project maintainer.  
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   git clone https://github.com/1Jayakrishnan/automated-review-system.git
   cd automated-review-system

2. **Create a virtual environment:**
   python -m venv venv
   
3. **Activate the environment:**
   windows : venv\Scripts\activate or
   mac/linux : source venv/bin/activate

4. **Install dependencies:**
   pip install -r requirements.txt

5. **Run migrations:**
   python manage.py migrate

6. **Start the development server:**
   python manage.py runserver

7. **Visit:**
   http://127.0.0.1:8000
