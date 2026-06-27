# Facility Booking Management System

---

## Project Information

**Project Title**

Facility Booking Management System

**Repository**

> https://github.com/uthrahh/FacilityBooking
> 

#### Description

The Facility Booking Management System is a web-based application developed to digitize the reservation and administration of laboratories, equipment, and meeting halls within an organization.

The system provides separate interfaces for Startup Users and Administrators. Startup users can request facility bookings, track their booking status, and receive notifications. Administrators can manage facilities, review booking requests, approve or reject reservations, and monitor system activities through an administrative dashboard.

The application eliminates manual booking processes, prevents scheduling conflicts, centralizes facility management, and maintains complete booking history.

**Framework**

Django 6

**Developed By**

Pavithra Uthrah R. K. - uthrahrk@gmail.com

---

## Technology Stack

#### Backend

- Python 3.13
- Django 6
- Django ORM

#### Database

- PostgreSQL

#### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

#### Additional Libraries

- psycopg2
- Django Authentication
- Django Sessions

---

## Installation Guide

#### 1. Clone Repository

```bash
git clone https://github.com/uthrahh/FacilityBooking
cd FacilityBooking
```

#### 2. Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure PostgreSQL

Create a PostgreSQL database.

Example:

```
Database : facility_booking
User     : facility_admin
Password : ********
Host     : localhost
Port     : 5432
```

Update the database configuration in:

```
config/settings.py
```

#### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Administrator

```bash
python manage.py createsuperuser
```

Follow the prompts:

```
Username:
Email:
Password:
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

Application:

```
http://127.0.0.1:8000/
```

Admin Panel:

```
http://127.0.0.1:8000/admin/
```

---

## Project Structure

```
FacilityBooking
│   .gitattributes
│   .gitignore
│   manage.py
│   requirements.txt
│
├───accounts
│   │   admin.py
│   │   apps.py
│   │   decorators.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           __init__.py
│
├───admin
│   └───labs
│       └───import
├───bookings
│   │   admin.py
│   │   api.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   services.py
│   │   tests.py
│   │   urls.py
│   │   utils.py
│   │   validators.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           0001_initial.py
│           __init__.py
│
├───config
│       asgi.py
│       settings.py
│       urls.py
│       wsgi.py
│       __init__.py
│
├───core
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           __init__.py
│
├───dashboard
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           __init__.py
│
├───halls
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   import_csv.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           0001_initial.py
│           __init__.py
│
├───labs
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   import_csv.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           0001_initial.py
│           __init__.py
│
├───media
├───notifications
│   │   admin.py
│   │   apps.py
│   │   context_processors.py
│   │   models.py
│   │   services.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           0001_initial.py
│           0002_notification_startup.py
│           __init__.py
│
├───startups
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   views.py
│   │   __init__.py
│   │
│   └───migrations
│           0001_initial.py
│           __init__.py
│
├───static
│   ├───css
│   │       style.css
│   │
│   └───js
│           hall_availability.js
│           lab_availability.js
│           lab_booking.js
│
└───templates
    │   base.html
    │
    ├───accounts
    │       admin_login.html
    │       dashboard.html
    │       login.html
    │       signup.html
    │
    ├───bookings
    │       hall_booking.html
    │       lab_booking.html
    │       my_bookings.html
    │
    ├───core
    │       home.html
    │
    ├───dashboard
    │       admin_dashboard.html
    │       calendar.html
    │       dashboard.html
    │       equipment_form.html
    │       equipment_list.html
    │       hall_booking_list.html
    │       hall_form.html
    │       hall_list.html
    │       import_csv.html
    │       lab_booking_list.html
    │       lab_form.html
    │       lab_list.html
    │       notification_list.html
    │       startup_form.html
    │       startup_list.html
    │
    ├───labs
    │       upload_labs.html
    │
    └───notifications
            list.html
```

---

## Database Models

#### Accounts

- Admin User
- Startup User

#### Startups

- Startup

#### Laboratories

- Lab
- Equipment

#### Bookings

- LabBooking
- LabBookingEquipment
- HallBooking
- BookingHistory

#### Notifications

- Notification

---

## User Roles

#### Startup User

- Login
- Dashboard
- Book Laboratories
- Book Equipment
- Book Meeting Halls
- View Booking Status
- Cancel Bookings
- View Notifications
- Calendar View

#### Administrator

- Login
- Dashboard
- Startup Management
- Laboratory Management
- Equipment Management
- Hall Management
- Review Booking Requests
- Approve / Reject Bookings
- View Booking History
- Manage Notifications

---

## Major Features

#### Authentication

- Secure login system
- Session-based authentication
- Startup authentication
- Administrator authentication
- Protected routes using custom decorators

#### Startup Management

Administrator can:

- Add startups
- View startup list
- Activate or deactivate startups
- Manage startup records

#### Laboratory Management

Administrator can:

- Add laboratories
- Edit laboratory information
- Enable or disable laboratories
- View laboratory list

Each laboratory contains:

- Lab ID
- Name
- Description
- Availability Status

#### Equipment Management

Administrator can:

- Add equipment
- Assign equipment to laboratories
- Configure hourly usage fee
- Activate or deactivate equipment

Each equipment contains:

- Equipment ID
- Equipment Name
- Associated Lab
- Hourly Fee
- Availability Status

#### Hall Management

Administrator can:

- Add halls
- Configure seating capacity
- Update descriptions
- Activate or deactivate halls

Each hall contains:

- Hall ID
- Hall Name
- Capacity
- Description
- Availability Status

#### Laboratory Booking Module

Startup users can:

- Select laboratory
- Select booking date
- Book multiple equipment
- Specify individual time slots
- View equipment availability
- Calculate estimated booking fee
- Submit booking request

Features:

- Equipment conflict validation
- Time overlap validation
- Multiple equipment booking
- Automatic fee calculation
- Booking history generation

#### Hall Booking Module

Startup users can:

- Select hall
- Choose booking time
- Select AC
- Select projector
- Specify seating requirement
- Request microphones
- Request water bottles

Features:

- Hall availability validation
- Time conflict prevention
- Capacity validation
- Booking history tracking

#### Booking Workflow

1. Startup submits booking request.
2. Booking status is created as **NEW**.
3. Administrator reviews request.
4. Administrator approves or rejects request.
5. Notification is generated.
6. Booking history is stored.

#### Notifications

The system automatically generates notifications for:

- Booking Approved
- Booking Rejected
- Booking Cancelled

Unread notification count is displayed in the dashboard.

---

## Dashboard Features

#### Startup Dashboard

Displays:

- Total Lab Bookings
- Total Hall Bookings
- Pending Requests
- Approved Requests

#### Admin Dashboard

Displays:

- Total Startups
- Total Laboratories
- Total Equipment
- Total Halls
- Pending Lab Requests
- Pending Hall Requests
- Notification Count

#### Calendar

Integrated booking calendar displaying:

- Approved laboratory bookings
- Approved hall bookings
- Time slots
- Color-coded events

#### Booking Status

Possible booking statuses:

- NEW
- APPROVED
- REJECTED
- CANCELLED

---

## Frequently Used Commands

#### Collect Static Files (Production)

```bash
python manage.py collectstatic
```

#### Django Shell

```bash
python manage.py shell
```

---
