# 🌹 Rose Day - Send Love That Blooms

A beautiful, romantic web application for sending virtual roses with heartfelt messages. Each rose blooms for exactly 24 hours, making your gesture special and timely.

## ✨ Features

- **Beautiful UI**: Modern, gradient-based design with smooth animations
- **Falling Petals**: Animated petals that fall on the rose view page
- **Character Counter**: Real-time feedback while writing your message
- **Share Link**: Easy copy-to-clipboard functionality for sharing roses
- **Time-Limited**: Roses expire after 24 hours, making each gesture meaningful
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Elegant Animations**: Smooth transitions and delightful micro-interactions

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A Supabase account (for database)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd C:\Personal\rose-day
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**
   
   Make sure your `.env` file contains:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

4. **Create the database table in Supabase**
   
   Run this SQL in your Supabase SQL Editor:
   ```sql
   CREATE TABLE roses (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     to_name VARCHAR(100) NOT NULL,
     message TEXT NOT NULL,
     expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

### Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at:
- **Local**: http://127.0.0.1:8000
- **Network**: http://0.0.0.0:8000

## 📖 How to Use

1. **Create a Rose**
   - Visit the homepage
   - Enter the recipient's name
   - Write your heartfelt message (up to 500 characters)
   - Click "Create Rose"

2. **Share the Rose**
   - Copy the generated link
   - Share it with your special someone
   - They can view the rose for 24 hours

3. **View a Rose**
   - Open the shared link
   - Enjoy the beautiful animation and message
   - Share your own rose!

## 🎨 Design Highlights

- **Color Palette**: Romantic pinks and reds with gradient backgrounds
- **Typography**: Playfair Display for headings, Poppins for body text
- **Animations**: 
  - Bloom effect when viewing a rose
  - Floating roses on the homepage
  - Falling petals on the rose view page
  - Smooth hover effects on all interactive elements
- **Responsive**: Mobile-first design that scales beautifully

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with gradients and animations

## 📝 API Endpoints

- `GET /` - Homepage with rose creation form
- `POST /create` - Create a new rose
- `GET /r/{rose_id}` - View a specific rose

## 🔒 Security Notes

- Keep your `.env` file private and never commit it to version control
- The SUPABASE_KEY shown is an anon key (safe for client-side use)
- Consider adding rate limiting for production use

## 🌟 Future Enhancements

- [ ] Add countdown timer showing time until rose expires
- [ ] Allow users to choose rose colors
- [ ] Add background music option
- [ ] Enable custom expiration times
- [ ] Add analytics to see how many times a rose was viewed
- [ ] Social media preview images (Open Graph tags)

## 📄 License

This project is open source and available for personal use.

## 💝 Perfect For

- Rose Day celebrations
- Valentine's Day
- Anniversaries
- Birthday wishes
- Just because moments
- Any day you want to make someone smile

---

Made with ❤️ for those who believe in the power of small gestures.
