# MHA API Project

This Django + Django REST Framework (DRF) project provides a structured API for My Hero Academia characters and their associated metadata, such as quirks and affiliations. It is designed for educational, fan-based, or prototype purposes and includes a scraper and a management interface for updating data.

## Features

- RESTful API endpoints for characters
- Admin panel for managing character data
- DRF Spectacular integration for API documentation
- Custom management command for data cleanup
- Local media storage for character images

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/mha_api_project.git
   cd mha_api_project
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the app**
   - Admin panel: http://localhost:8000/admin/
   - API root: http://localhost:8000/api/
   - API docs (Swagger UI): http://localhost:8000/api/docs/
   - API docs (ReDoc): http://localhost:8000/api/redoc/

## Notes

- Make sure `drf_spectacular` and `drf_spectacular_sidecar` are installed for full documentation support.
- Run `python manage.py collectstatic` when static assets are updated.
- Images are stored locally in `media/characters/`.

## License

This project is for educational and non-commercial use only.
