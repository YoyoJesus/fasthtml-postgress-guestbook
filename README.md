# FastHTML Python Guestbook (Docker)

This project is a FastHTML-based guestbook web app using Flask and PostgreSQL, fully containerized with Docker.

## Getting Started

1. Clone this repository.
2. Build and start the app with Docker Compose:
	 ```powershell
	 docker-compose up --build
	 ```
3. The web app will be available at [http://localhost:5000](http://localhost:5000).

## Database

PostgreSQL runs in a Docker container. The default credentials are:
	- User: `admin`
	- Password: `123456`
	- Database: `fasthtml_db`

## Admin Access

To delete guestbook entries, log in as admin:
	- Username: `admin`
	- Password: `123456789`

## Customization

- Change database credentials in `docker-compose.yml` and `main.py` as needed.
- Change admin password in `main.py`.
