# Quick Start Guide

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Make sure your `.env` file exists with:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Set Up Database
Go to your Supabase SQL Editor and run:
```sql
CREATE TABLE IF NOT EXISTS roses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  to_name VARCHAR(100) NOT NULL,
  message TEXT NOT NULL,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Or run the complete `setup.sql` file.

### 4. Run the Application
```bash
uvicorn main:app --reload
```

Visit: http://127.0.0.1:8000

## Deployment Options

### Option 1: Vercel (Recommended for FastAPI)
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```
3. Deploy: `vercel --prod`

### Option 2: Railway
1. Connect your GitHub repo
2. Add environment variables from `.env`
3. Railway auto-detects Python and deploys

### Option 3: Heroku
1. Create `Procfile`:
```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
```
2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option 4: DigitalOcean App Platform
1. Connect your GitHub repo
2. Set environment variables
3. Deploy with one click

## Testing Locally

1. **Create a Rose**: Go to http://127.0.0.1:8000
2. **Fill the form** with a name and message
3. **Submit** and you'll be redirected to the rose page
4. **Copy the link** and share it!

## Customization Ideas

- Change color schemes in the CSS
- Modify expiration time (currently 24 hours)
- Add more features like custom backgrounds
- Enable analytics
- Add email notifications

## Troubleshooting

### "Connection refused" error
- Make sure Supabase credentials are correct
- Check if `.env` file is in the project root

### "Table doesn't exist" error
- Run the `setup.sql` in Supabase SQL Editor

### Import errors
- Activate virtual environment: `.venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`

## Support

For issues or questions, check:
- FastAPI docs: https://fastapi.tiangolo.com
- Supabase docs: https://supabase.com/docs
- Python docs: https://docs.python.org

---

Enjoy spreading love! 🌹
