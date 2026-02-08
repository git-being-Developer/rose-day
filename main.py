from datetime import timedelta, datetime, timezone
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from supabase_client import supabase

app = FastAPI()

# Mount static files for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        <title>💍 Propose Day – Ask With Artistry</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Poppins', sans-serif;
                background: radial-gradient(circle at 20% 20%, #fff4f4 0%, #ffe4d9 35%, #f8dfe5 60%, #e7d2ff 100%);
                min-height: 100vh;
                padding: 30px 20px 60px;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                overflow-x: hidden;
            }
            body::before {
                content: '';
                position: absolute;
                inset: 0;
                background: url('https://www.transparenttextures.com/patterns/asfalt-dark.png');
                opacity: 0.15;
                mix-blend-mode: soft-light;
            }
            .floating-rings span {
                position: absolute;
                border: 2px solid rgba(255, 215, 138, 0.7);
                border-radius: 50%;
                animation: drift 18s linear infinite;
                opacity: 0.4;
            }
            .floating-rings span:nth-child(1) { width: 160px; height: 160px; top: 5%; left: 8%; animation-delay: 0s; }
            .floating-rings span:nth-child(2) { width: 120px; height: 120px; bottom: 10%; right: 15%; animation-delay: -4s; }
            .floating-rings span:nth-child(3) { width: 90px; height: 90px; top: 15%; right: 25%; animation-delay: -8s; }
            @keyframes drift {
                0% { transform: rotate(0deg) scale(1); }
                50% { transform: rotate(180deg) scale(1.1); }
                100% { transform: rotate(360deg) scale(1); }
            }
            .main-wrapper {
                position: relative;
                z-index: 2;
                display: flex;
                gap: 30px;
                width: 100%;
                max-width: 1200px;
                flex-wrap: wrap;
                justify-content: center;
            }
            .hero-card {
                flex: 1;
                min-width: 320px;
                max-width: 450px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 28px;
                padding: 40px;
                box-shadow: 0 25px 60px rgba(183, 136, 197, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.6);
                backdrop-filter: blur(12px);
            }
            .eyebrow {
                text-transform: uppercase;
                letter-spacing: 2px;
                font-size: 0.75rem;
                color: #c39a5b;
                font-weight: 600;
                margin-bottom: 12px;
            }
            .hero-card h1 {
                font-family: 'Playfair Display', serif;
                font-size: 2.7rem;
                line-height: 1.2;
                color: #3c2b39;
                margin-bottom: 18px;
            }
            .hero-card h1 span {
                color: #c38f2f;
            }
            .hero-text {
                font-size: 1rem;
                color: #6c5a6b;
                margin-bottom: 25px;
            }
            .highlights {
                list-style: none;
                display: grid;
                gap: 15px;
            }
            .highlights li {
                display: flex;
                gap: 12px;
                align-items: flex-start;
                font-size: 0.95rem;
                color: #4d3a45;
            }
            .highlights li span {
                font-size: 1.1rem;
            }
            .container {
                flex: 1;
                min-width: 320px;
                max-width: 520px;
                background: rgba(255, 255, 255, 0.96);
                border-radius: 30px;
                padding: 45px 40px;
                box-shadow: 0 30px 70px rgba(121, 92, 158, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(15px);
            }
            h2 {
                font-family: 'Playfair Display', serif;
                font-size: 2rem;
                color: #3a2740;
                margin-bottom: 10px;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                color: #7c6a7f;
                font-size: 0.95rem;
                margin-bottom: 30px;
            }
            .form-group { margin-bottom: 22px; }
            label {
                display: block;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #b38244;
                font-weight: 600;
                margin-bottom: 6px;
            }
            input, textarea {
                width: 100%;
                padding: 15px 18px;
                border-radius: 18px;
                border: 2px solid rgba(195, 143, 47, 0.2);
                background: rgba(255, 255, 255, 0.95);
                font-size: 1rem;
                font-family: 'Poppins', sans-serif;
                transition: border 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus, textarea:focus {
                outline: none;
                border-color: #c38f2f;
                box-shadow: 0 0 0 4px rgba(195, 143, 47, 0.15);
            }
            textarea {
                resize: vertical;
                min-height: 140px;
                line-height: 1.6;
            }
            .char-count {
                text-align: right;
                font-size: 0.8rem;
                color: #9c8a9e;
                margin-top: 6px;
            }
            .tip-jar {
                margin: 35px 0 25px;
                text-align: center;
            }
            .jar-container {
                width: 180px;
                margin: 0 auto;
                position: relative;
            }
            .jar-lid {
                height: 12px;
                border-radius: 10px 10px 0 0;
                background: linear-gradient(120deg, #c38f2f, #f8d18b);
                box-shadow: 0 4px 10px rgba(195, 143, 47, 0.25);
            }
            .jar-lid::before {
                content: '';
                position: absolute;
                top: -6px;
                left: 50%;
                transform: translateX(-50%);
                width: 46px;
                height: 9px;
                border-radius: 12px;
                background: linear-gradient(120deg, #d9a544, #f8d693);
            }
            .jar-body {
                background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255, 247, 232, 0.95));
                border: 3px solid rgba(195, 143, 47, 0.35);
                border-top: none;
                border-radius: 0 0 22px 22px;
                padding: 20px 15px 35px;
                box-shadow: inset 0 4px 10px rgba(255, 255, 255, 0.6), inset 0 -4px 10px rgba(195, 143, 47, 0.15);
                position: relative;
            }
            .jar-body::before {
                content: '';
                position: absolute;
                top: 10px;
                left: 12%;
                width: 28%;
                height: 60%;
                border-radius: 18px;
                background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0));
            }
            .jar-label {
                border: 2px dashed rgba(195, 143, 47, 0.25);
                border-radius: 10px;
                padding: 8px;
                background: rgba(255,255,255,0.9);
                margin-bottom: 10px;
            }
            .tip-text {
                font-size: 0.7rem;
                color: #8a6740;
                font-weight: 600;
                line-height: 1.3;
            }
            .qr-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
            }
            .qr-code {
                width: 90px;
                border-radius: 10px;
                border: 2px solid rgba(195, 143, 47, 0.2);
                box-shadow: 0 6px 16px rgba(195, 143, 47, 0.25);
            }
            .upi-id {
                font-family: monospace;
                font-size: 0.7rem;
                color: #71502e;
                border: 1px solid rgba(195, 143, 47, 0.35);
                border-radius: 4px;
                padding: 4px 8px;
                background: rgba(255,255,255,0.8);
            }
            .coins {
                position: absolute;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 4px;
                opacity: 0.6;
            }
            .coin { animation: coinDrop 2s ease-in-out infinite; }
            .coin:nth-child(2) { animation-delay: 0.3s; }
            .coin:nth-child(3) { animation-delay: 0.6s; }
            @keyframes coinDrop {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            button {
                width: 100%;
                padding: 18px;
                border: none;
                border-radius: 18px;
                background: linear-gradient(120deg, #f9d976, #f39f86);
                color: #3d2a2f;
                font-size: 1.05rem;
                font-weight: 600;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                cursor: pointer;
                box-shadow: 0 18px 35px rgba(243, 159, 134, 0.35);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }
            button:hover {
                transform: translateY(-4px);
                box-shadow: 0 22px 45px rgba(243, 159, 134, 0.45);
            }
            button:active { transform: translateY(-1px); }
            .info {
                margin-top: 20px;
                text-align: center;
                font-size: 0.85rem;
                color: #7b657a;
                display: flex;
                justify-content: center;
                gap: 8px;
            }
            .info::before { content: '⏳'; }
            @media (max-width: 960px) {
                .main-wrapper { flex-direction: column; align-items: stretch; }
            }
            @media (max-width: 540px) {
                body { padding: 20px 15px 50px; }
                .container, .hero-card { padding: 30px 25px; }
                .hero-card h1 { font-size: 2.1rem; }
            }
        </style>
    </head>
    <body>
        <div class="floating-rings">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="main-wrapper">
            <section class="hero-card">
                <p class="eyebrow">Propose Day • 24-hour keepsake</p>
                <h1>💍 Ask the question<br><span>with poetry</span></h1>
                <p class="hero-text">Pen your promise, let it live online for a full day, and send a link that feels as thoughtful as the moment.</p>
                <ul class="highlights">
                    <li><span>✨</span>Hand off a cinematic page with your words floating in soft gold glows.</li>
                    <li><span>🔐</span>Each proposal auto-expires in 24 hours for privacy and exclusivity.</li>
                    <li><span>🎁</span>Add a tip in the keepsake jar to keep the love-thon live all week.</li>
                </ul>
            </section>
            <div class="container">
                <h2>Craft Your Proposal</h2>
                <p class="subtitle">They open a bespoke page; you get the courage boost.</p>
                <form method="post" action="/create" id="proposalForm">
                    <div class="form-group">
                        <label for="to_name">Who is this for?</label>
                        <input type="text" id="to_name" name="to_name" placeholder="Their name..." required maxlength="100">
                    </div>
                    <div class="form-group">
                        <label for="message">Your promise</label>
                        <textarea id="message" name="message" placeholder="Tell them why forever starts now..." required maxlength="500"></textarea>
                        <div class="char-count"><span id="charCount">0</span>/500 characters</div>
                    </div>
                    <div class="tip-jar">
                        <div class="jar-container">
                            <div class="jar-lid"></div>
                            <div class="jar-body">
                                <div class="jar-label">
                                    <p class="tip-text">💝 Tip Jar<br>Fuel the servers & spread love all Propose Week.</p>
                                </div>
                                <div class="qr-container">
                                    <img src="/static/upi-qr.png" alt="UPI QR" class="qr-code" onerror="this.style.display='none'">
                                    <p class="upi-id">hrithik.raj.543@okhdfcbank</p>
                                </div>
                                <div class="coins">
                                    <span class="coin">🪙</span>
                                    <span class="coin">🪙</span>
                                    <span class="coin">🪙</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="submit">💌 Send the Proposal</button>
                </form>
                <div class="info">Your proposal stays live for exactly 24 hours.</div>
            </div>
        </div>
        <script>
            const textarea = document.getElementById('message');
            const charCount = document.getElementById('charCount');
            textarea.addEventListener('input', function () {
                charCount.textContent = this.value.length;
            });
        </script>
    </body>
    </html>
    """

def rose_page(name, message):
    return f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>💍 A Proposal for {name}</title>
        <link href=\"https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Poppins:wght@300;400;500;600&display=swap\" rel=\"stylesheet\">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                padding: 30px 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: radial-gradient(circle at top, #1d1a2e 0%, #2f2346 35%, #462c52 70%, #1c1a2b 100%);
                position: relative;
                overflow: hidden;
            }}
            body::before {{
                content: '';
                position: absolute;
                inset: 0;
                background: url('https://www.transparenttextures.com/patterns/gplay.png');
                opacity: 0.12;
            }}
            .aurora {{
                position: absolute;
                width: 120%;
                height: 120%;
                background: radial-gradient(circle at 20% 20%, rgba(255,220,177,0.25), transparent 55%),
                            radial-gradient(circle at 80% 30%, rgba(255,139,180,0.2), transparent 60%),
                            radial-gradient(circle at 60% 70%, rgba(131,109,255,0.25), transparent 60%);
                filter: blur(40px);
                animation: sway 20s ease-in-out infinite;
            }}
            @keyframes sway {{
                0%, 100% {{ transform: translate(-5%, -5%); }}
                50% {{ transform: translate(5%, 5%); }}
            }}
            .container {{
                position: relative;
                z-index: 1;
                width: 100%;
                max-width: 680px;
                background: rgba(16, 15, 28, 0.75);
                border-radius: 32px;
                padding: 55px 50px;
                border: 1px solid rgba(255,255,255,0.2);
                box-shadow: 0 35px 80px rgba(3, 3, 8, 0.6);
                backdrop-filter: blur(18px);
            }}
            .ring-icon {{
                font-size: 4.5rem;
                display: inline-block;
                margin-bottom: 15px;
                animation: float 3s ease-in-out infinite;
                filter: drop-shadow(0 15px 35px rgba(243, 186, 83, 0.35));
            }}
            @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
            h1 {{
                font-family: 'Playfair Display', serif;
                font-size: 2.6rem;
                color: #fef2dc;
                text-align: center;
                margin-bottom: 25px;
            }}
            h1 span {{ color: #f4c886; }}
            .message-box {{
                margin: 30px auto;
                padding: 35px;
                border-radius: 24px;
                background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255, 255, 255, 0.03));
                border: 1px solid rgba(255,255,255,0.15);
                color: #fdf7ef;
                font-size: 1.25rem;
                line-height: 1.8;
                font-style: italic;
                box-shadow: inset 0 0 40px rgba(255,255,255,0.07);
                position: relative;
                overflow: hidden;
            }}
            .message-box::before {{
                content: '';
                position: absolute;
                inset: -60% 0;
                background: linear-gradient(120deg, rgba(244,200,134,0.25), transparent 60%);
                animation: sheen 6s linear infinite;
            }}
            @keyframes sheen {{
                0% {{ transform: translateX(-60%); }}
                100% {{ transform: translateX(120%); }}
            }}
            .share-link {{
                background: rgba(255,255,255,0.08);
                border-radius: 18px;
                padding: 18px;
                border: 1px solid rgba(255,255,255,0.1);
                color: #d5cdef;
                margin-bottom: 30px;
            }}
            .link-box {{ display: flex; gap: 10px; margin-top: 12px; }}
            .link-input {{
                flex: 1;
                padding: 12px 14px;
                border-radius: 14px;
                border: 1px solid rgba(244,200,134,0.4);
                background: rgba(0,0,0,0.25);
                color: #ffe7ca;
                font-family: monospace;
                font-size: 0.95rem;
            }}
            .copy-btn {{
                padding: 12px 18px;
                border-radius: 14px;
                border: none;
                background: linear-gradient(135deg, #f9d976, #f39f86);
                color: #4b2d20;
                font-weight: 600;
                cursor: pointer;
            }}
            .tip-jar {{ text-align: center; margin: 25px 0 35px; }}
            .jar-container {{ width: 180px; margin: 0 auto; position: relative; }}
            .jar-lid {{
                height: 12px;
                border-radius: 10px 10px 0 0;
                background: linear-gradient(120deg, #c38f2f, #f8d18b);
                box-shadow: 0 4px 10px rgba(195, 143, 47, 0.25);
            }}
            .jar-lid::before {{
                content: '';
                position: absolute;
                top: -6px;
                left: 50%;
                transform: translateX(-50%);
                width: 46px;
                height: 9px;
                border-radius: 12px;
                background: linear-gradient(120deg, #d9a544, #f8d693);
            }}
            .jar-body {{
                background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(255, 247, 232, 0.12));
                border: 3px solid rgba(195, 143, 47, 0.35);
                border-top: none;
                border-radius: 0 0 22px 22px;
                padding: 20px 15px 35px;
                position: relative;
            }}
            .jar-label {{
                border: 2px dashed rgba(195, 143, 47, 0.35);
                border-radius: 10px;
                padding: 8px;
                background: rgba(22, 20, 34, 0.7);
                color: #f4d8a8;
                font-size: 0.7rem;
                line-height: 1.4;
                font-weight: 600;
            }}
            .qr-container {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
            .qr-code {{ width: 95px; border-radius: 10px; border: 2px solid rgba(195, 143, 47, 0.35); box-shadow: 0 12px 25px rgba(0,0,0,0.35); }}
            .upi-id {{ font-family: monospace; font-size: 0.75rem; color: #fceecd; background: rgba(0,0,0,0.35); padding: 4px 8px; border-radius: 4px; }}
            .coins {{ position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; opacity: 0.7; }}
            .coin {{ animation: coinDrop 2s ease-in-out infinite; }}
            .coin:nth-child(2) {{ animation-delay: 0.3s; }}
            .coin:nth-child(3) {{ animation-delay: 0.6s; }}
            @keyframes coinDrop {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
            .actions {{ display: flex; gap: 15px; flex-wrap: wrap; }}
            .btn {{
                flex: 1;
                min-width: 200px;
                padding: 16px 24px;
                border-radius: 16px;
                font-weight: 600;
                text-decoration: none;
                text-align: center;
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }}
            .btn-primary {{
                background: linear-gradient(120deg, #f9d976, #f39f86);
                color: #38231f;
                box-shadow: 0 20px 40px rgba(243, 159, 134, 0.35);
            }}
            .btn-secondary {{ border: 1px solid rgba(255,255,255,0.4); color: #fbead6; }}
            .btn:hover {{ transform: translateY(-4px); }}
            .note {{ margin-top: 25px; text-align: center; color: #d2c3f8; font-size: 0.9rem; }}
            @media (max-width: 600px) {{
                .container {{ padding: 40px 25px; }}
                h1 {{ font-size: 2rem; }}
                .actions {{ flex-direction: column; }}
            }}
        </style>
    </head>
    <body>
        <div class=\"aurora\"></div>
        <div class=\"container\">
            <div class=\"ring-icon\">💍</div>
            <h1>A Proposal for <span>{name}</span></h1>
            <div class=\"message-box\">
                “{message}”
            </div>
            <div class=\"share-link\">
                <p><strong>Share this private page:</strong></p>
                <div class=\"link-box\">
                    <input type=\"text\" class=\"link-input\" id=\"shareLink\" value=\"\" readonly />
                    <button class=\"copy-btn\" onclick=\"copyLink()\">Copy</button>
                </div>
            </div>
            <div class=\"tip-jar\">
                <div class=\"jar-container\">
                    <div class=\"jar-lid\"></div>
                    <div class=\"jar-body\">
                        <div class=\"jar-label\">💝 Tip Jar · Keep the proposal wall glowing</div>
                        <div class=\"qr-container\">
                            <img src=\"/static/upi-qr.png\" alt=\"UPI QR\" class=\"qr-code\" onerror=\"this.style.display='none'\">
                            <p class=\"upi-id\">hrithik.raj.543@okhdfcbank</p>
                        </div>
                        <div class=\"coins\">
                            <span class=\"coin\">🪙</span>
                            <span class=\"coin\">🪙</span>
                            <span class=\"coin\">🪙</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class=\"actions\">
                <a href=\"/\" class=\"btn btn-primary\">💌 Craft Your Proposal</a>
                <a href=\"https://www.pinterest.com/search/pins/?q=proposal%20quotes\" target=\"_blank\" class=\"btn btn-secondary\">Inspiration Board</a>
            </div>
            <p class=\"note\">This proposal dissolves in 24 hours to keep your promise private.</p>
        </div>
        <script>
            document.getElementById('shareLink').value = window.location.href;
            function copyLink() {{
                const input = document.getElementById('shareLink');
                input.select();
                navigator.clipboard.writeText(input.value).then(() => {{
                    const btn = event.target;
                    btn.textContent = 'Copied!';
                    setTimeout(() => btn.textContent = 'Copy', 1800);
                }}).catch(() => document.execCommand('copy'));
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
        <title>⌛ Proposal Window Closed</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
                background: linear-gradient(135deg, #2b2c3b 0%, #1c1f2c 35%, #0f1220 100%);
                color: #f7f0ff;
            }
            .card {
                max-width: 520px;
                width: 100%;
                background: rgba(20, 18, 33, 0.85);
                border-radius: 28px;
                padding: 50px 45px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: 0 30px 60px rgba(0,0,0,0.55);
            }
            .icon {
                font-size: 4rem;
                margin-bottom: 18px;
                display: inline-block;
                animation: pulse 2.5s ease-in-out infinite;
            }
            @keyframes pulse { 0%,100% { opacity: 0.6; transform: scale(1); } 50% { opacity: 1; transform: scale(1.1); } }
            h1 {
                font-family: 'Playfair Display', serif;
                font-size: 2.2rem;
                margin-bottom: 15px;
            }
            p {
                color: #c9c2d9;
                line-height: 1.7;
                margin-bottom: 25px;
            }
            .quote {
                border-left: 4px solid #f4c886;
                padding-left: 18px;
                margin: 25px 0;
                font-style: italic;
                color: #fce9ca;
            }
            a {
                display: inline-block;
                margin-top: 10px;
                padding: 16px 36px;
                border-radius: 16px;
                background: linear-gradient(120deg, #f9d976, #f39f86);
                color: #3a2620;
                text-decoration: none;
                font-weight: 600;
                box-shadow: 0 15px 35px rgba(243, 159, 134, 0.35);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">⌛</div>
            <h1>The moment slipped by</h1>
            <p>This proposal link has gracefully retired after its 24-hour spotlight.</p>
            <div class="quote">“Great gestures stay special because they live in memory, not forever online.”</div>
            <a href="/">💌 Craft a fresh proposal</a>
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
        <title>🔍 Proposal Not Found</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
                background: linear-gradient(135deg, #201f2c 0%, #2b2444 45%, #462d5f 100%);
                color: #fef6ff;
            }
            .card {
                max-width: 540px;
                width: 100%;
                background: rgba(14, 12, 24, 0.85);
                border-radius: 28px;
                padding: 50px 40px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 25px 65px rgba(6, 4, 12, 0.6);
            }
            .icon {
                font-size: 3.8rem;
                margin-bottom: 15px;
            }
            h1 {
                font-family: 'Playfair Display', serif;
                font-size: 2.3rem;
                margin-bottom: 18px;
            }
            p {
                color: #cdc2df;
                line-height: 1.7;
                margin-bottom: 28px;
            }
            a {
                display: inline-block;
                padding: 16px 32px;
                border-radius: 16px;
                background: linear-gradient(130deg, #f9d976, #f39f86);
                color: #3b2420;
                font-weight: 600;
                text-decoration: none;
                box-shadow: 0 15px 35px rgba(243, 159, 134, 0.35);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">🔍</div>
            <h1>Proposal not found</h1>
            <p>Either this link never existed, the URL was mistyped, or the heartfelt ask already expired.</p>
            <a href="/">💍 Start a new proposal</a>
        </div>
    </body>
    </html>
    """
