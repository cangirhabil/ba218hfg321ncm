# osTicket Docker Setup for BacFuzz

**One-command installation for osTicket ready for security testing.**

## 🚀 Quick Start

```bash
cd /Users/admin/Desktop/ba218hfg321ncm/WUT/osTicket
./setup.sh
```

That's it! The script will:

1. Start Docker containers (osTicket + MariaDB)
2. Prepare the installation
3. Open your browser to complete setup
4. Provide all credentials and access info

## 🌐 After Setup

The script opens: **http://localhost:8085/setup/**

**Fill the form with these values:**

```
Helpdesk Name: osTicket BacFuzz System
Admin Email: admin@osticket.local
Username: admin
Password: admin123

Database Host: db
Database Name: osticket
Database User: osticket
Database Password: osticket123
```

Click "Install Now" and you're done!

## 🎯 Access Points

After installation:

- **Main Site:** http://localhost:8085
- **Admin Panel:** http://localhost:8085/scp
- **New Ticket:** http://localhost:8085/open.php

**Login:** adminuser / admin123

## 🎪 BacFuzz Testing Targets

- **Authentication:** `/scp/login.php`, `/login.php`
- **Ticket System:** `/open.php`, `/tickets.php`
- **Admin Functions:** `/scp/*`
- **API Endpoints:** `/api/*`
- **File Uploads:** Ticket attachments

## 🔧 Management

```bash
# View logs
docker-compose logs -f

# Stop system
docker-compose down

# Complete reset
docker-compose down -v && ./setup.sh
```

## � System Info

- **osTicket Version:** 1.18-git (Development)
- **Database:** MariaDB 10.6
- **Web Server:** PHP 8.3.6-Apache
- **Port:** 8085
- **Network:** Isolated Docker network

**Ready for comprehensive security testing! 🎯**

# Access database

docker exec -it osticket-db-1 mysql -u osticket -posticket123 osticket

# Access application container

docker exec -it osticket-app-1 bash

```

## File Structure

```

osTicket/
├── docker-compose.yaml # Docker Compose configuration
├── setup.sh # Automated installation script
├── README.md # This file
├── configs/
│ ├── php.ini # PHP configuration
│ └── 000-default.conf # Apache virtual host
└── instrumentation/ # Fuzzing instrumentation files

```

## Troubleshooting

1. **Port conflicts**: If port 8085 is in use, change it in docker-compose.yaml
2. **Database issues**: Check container logs with `docker-compose logs db`
3. **Permission issues**: Ensure proper file permissions in the container
4. **Installation fails**: Remove volumes and retry: `docker-compose down -v`

## Security Notes

- The setup removes the `/setup` directory after installation for security
- Default credentials should be changed in production
- File permissions are set appropriately for osTicket requirements

## Integration with Fuzzing

This setup is designed to work with the existing fuzzing infrastructure:
- Instrumentation files are copied to the container
- Shared tmpfs volume is mounted for fuzzing outputs
- The application is accessible on a dedicated port (8085)
```
