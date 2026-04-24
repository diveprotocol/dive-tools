# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.2.0] - 2026-04-01

### Added

- N/A

### Changed

- Implementation for the `0.2.0` opendive-client.

### Fixed

- N/A

---

## [1.0.1] - 2026-04-01

### Added

- N/A

### Changed

- N/A

### Fixed

- DNSSEC validation improved.

---

## [1.0.0] - 2026-04-01

### Added

- Initial release of **DIVE Tools**.
- Flask-based API to check if a URL is protected by the DIVE protocol.
- Web interface for manual URL checks.
- REST API endpoints:
  - `GET /api/check`
  - `POST /api/check`
- DIVE policy retrieval (scope, directives, DNSSEC status).
- Domain key listing.
- Dockerfile and `docker-compose.yml` for easy deployment.
- Configuration via `.env` file.
- Deployment instructions with Gunicorn and Docker.
- Integration instructions for embedding in the DIVE project website.

### Changed

- N/A

### Fixed

- N/A
