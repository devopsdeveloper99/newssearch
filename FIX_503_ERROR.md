# Fix 503 Service Unavailable Error

## Problem
Getting 503 error when calling `callSearch()` function. This means Django application isn't running on the server.

## Root Cause
The Django/Python application is not properly configured or running on your cPanel server.

## Solution Steps

### Step 1: Verify Python App is Running

1. **Go to cPanel → Software → Setup Python App**
2. **Check if your Python app exists and is running:**
   - Should show green status (running)
   - If red/stopped, click **Start** or **Restart**

### Step 2: Check Application Configuration

In Python App settings, verify:
- **Application root**: `/home/shadhinc/newssearch`
- **Startup file**: `passenger_wsgi.py`
- **Python version**: 3.9 (or 3.8+)

### Step 3: Check Error Logs

1. **Go to cPanel → Metrics → Errors**
2. **Look for recent errors** related to Python/Django
3. **Check for:**
   - Import errors
   - Module not found errors
   - Permission errors
   - Configuration errors

### Step 4: Test Django Manually (SSH)

If you have SSH access:

```bash
cd /home/shadhinc/newssearch

# Test Django configuration
python manage.py check

# Test if Django can start
python manage.py runserver 0.0.0.0:8000
```

If this works, Django is fine - the issue is with Passenger/WSGI configuration.

### Step 5: Verify Files Exist

Check these files exist on server:
```bash
ls -la /home/shadhinc/newssearch/passenger_wsgi.py
ls -la /home/shadhinc/newssearch/.htaccess
ls -la /home/shadhinc/newssearch/manage.py
```

### Step 6: Check File Permissions

```bash
chmod 755 /home/shadhinc/newssearch/passenger_wsgi.py
chmod 755 /home/shadhinc/newssearch/manage.py
chmod -R 755 /home/shadhinc/newssearch/news/
chmod -R 755 /home/shadhinc/newssearch/web/
```

### Step 7: Verify Dependencies

```bash
pip list | grep -i django
pip list | grep -i feedparser
pip list | grep -i requests
pip list | grep -i beautifulsoup4
pip list | grep -i pandas
```

All should be installed. If not:
```bash
pip install -r requirements.txt
```

### Step 8: Check Environment Variables

In Python App settings, verify:
- `DJANGO_SETTINGS_MODULE=web.settings`
- `DEBUG=False` (or `True` for testing)
- `ALLOWED_HOSTS=shadhin247.com,www.shadhin247.com`

### Step 9: Restart Python App

After making changes:
1. **Stop** the Python app
2. **Start** it again
3. Wait 30 seconds for it to fully start
4. Test the website

## Common Issues

### Issue 1: Node.js Still Configured
If you see Node.js errors in logs:
- Contact hosting to disable Node.js for your domain
- Or remove Node.js app configuration in cPanel

### Issue 2: Import Errors
If Django can't import modules:
- Check `INSTALLED_APPS` in `settings.py`
- Verify all Python packages are installed
- Check Python path in `passenger_wsgi.py`

### Issue 3: Database Errors
```bash
python manage.py migrate
```

### Issue 4: Static Files Errors
```bash
python manage.py collectstatic --noinput
```

## Quick Test

After fixing, test these URLs:

1. **Homepage**: `http://shadhin247.com/`
   - Should show search page (not 503)

2. **Static file**: `http://shadhin247.com/static/scripts/search.js`
   - Should show JavaScript code (not 503)

3. **Search endpoint**: Use browser console:
   ```javascript
   fetch('/search/', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
     },
     body: JSON.stringify({query: 'test'})
   }).then(r => r.json()).then(console.log)
   ```
   - Should return JSON (not 503 HTML)

## Still Getting 503?

1. **Contact hosting support** - Server-level configuration may be needed
2. **Check LiteSpeed/PHP error logs** - May reveal the issue
3. **Try enabling DEBUG=True temporarily** - To see actual error messages
4. **Check if Passenger is installed** - Required for WSGI applications

## Files Updated

- ✅ `search.js` - Removed debug code, improved error handling
- ✅ `search.html` - Added CSRF token meta tag
- ✅ Error messages now more user-friendly
