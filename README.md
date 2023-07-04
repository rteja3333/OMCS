# OMCS
# Online Medical Consultation System  - Django App

Welcome to the Online Medical Consultation System (OMCS) repository! 
OMCS is a web application developed using Django, which allows users to book medical appointments, manage hospitals and doctors, and facilitate online medical consultations.

## Features

OMCS provides the following features for different user roles:

- **Admin**
  - Add new hospitals to the system.
  - Edit existing hospital information.
  - Approve new doctor registrations.
  - Manage doctor profiles and information.
  - View and analyze system data.

- **Doctor**
  - Approve or decline patient appointments for a specific day and time slot.
  - Send messages to patients regarding their appointment status.
  - Edit doctor profile information.

- **Patient**
  - Book appointments with doctors based on specialization and location (using pincode).
  - Receive email notifications for appointment confirmation and updates.
  - Manage personal information and update contact details.

## Installation

To install and run the OMCS application, follow these steps:

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the project directory:
```bash
cd OMCS
```

3. Create a virtual environment:
```bash
python -m venv env
```

4. Activate the virtual environment:
- For Windows:
```bash
env\Scripts\activate
```
- For Linux/macOS:
```bash
source env/bin/activate
```

5. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Set up the database:
```bash
python manage.py migrate
```

2. Create a superuser (admin) account:
```bash
python manage.py createsuperuser
```

3. Run the development server:
```bash
python manage.py runserver
```

4. Access the OMCS application in your web browser:
```bash
http://localhost:8000/
```


## Database

OMCS utilizes SQLite3 as the default database for development purposes. If you wish to use a different database, modify the `settings.py` file in the `OMCS` directory and update the database settings accordingly.

## File Structure

The file structure of the OMCS application is as follows:

OMCS/
├── OMCS/  
│ ├── templates/  
│ ├── admin.py  
│ ├── apps.py    
│ ├── forms.py    
│ ├── models.py    
│ ├── serialisers.py     
│ ├── tests.py    
│ ├── urls.py    
│ ├── views.py    
│ └── ...     
├── SE_project/     
│ ├── asgi.py     
│ ├── settings.py     
│ ├── urls.py     
│ ├── wsgi.py    
├── db.sqlite3    
├── manage.py        
├── requirements.txt    
└── README.md     

### Let's briefly go over each file and directory:

- `OMCS/` : The main directory for your Django project.
- `OMCS/ templates/` : Contains HTML templates for rendering views.
- `OMCS/admin.py` : Configurations for the Django admin interface.
- `OMCS/apps.py` : Configuration for the OMCS app.
- `OMCS/forms.py` : Contains form classes for handling user input.
- `OMCS/models.py` : Defines database models(classes) for the OMCS app.
- `OMCS/serializers.py` : Serializers for converting Django models to JSON.
- `OMCS/tests.py` : Unit tests for the OMCS app.
- `OMCS/urls.py` : URLS used for the OMCS app.
- `OMCS/views.py` : Contains all functionalities in python.
- `SE_project/`: The project directory generated by Django.
- `SE_project/asgi.py` : ASGI configuration for the project.
- `SE_project/settings.py` : Project settings and configurations.
- `SE_project/urls.py` : Top-level URL configuration for the project.
- `SE_project/wsgi.py` : WSGI configuration for the project.
- `db.sqlite3`: The SQLite database file where your project's data is stored.
- `manage.py`: The command-line utility for managing the Django project.
- `requirements.txt`: A file listing the required Python libraries and versions for your project.
- `README.md:` The readme file for the project.

## Requirements

The OMCS application relies on the following libraries:

- Django (version 3.2)
- SQLite3 (included with Django)
- Other dependencies (specified in the `requirements.txt` file)

You can install all the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

Make sure to use a compatible version of Python and update the dependencies as necessary.

## Contributing
Contributions to the OMCS project are always welcome! If you'd like to contribute, please follow the guidelines outlined in the CONTRIBUTING.md file.

## License
MIT License

The OMCS application is open-source and licensed under the MIT License. Please review the LICENSE file for more details.

