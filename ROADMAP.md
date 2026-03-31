# Roadmap

This document outlines the planned features and improvements for **DIVE Tools**.

## Current Version

- **1.0.0** – Initial release
  - Flask-based API for checking DIVE protection
  - Web interface for manual checks
  - REST API endpoints (`GET /api/check`, `POST /api/check`)
  - DIVE policy retrieval (scope, directives, DNSSEC status)
  - Domain key listing
  - Docker and `docker-compose` support
  - Configuration via `.env`

## Upcoming Features

- **Additional DIVE Testing Tools**

  - More developer tools to validate DIVE policies
  - Enhanced checks for domain configuration and key validity

- **API Rate Limiting**
  - Limit number of requests per client/IP
  - Prevent abuse and improve reliability

## Future Ideas

- Analytics dashboard for checked URLs
- Integration with browser extensions or CI/CD pipelines
- Advanced reporting of policy compliance
