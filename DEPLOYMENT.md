# Django Site Deployment Guide

This guide will help you deploy your Django LeetCode site to make it accessible from the internet.

## Prerequisites

- Python 3.11+
- Git
- A deployment platform account (Heroku, Railway, DigitalOcean, etc.)

## Quick Deployment Options

### Option 1: Heroku (Easiest)

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set DEBUG=False
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Run migrations**:
   ```bash
   heroku run python manage.py migrate --settings=config.settings_production
   ```

6. **Collect static files**:
   ```bash
   heroku run python manage.py collectstatic --noinput --settings=config.settings_production
   ```

### Option 2: Railway

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard:
   - `SECRET_KEY`: Generate a new secret key (use the one generated above)
   - `DEBUG`: False
3. **Deploy automatically** - Railway will use the provided configuration files:
   - `railway.json` - Railway deployment configuration
   - `nixpacks.toml` - Build configuration
   - `start.sh` - Startup script
4. **Railway will automatically**:
   - Install dependencies from `requirements.txt`
   - Collect static files
   - Run database migrations
   - Start the application with Gunicorn

### Option 3: DigitalOcean App Platform

1. **Create a new app** in DigitalOcean
2. **Connect your GitHub repository**
3. **Configure build settings**:
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput --settings=config.settings_production`
   - Run command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --settings=config.settings_production`
4. **Set environment variables**:
   - `SECRET_KEY`
   - `DEBUG=False`

### Option 4: Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **For production with Docker**:
   ```bash
   docker build -t django-leetcode .
   docker run -p 8000:8000 -e SECRET_KEY="your-secret-key" django-leetcode
   ```

## Local Production Testing

Before deploying, test your production settings locally:

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
python manage.py runserver --settings=config.settings_production

# Or with Gunicorn
gunicorn config.wsgi:application --settings=config.settings_production
```

## Important Security Notes

1. **Change the SECRET_KEY** - Generate a new one for production
2. **Set DEBUG=False** - Never run with DEBUG=True in production
3. **Use HTTPS** - Enable SSL certificates for your domain
4. **Restrict ALLOWED_HOSTS** - Set to your actual domain instead of '*'
5. **Use environment variables** for sensitive data

## Domain Configuration

After deployment, you can:

1. **Use the provided subdomain** (e.g., your-app.herokuapp.com)
2. **Add a custom domain** in your platform's dashboard
3. **Update ALLOWED_HOSTS** in settings_production.py with your domain

## Database Considerations

- **SQLite**: Good for development, but consider PostgreSQL for production
- **PostgreSQL**: Recommended for production (included in docker-compose.yml)
- **Database migrations**: Always run after deployment

## Static Files

Static files are configured to be served by WhiteNoise in production. Make sure to run:
```bash
python manage.py collectstatic --noinput --settings=config.settings_production
```

## Monitoring and Logs

- Check your platform's logging system
- Monitor application performance
- Set up error tracking (Sentry, etc.)

## Troubleshooting

1. **Static files not loading**: Ensure collectstatic was run
2. **Database errors**: Check database configuration and run migrations
3. **Permission errors**: Check file permissions and environment variables
4. **Port issues**: Ensure your app binds to the correct port (usually $PORT or 8000)

## Next Steps

1. Choose a deployment platform
2. Follow the specific platform instructions
3. Test your deployed application
4. Set up monitoring and backups
5. Consider adding a custom domain

Your Django LeetCode site should now be accessible from the internet!
