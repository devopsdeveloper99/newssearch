# Deployment Steps for shadhin247.com

## Current Issue: 503 Service Unavailable

The server is returning 503 because Django isn't configured to run. Follow these steps:

## Step 1: Upload Files to Server

Upload these files to `/home/shadhinc/newssearch/`:
- ✅ `passenger_wsgi.py` - WSGI entry point
- ✅ `.htaccess` - Server configuration
- ✅ All other project files

## Step 2: Configure Python App in cPanel

1. **Go to cPanel → Software → Setup Python App**

2. **Create a new Python application:**
   - **Python version**: 3.9 (or 3.8+)
   - **Application root**: `/home/shadhinc/newssearch`
   - **Application URL**: `/` (or your domain)
   - **Application startup file**: `passenger_wsgi.py`
   - Click **Create**

3. **If app already exists:**
   - Click **Edit**
   - Verify startup file is `passenger_wsgi.py`
   - Update if needed

## Step 3: Install Dependencies

In cPanel Python App terminal (or SSH):
```bash
cd /home/shadhinc/newssearch
pip install -r requirements.txt
```

## Step 4: Set Environment Variables

In Python App settings, add:
- `DJANGO_SETTINGS_MODULE=web.settings` (usually automatic)
- `DEBUG=False`
- `ALLOWED_HOSTS=shadhin247.com,www.shadhin247.com`

## Step 5: Run Migrations

```bash
python manage.py migrate
```

## Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This creates the `staticfiles/` directory with all static files.

## Step 7: Set File Permissions

```bash
chmod 755 passenger_wsgi.py
chmod 755 manage.py
chmod 664 db.sqlite3
chmod -R 755 news/
chmod -R 755 web/
```

## Step 8: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Step 9: Restart Python App

In cPanel Python App, click **Restart**

## Step 10: Test

1. Visit: `http://shadhin247.com/`
   - Should show Django app (not 503 error)

2. Test static files: `http://shadhin247.com/static/scripts/search.js`
   - Should load JavaScript file

## Troubleshooting

### Still Getting 503?

1. **Check Python App Status:**
   - Go to cPanel → Software → Setup Python App
   - Verify app is running (green status)
   - Check error logs

2. **Check Error Logs:**
   - cPanel → Metrics → Errors
   - Look for Python/Django errors
   - Check `passenger_error.log` in project directory

3. **Test Django Manually:**
   ```bash
   cd /home/shadhinc/newssearch
   python manage.py check
   python manage.py runserver 0.0.0.0:8000
   ```

4. **Verify Dependencies:**
   ```bash
   pip list
   # Should show Django, feedparser, requests, beautifulsoup4, pandas
   ```

5. **Check File Permissions:**
   ```bash
   ls -la passenger_wsgi.py
   # Should show -rwxr-xr-x (executable)
   ```

### Node.js Error?

If you see Node.js errors, the server is still configured for Node.js:
- Contact hosting provider to disable Node.js for your domain
- Or remove any Node.js app configuration in cPanel

### Static Files Not Loading?

1. Run `python manage.py collectstatic --noinput`
2. Check `staticfiles/` directory exists
3. Verify `.htaccess` is in project root
4. Check file permissions: `chmod -R 755 staticfiles/`

## Quick Checklist

- [ ] `passenger_wsgi.py` uploaded and executable
- [ ] `.htaccess` uploaded to project root
- [ ] Python app created in cPanel
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Environment variables set
- [ ] Python app restarted
- [ ] Tested homepage and static files
