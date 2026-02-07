from datetime import timedelta, datetime, timezone
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase_client import supabase

app = FastAPI()

@app.post("/create")
async def create_rose(
    to_name: str = Form(...),
    message: str = Form(...)
):
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    res = supabase.table("roses").insert({
        "to_name": to_name,
        "message": message,
        "expires_at": expires_at.isoformat()
    }).execute()

    rose_id = res.data[0]["id"]
    return RedirectResponse(url=f"/r/{rose_id}", status_code=303)

@app.get("/r/{rose_id}", response_class=HTMLResponse)
async def view_rose(rose_id: str):
    res = supabase.table("roses") \
        .select("to_name,message,expires_at") \
        .eq("id", rose_id) \
        .execute()

    if not res.data:
        return not_found_page()

    rose = res.data[0]
    expires_at = datetime.fromisoformat(rose["expires_at"])

    if datetime.now(timezone.utc) > expires_at:
        return expired_page()

    return rose_page(rose["to_name"], rose["message"])

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌹 Rose Day - Send Love That Lasts</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #ff6b9d 0%, #c06c84 50%, #f67280 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                position: relative;
                overflow-x: hidden;
            }
            
            .rose-float {
                position: absolute;
                font-size: 30px;
                opacity: 0.2;
                animation: float 10s infinite ease-in-out;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-30px) rotate(10deg); }
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                padding: 50px 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 550px;
                width: 100%;
                animation: slideIn 0.8s ease-out;
                backdrop-filter: blur(10px);
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            h1 {
                font-family: 'Playfair Display', serif;
                color: #c2185b;
                font-size: 2.5em;
                margin-bottom: 10px;
                text-align: center;
                animation: fadeIn 1s ease-out 0.3s both;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .subtitle {
                text-align: center;
                color: #666;
                font-size: 0.95em;
                margin-bottom: 35px;
                font-weight: 300;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            label {
                display: block;
                color: #c2185b;
                font-weight: 600;
                margin-bottom: 8px;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            input, textarea {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #f8bbd0;
                border-radius: 15px;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                transition: all 0.3s ease;
                background: #fff;
            }
            
            input:focus, textarea:focus {
                outline: none;
                border-color: #c2185b;
                box-shadow: 0 0 0 4px rgba(194, 24, 91, 0.1);
                transform: translateY(-2px);
            }
            
            textarea {
                resize: vertical;
                min-height: 120px;
                line-height: 1.6;
            }
            
            .char-count {
                text-align: right;
                font-size: 0.8em;
                color: #999;
                margin-top: 5px;
            }
            
            button {
                width: 100%;
                padding: 18px;
                background: linear-gradient(135deg, #e91e63 0%, #c2185b 100%);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                font-family: 'Poppins', sans-serif;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 10px 25px rgba(194, 24, 91, 0.3);
            }
            
            button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(194, 24, 91, 0.4);
            }
            
            button:active {
                transform: translateY(-1px);
            }
            
            .info {
                text-align: center;
                margin-top: 25px;
                color: #666;
                font-size: 0.85em;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            
            .info::before {
                content: "⏱️";
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 35px 25px;
                }
                
                h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="rose-float" style="top: 10%; left: 10%;">🌹</div>
        <div class="rose-float" style="top: 60%; right: 15%; animation-delay: -3s;">🌹</div>
        <div class="rose-float" style="top: 80%; left: 20%; animation-delay: -6s;">🌹</div>
        <div class="rose-float" style="top: 30%; right: 10%; animation-delay: -9s;">💝</div>
        
        <div class="container">
            <h1>🌹 Send a Rose</h1>
            <p class="subtitle">A beautiful gesture that blooms for 24 hours</p>
            
            <form method="post" action="/create" id="roseForm">
                <div class="form-group">
                    <label for="to_name">For</label>
                    <input 
                        type="text" 
                        id="to_name" 
                        name="to_name" 
                        placeholder="Enter their name..." 
                        required 
                        maxlength="100"
                    />
                </div>
                
                <div class="form-group">
                    <label for="message">Your Message</label>
                    <textarea 
                        id="message" 
                        name="message" 
                        placeholder="Express your feelings..." 
                        required 
                        maxlength="500"
                    ></textarea>
                    <div class="char-count">
                        <span id="charCount">0</span>/500 characters
                    </div>
                </div>
                
                <button type="submit">🌹 Create Rose</button>
            </form>
            
            <div class="info">
                Your rose will bloom for 24 hours
            </div>
        </div>
        
        <script>
            const textarea = document.getElementById('message');
            const charCount = document.getElementById('charCount');
            
            textarea.addEventListener('input', function() {
                charCount.textContent = this.value.length;
            });
        </script>
    </body>
    </html>
    """

def rose_page(name, message):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌹 A Rose for {name}</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #c2185b 0%, #e91e63 50%, #f06292 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                position: relative;
                overflow: hidden;
            }}
            
            /* Animated gradient background */
            body::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, 
                    rgba(194, 24, 91, 0.8) 0%, 
                    rgba(233, 30, 99, 0.8) 25%,
                    rgba(240, 98, 146, 0.8) 50%,
                    rgba(233, 30, 99, 0.8) 75%,
                    rgba(194, 24, 91, 0.8) 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
                z-index: 0;
            }}
            
            @keyframes gradientShift {{
                0%, 100% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
            }}
            
            /* Floating particles */
            .particles {{
                position: absolute;
                width: 100%;
                height: 100%;
                overflow: hidden;
                pointer-events: none;
                z-index: 1;
            }}
            
            .particle {{
                position: absolute;
                width: 8px;
                height: 8px;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.8), rgba(255, 192, 203, 0.3));
                border-radius: 50%;
                animation: floatUp linear infinite;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            }}
            
            @keyframes floatUp {{
                0% {{
                    transform: translateY(100vh) scale(0);
                    opacity: 0;
                }}
                10% {{
                    opacity: 1;
                }}
                90% {{
                    opacity: 1;
                }}
                100% {{
                    transform: translateY(-100px) scale(1);
                    opacity: 0;
                }}
            }}
            
            /* Falling petals with realistic motion */
            .petals {{
                position: absolute;
                width: 100%;
                height: 100%;
                overflow: hidden;
                pointer-events: none;
                z-index: 1;
            }}
            
            .petal {{
                position: absolute;
                width: 15px;
                height: 15px;
                background: linear-gradient(135deg, rgba(255, 182, 193, 0.9), rgba(255, 105, 180, 0.7));
                border-radius: 50% 0 50% 0;
                animation: fall linear infinite;
                filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
            }}
            
            @keyframes fall {{
                0% {{
                    transform: translateY(-10vh) rotate(0deg);
                    opacity: 1;
                }}
                100% {{
                    transform: translateY(110vh) rotate(720deg) translateX(100px);
                    opacity: 0.3;
                }}
            }}
            
            /* Main container with stunning entrance */
            .container {{
                background: rgba(255, 255, 255, 0.98);
                border-radius: 30px;
                padding: 60px 50px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4),
                            0 0 100px rgba(233, 30, 99, 0.3);
                max-width: 650px;
                width: 100%;
                text-align: center;
                animation: bloom 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                backdrop-filter: blur(10px);
                position: relative;
                z-index: 10;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            
            @keyframes bloom {{
                0% {{
                    opacity: 0;
                    transform: scale(0.1) rotate(-15deg);
                    filter: blur(10px);
                }}
                50% {{
                    transform: scale(1.1) rotate(5deg);
                }}
                100% {{
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                    filter: blur(0);
                }}
            }}
            
            /* Animated 3D Rose */
            .rose-container {{
                position: relative;
                display: inline-block;
                animation: roseEntrance 2s ease-out;
            }}
            
            @keyframes roseEntrance {{
                0% {{
                    transform: translateY(50px) scale(0);
                    opacity: 0;
                }}
                60% {{
                    transform: translateY(-10px) scale(1.2);
                }}
                100% {{
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }}
            }}
            
            .rose-icon {{
                font-size: 6em;
                display: inline-block;
                animation: roseFloat 3s ease-in-out infinite;
                filter: drop-shadow(0 10px 30px rgba(233, 30, 99, 0.5));
                position: relative;
            }}
            
            @keyframes roseFloat {{
                0%, 100% {{
                    transform: translateY(0) rotate(-5deg);
                }}
                50% {{
                    transform: translateY(-20px) rotate(5deg);
                }}
            }}
            
            /* Sparkle effect around rose */
            .rose-container::before,
            .rose-container::after {{
                content: '✨';
                position: absolute;
                font-size: 1.5em;
                animation: sparkle 2s ease-in-out infinite;
            }}
            
            .rose-container::before {{
                top: 0;
                left: -20px;
                animation-delay: 0.5s;
            }}
            
            .rose-container::after {{
                top: 0;
                right: -20px;
                animation-delay: 1s;
            }}
            
            @keyframes sparkle {{
                0%, 100% {{
                    opacity: 0;
                    transform: scale(0) rotate(0deg);
                }}
                50% {{
                    opacity: 1;
                    transform: scale(1) rotate(180deg);
                }}
            }}
            
            /* Heart particles emanating from rose */
            .hearts {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                pointer-events: none;
            }}
            
            .heart {{
                position: absolute;
                font-size: 1.2em;
                animation: heartFloat 3s ease-out infinite;
                opacity: 0;
            }}
            
            @keyframes heartFloat {{
                0% {{
                    transform: translate(0, 0) scale(0);
                    opacity: 0;
                }}
                20% {{
                    opacity: 1;
                }}
                100% {{
                    transform: translate(var(--tx), var(--ty)) scale(1);
                    opacity: 0;
                }}
            }}
            
            h1 {{
                font-family: 'Playfair Display', serif;
                color: #c2185b;
                font-size: 2.5em;
                margin: 20px 0 30px;
                animation: fadeInDown 1s ease-out 0.5s both;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                position: relative;
            }}
            
            /* Underline animation */
            h1::after {{
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 3px;
                background: linear-gradient(90deg, #c2185b, #e91e63);
                animation: expandLine 1s ease-out 1s forwards;
                border-radius: 2px;
            }}
            
            @keyframes expandLine {{
                to {{ width: 60%; }}
            }}
            
            @keyframes fadeInDown {{
                from {{
                    opacity: 0;
                    transform: translateY(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .message-box {{
                background: linear-gradient(135deg, #fff5f8 0%, #ffe5ec 100%);
                border-left: 4px solid #e91e63;
                padding: 30px;
                border-radius: 20px;
                margin: 30px 0;
                animation: fadeInScale 1s ease-out 0.8s both;
                box-shadow: 0 5px 20px rgba(233, 30, 99, 0.15);
                position: relative;
                overflow: hidden;
            }}
            
            /* Shimmer effect on message box */
            .message-box::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255, 255, 255, 0.5), 
                    transparent);
                animation: shimmer 3s ease-in-out infinite;
            }}
            
            @keyframes shimmer {{
                0%, 100% {{ left: -100%; }}
                50% {{ left: 100%; }}
            }}
            
            @keyframes fadeInScale {{
                from {{
                    opacity: 0;
                    transform: scale(0.8);
                }}
                to {{
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
            
            .message {{
                font-size: 1.3em;
                line-height: 1.8;
                color: #333;
                font-weight: 300;
                font-style: italic;
                position: relative;
                z-index: 1;
            }}
            
            .actions {{
                display: flex;
                gap: 15px;
                margin-top: 35px;
                flex-wrap: wrap;
                animation: fadeIn 1s ease-out 1.2s both;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            .btn {{
                flex: 1;
                min-width: 160px;
                padding: 15px 25px;
                border-radius: 15px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                text-decoration: none;
                display: inline-block;
                font-family: 'Poppins', sans-serif;
                position: relative;
                overflow: hidden;
            }}
            
            .btn::before {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }}
            
            .btn:hover::before {{
                width: 300px;
                height: 300px;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #e91e63 0%, #c2185b 100%);
                color: white;
                border: none;
                box-shadow: 0 10px 25px rgba(194, 24, 91, 0.3);
            }}
            
            .btn-primary:hover {{
                transform: translateY(-5px) scale(1.05);
                box-shadow: 0 20px 40px rgba(194, 24, 91, 0.4);
            }}
            
            .btn-secondary {{
                background: white;
                color: #c2185b;
                border: 2px solid #c2185b;
            }}
            
            .btn-secondary:hover {{
                background: #c2185b;
                color: white;
                transform: translateY(-5px) scale(1.05);
                box-shadow: 0 15px 30px rgba(194, 24, 91, 0.3);
            }}
            
            .share-link {{
                margin-top: 25px;
                padding: 15px;
                background: rgba(194, 24, 91, 0.05);
                border-radius: 10px;
                font-size: 0.85em;
                color: #666;
                animation: fadeIn 1s ease-out 1s both;
            }}
            
            .link-box {{
                display: flex;
                gap: 10px;
                margin-top: 10px;
                align-items: center;
            }}
            
            .link-input {{
                flex: 1;
                padding: 10px 15px;
                border: 2px solid #f8bbd0;
                border-radius: 10px;
                font-family: monospace;
                font-size: 0.9em;
                background: white;
                transition: all 0.3s ease;
            }}
            
            .link-input:focus {{
                outline: none;
                border-color: #e91e63;
                box-shadow: 0 0 10px rgba(233, 30, 99, 0.2);
            }}
            
            .copy-btn {{
                padding: 10px 20px;
                background: #c2185b;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                position: relative;
            }}
            
            .copy-btn:hover {{
                background: #e91e63;
                transform: scale(1.1);
            }}
            
            .copy-btn:active {{
                transform: scale(0.95);
            }}
            
            .copied {{
                background: #4caf50 !important;
                animation: success 0.5s ease;
            }}
            
            @keyframes success {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.2); }}
            }}
            
            @media (max-width: 600px) {{
                .container {{
                    padding: 40px 30px;
                }}
                
                h1 {{
                    font-size: 1.8em;
                }}
                
                .rose-icon {{
                    font-size: 4em;
                }}
                
                .message {{
                    font-size: 1.1em;
                }}
                
                .actions {{
                    flex-direction: column;
                }}
                
                .btn {{
                    min-width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="particles" id="particles"></div>
        <div class="petals" id="petals"></div>
        
        <div class="container">
            <div class="rose-container">
                <div class="hearts" id="hearts"></div>
                <div class="rose-icon">🌹</div>
            </div>
            <h1>A Rose for {name}</h1>
            
            <div class="message-box">
                <div class="message">"{message}"</div>
            </div>
            
            <div class="share-link">
                <p><strong>Share this rose:</strong></p>
                <div class="link-box">
                    <input 
                        type="text" 
                        class="link-input" 
                        id="shareLink" 
                        value="" 
                        readonly 
                    />
                    <button class="copy-btn" onclick="copyLink()">Copy</button>
                </div>
            </div>
            
            <div class="actions">
                <a href="/" class="btn btn-primary">🌹 Send Your Own Rose</a>
                <a href="https://www.google.com/search?q=rose+day+quotes" target="_blank" class="btn btn-secondary">Get Inspired</a>
            </div>
        </div>
        
        <script>
            // Set share link
            document.getElementById('shareLink').value = window.location.href;
            
            // Copy link functionality
            function copyLink() {{
                const input = document.getElementById('shareLink');
                const btn = event.target;
                
                input.select();
                navigator.clipboard.writeText(input.value).then(() => {{
                    btn.textContent = '✓ Copied!';
                    btn.classList.add('copied');
                    
                    setTimeout(() => {{
                        btn.textContent = 'Copy';
                        btn.classList.remove('copied');
                    }}, 2000);
                }}).catch(() => {{
                    // Fallback for older browsers
                    document.execCommand('copy');
                    btn.textContent = '✓ Copied!';
                    btn.classList.add('copied');
                    
                    setTimeout(() => {{
                        btn.textContent = 'Copy';
                        btn.classList.remove('copied');
                    }}, 2000);
                }});
            }}
            
            // Create falling petals with variation
            function createPetal() {{
                const petal = document.createElement('div');
                petal.classList.add('petal');
                petal.style.left = Math.random() * 100 + '%';
                petal.style.animationDuration = (Math.random() * 4 + 6) + 's';
                petal.style.opacity = Math.random() * 0.6 + 0.4;
                petal.style.animationDelay = Math.random() * 2 + 's';
                petal.style.width = (Math.random() * 10 + 10) + 'px';
                petal.style.height = petal.style.width;
                document.getElementById('petals').appendChild(petal);
                
                setTimeout(() => petal.remove(), 10000);
            }}
            
            // Create floating particles
            function createParticle() {{
                const particle = document.createElement('div');
                particle.classList.add('particle');
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDuration = (Math.random() * 5 + 8) + 's';
                particle.style.animationDelay = Math.random() * 3 + 's';
                document.getElementById('particles').appendChild(particle);
                
                setTimeout(() => particle.remove(), 13000);
            }}
            
            // Create heart animations
            function createHeart() {{
                const heart = document.createElement('div');
                heart.classList.add('heart');
                heart.textContent = '💕';
                
                const angle = Math.random() * Math.PI * 2;
                const distance = 100 + Math.random() * 100;
                const tx = Math.cos(angle) * distance;
                const ty = Math.sin(angle) * distance;
                
                heart.style.setProperty('--tx', tx + 'px');
                heart.style.setProperty('--ty', ty + 'px');
                heart.style.animationDelay = Math.random() * 2 + 's';
                
                document.getElementById('hearts').appendChild(heart);
                
                setTimeout(() => heart.remove(), 3000);
            }}
            
            // Generate effects periodically
            setInterval(createPetal, 400);
            setInterval(createParticle, 800);
            setInterval(createHeart, 1500);
            
            // Initial burst
            for(let i = 0; i < 15; i++) {{
                setTimeout(createPetal, i * 150);
            }}
            for(let i = 0; i < 8; i++) {{
                setTimeout(createParticle, i * 300);
            }}
            for(let i = 0; i < 5; i++) {{
                setTimeout(createHeart, i * 500);
            }}
        </script>
    </body>
    </html>
    """

def expired_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🥀 Rose Has Faded</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #9e9e9e 0%, #757575 50%, #616161 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                padding: 60px 50px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
                max-width: 550px;
                width: 100%;
                text-align: center;
                animation: fadeIn 1s ease-out;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .icon {
                font-size: 6em;
                opacity: 0.7;
                animation: droop 3s ease-in-out infinite;
            }
            
            @keyframes droop {
                0%, 100% {
                    transform: rotate(0deg);
                }
                50% {
                    transform: rotate(-10deg);
                }
            }
            
            h1 {
                font-family: 'Playfair Display', serif;
                color: #666;
                font-size: 2.3em;
                margin: 25px 0 20px;
            }
            
            p {
                font-size: 1.1em;
                color: #777;
                line-height: 1.8;
                margin-bottom: 35px;
                font-weight: 300;
            }
            
            .quote {
                background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
                font-style: italic;
                color: #555;
            }
            
            .btn {
                display: inline-block;
                padding: 18px 40px;
                background: linear-gradient(135deg, #e91e63 0%, #c2185b 100%);
                color: white;
                text-decoration: none;
                border-radius: 15px;
                font-weight: 600;
                font-size: 1.1em;
                transition: all 0.3s ease;
                box-shadow: 0 10px 25px rgba(194, 24, 91, 0.3);
            }
            
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(194, 24, 91, 0.4);
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 40px 30px;
                }
                
                h1 {
                    font-size: 1.8em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🥀</div>
            <h1>This Rose Has Faded</h1>
            <p>The beauty of a moment is that it doesn't last forever.</p>
            
            <div class="quote">
                "Some gestures are meant to be felt in time,<br>
                cherished in memory, and renewed with love."
            </div>
            
            <a href="/" class="btn">🌹 Create a Fresh Rose</a>
        </div>
    </body>
    </html>
    """

def not_found_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌹 Rose Not Found</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #5d4157 0%, #a8caba 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                padding: 60px 50px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
                max-width: 550px;
                width: 100%;
                text-align: center;
                animation: fadeIn 1s ease-out;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .icon {
                font-size: 6em;
                opacity: 0.8;
                animation: sway 2s ease-in-out infinite;
            }
            
            @keyframes sway {
                0%, 100% {
                    transform: rotate(-5deg);
                }
                50% {
                    transform: rotate(5deg);
                }
            }
            
            h1 {
                font-family: 'Playfair Display', serif;
                color: #5d4157;
                font-size: 2.3em;
                margin: 25px 0 20px;
            }
            
            p {
                font-size: 1.1em;
                color: #777;
                line-height: 1.8;
                margin-bottom: 35px;
                font-weight: 300;
            }
            
            .btn {
                display: inline-block;
                padding: 18px 40px;
                background: linear-gradient(135deg, #e91e63 0%, #c2185b 100%);
                color: white;
                text-decoration: none;
                border-radius: 15px;
                font-weight: 600;
                font-size: 1.1em;
                transition: all 0.3s ease;
                box-shadow: 0 10px 25px rgba(194, 24, 91, 0.3);
            }
            
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(194, 24, 91, 0.4);
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 40px 30px;
                }
                
                h1 {
                    font-size: 1.8em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🔍</div>
            <h1>Rose Not Found</h1>
            <p>This rose doesn't exist or the link is incorrect.<br>
            Perhaps it was never sent, or it bloomed and faded away.</p>
            
            <a href="/" class="btn">🌹 Send a Rose</a>
        </div>
    </body>
    </html>
    """

