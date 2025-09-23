# Nextcloud Setup Script

This script installs the Nextcloud project and creates test users through the project interface.

## Usage

```bash
./setup.sh
```

## Script Operations

1. **Project Installation:**
   - Stops and cleans existing containers
   - Starts Nextcloud, MariaDB and Redis services with Docker Compose
   - Waits for Nextcloud to be ready

2. **User Creation:**
   - Creates test users using Nextcloud OCC commands
   - Assigns users to groups
   - Creates test files

## Created Users

| Username | Password | Role | Group |
|----------|----------|------|-------|
| admin | admin123 | Administrator | - |
| testuser | TestUser2024! | Regular user | - |
| editor | EditorPass2024! | Editor | editors |
| viewer | ViewerPass2024! | Viewer | viewers |
| admin_test | AdminTest2024! | Test Admin | admins |

## Access

- **URL:** http://localhost:8084
- **Login:** Use the user credentials above to login

## Important Notes

- Script stops existing containers before running
- All users are created through Nextcloud's own user management system
- No direct database intervention is performed
- Test files are automatically created

## Troubleshooting

- If script hangs, check logs with `docker-compose logs`
- Check container status with `docker ps`
- For manual cleanup: `docker-compose down -v`