from flask import Flask, render_template_string, request, session, redirect, url_for
import uuid

app = Flask(__name__)
app.secret_key = "lavanya-quiz-secret"

QUESTIONS = {
    "identity": "I know you're Pahadi and from South Delhi, but what would you like to be called as?",
    "normalFood": "I like to eat on normal days?",
    "specialFood": "I like to spice up my special days from?",
    "lifelongFood": "If I ask you what food you could eat for the rest of your life, then what would it be?",
    "foodType": "FOOD Department se last question.....",
    "foodNote": "If you want to express more about food, write here...",
    "flower": "I like..... my fav flower",
    "genre": "Now let's know about music taste!! Pick your fav genre",
    "artist": "My fav music artist...",
    "spotify": "Spotify account",
    "drink": "I'm a coffee person or a chai person?",
    "hobbies": "Let's know about your hobbies now....",
    "hobbyOther": "If other, mention it here...",
    "scroll": "I like to scroll...",
    "feedback": "How did you like this?",
    "feedbackNote": "Tell me your honest feelings..."
}

INDEX_HTML = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hi, Lavanya ✈️💖</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Pacifico&display=swap" rel="stylesheet">
  <style>
    :root{--bg:#120b1f;--line:#ffffff1a;--text:#fff7ff;--muted:#d7cce7;--accent:#ff7db6;--shadow:0 20px 60px rgba(0,0,0,.35)}
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,sans-serif;background:radial-gradient(circle at top,#37225f 0,#120b1f 45%,#0c0816 100%);color:var(--text);min-height:100vh;overflow-x:hidden}
    .bg-orbs span{position:fixed;border-radius:50%;filter:blur(10px);opacity:.5;animation:float 12s infinite ease-in-out}
    .bg-orbs span:nth-child(1){width:220px;height:220px;background:#ff7db644;left:-40px;top:70px}.bg-orbs span:nth-child(2){width:180px;height:180px;background:#8d8cff44;right:20px;top:120px}.bg-orbs span:nth-child(3){width:260px;height:260px;background:#ffd36f33;left:30%;bottom:-80px}
    .hearts span{position:fixed;font-size:20px;opacity:.7;animation:rise 10s infinite ease-in-out}
    .hearts span:nth-child(1){left:10%;top:15%}.hearts span:nth-child(2){left:80%;top:18%}.hearts span:nth-child(3){left:20%;bottom:15%}.hearts span:nth-child(4){left:60%;bottom:20%}.hearts span:nth-child(5){left:45%;top:8%}.hearts span:nth-child(6){left:70%;bottom:8%}
    @keyframes float{50%{transform:translateY(-18px) scale(1.03)}}
    @keyframes rise{50%{transform:translateY(-12px) rotate(6deg)}}
    .app{width:min(920px,92vw);margin:32px auto 110px;position:relative}
    .card{display:none;background:linear-gradient(180deg,#281847dd,#1b1233dd);border:1px solid var(--line);box-shadow:var(--shadow);border-radius:28px;padding:34px;backdrop-filter:blur(14px)}
    .card.active{display:block;animation:pop .35s ease}
    .badge,.section-top,.chip{display:inline-block;padding:8px 12px;border-radius:999px;background:#ffffff14;color:#f4e9ff;font-size:13px;margin:0 0 14px}
    .lead,p,.subq{color:var(--muted);line-height:1.6}
    h1,h2,h3{margin:0 0 12px;font-family:Pacifico,cursive}
    .choice-row,.choice-col,.choice-grid{display:grid;gap:12px}
    .choice-row{grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}.choice-col{grid-template-columns:1fr}.choice-grid{grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}
    .option-pill{display:block;position:relative;border-radius:18px;border:1px solid #ffffff20;background:#0f0b1ea8;overflow:hidden;cursor:pointer;transition:.22s transform,.22s box-shadow,.22s border-color;min-height:54px}
    .option-pill:hover{transform:translateY(-2px);border-color:#ffffff3a;box-shadow:0 12px 28px rgba(0,0,0,.18)}
    .option-pill input{position:absolute;opacity:0;pointer-events:none}
    .option-pill span{display:flex;align-items:center;justify-content:center;padding:15px 16px;color:var(--text);font-weight:700;letter-spacing:.2px}
    .option-pill input:checked + span{background:linear-gradient(135deg,var(--accent),#ff9f6f);color:#fff}
    textarea,input{width:100%;border:1px solid #ffffff25;background:#0f0b1ea8;color:var(--text);padding:15px 16px;border-radius:16px;font:inherit;outline:none;margin-top:4px}
    textarea{min-height:110px;resize:vertical}
    .btn{border:0;border-radius:16px;padding:14px 18px;font:600 15px/1 Inter,sans-serif;cursor:pointer;transition:.2s transform;color:var(--text);margin-top:10px}
    .btn:hover{transform:translateY(-1px)}
    .primary{background:linear-gradient(135deg,var(--accent),#ff9f6f)}
    .gif-line,.hero-img{width:100%;max-width:520px;display:block;margin:18px auto;border-radius:20px;box-shadow:0 14px 38px rgba(0,0,0,.28)}
    .hero{text-align:center}.spark{font-size:20px;font-weight:800;color:#ffd36f}.mini{font-size:14px;color:#f1e7ff;line-height:1.5}
    @keyframes pop{from{transform:scale(.98);opacity:.4}to{transform:scale(1);opacity:1}}
    @media (max-width:640px){.card{padding:22px}}
  </style>
</head>
<body>
  <div class="bg-orbs"><span></span><span></span><span></span></div>
  <div class="hearts"><span>💖</span><span>✨</span><span>🌸</span><span>💫</span><span>🫶</span><span>💖</span></div>
  <main class="app">
    <form method="POST" action="/submit" class="wizard">
      <section class="card active hero">
        <div class="badge">For the cutest cabin crew queen 👑✈️</div>
        <img class="hero-img" src="https://pplx-res.cloudinary.com/image/upload/pplx_search_images/0d6905ff529af1004cb8ad2582e2c320578df95f.jpg" alt="Airline crew illustration">
        <h1>Hi, Lavanya ✨💖</h1>
        <p class="lead">A tiny happy quiz made just for you — full of hearts, smiles, and a little airplane energy.</p>
        <button type="button" class="btn primary next-step">Start 🌷</button>
      </section>

      <section class="card"><div class="section-top">💫 About you</div><h2>I know you're Pahadi and from South Delhi, but what would you like to be called as?</h2><div class="choice-row"><label class="option-pill"><input type="radio" name="identity" value="South Delhi"><span>South Delhi</span></label><label class="option-pill"><input type="radio" name="identity" value="Pahadi"><span>Pahadi</span></label></div><img class="gif-line" src="https://media.giphy.com/media/111ebonMs90YLu/giphy.gif" alt="applause gif"><button type="button" class="btn primary next-step">Next ➡️</button></section>
      <section class="card"><div class="section-top">🌸 Cute check</div><h2>OK COOL <span class="chip">friend</span>!</h2><p>That sounds lovely.</p><img class="gif-line" src="https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif" alt="sparkle gif"><button type="button" class="btn primary next-step">Continue 💖</button></section>
      <section class="card"><div class="section-top">🍽️ Food vibes</div><h2>Let's know about you more now!!</h2><h3>I like to eat...</h3><p class="subq">1) On normal days?</p><div class="choice-col"><label class="option-pill"><input type="radio" name="normalFood" value="Healthy-diet food"><span>Healthy-diet food</span></label><label class="option-pill"><input type="radio" name="normalFood" value="Healthy-homecooked food"><span>Healthy-homecooked food</span></label><label class="option-pill"><input type="radio" name="normalFood" value="Un-healthy....uff"><span>Un-healthy....uff</span></label></div><p class="subq">2) I like to spice up my special days from?</p><div class="choice-col"><label class="option-pill"><input type="radio" name="specialFood" value="Eating my fav street food"><span>Eating my fav street food</span></label><label class="option-pill"><input type="radio" name="specialFood" value="Cooking my cheat meal...lol"><span>Cooking my cheat meal...lol</span></label><label class="option-pill"><input type="radio" name="specialFood" value="Kabhi kuch kabhi kuch, depending on my mood"><span>Kabhi kuch kabhi kuch, depending on my mood</span></label></div><img class="gif-line" src="https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif" alt="clapping gif"><button type="button" class="btn primary next-step">Next 🌈</button></section>
      <section class="card"><div class="section-top">🍜 Food forever</div><h2>If I ask you what food you could eat for the rest of your life, then what would it be?</h2><textarea name="lifelongFood" placeholder="Write your answer here..."></textarea><button type="button" class="btn primary next-step">Next ✨</button></section>
      <section class="card"><div class="section-top">🥗 Food style</div><h2>FOOD Department se last question.....</h2><div class="choice-col"><label class="option-pill"><input type="radio" name="foodType" value="I am a foodie"><span>I am a foodie</span></label><label class="option-pill"><input type="radio" name="foodType" value="I'm health conscious more so try to keep a balance"><span>I'm health conscious more so try to keep a balance</span></label><label class="option-pill"><input type="radio" name="foodType" value="I'm not all foodie"><span>I'm not all foodie</span></label></div><textarea name="foodNote" placeholder="If you want to express more about food, write here..."></textarea><img class="gif-line" src="https://media.giphy.com/media/3oz8xAFtqoOUUrsh7W/giphy.gif" alt="celebration gif"><button type="button" class="btn primary next-step">Next 🎀</button></section>
      <section class="card"><div class="section-top">🌷 Flowers</div><h2>I like..... my fav flower</h2><input name="flower" type="text" placeholder="Rose, lily, sunflower..."><button type="button" class="btn primary next-step">Next 💐</button></section>
      <section class="card"><div class="section-top">🎶 Music mood</div><h2>Now let's know about music taste!!</h2><p class="subq">Pick your fav genre</p><div class="choice-grid"><label class="option-pill"><input type="radio" name="genre" value="Pop"><span>Pop</span></label><label class="option-pill"><input type="radio" name="genre" value="Rock"><span>Rock</span></label><label class="option-pill"><input type="radio" name="genre" value="Hip-Hop / Rap"><span>Hip-Hop / Rap</span></label><label class="option-pill"><input type="radio" name="genre" value="R&B"><span>R&B</span></label><label class="option-pill"><input type="radio" name="genre" value="Indie"><span>Indie</span></label><label class="option-pill"><input type="radio" name="genre" value="Classical"><span>Classical</span></label><label class="option-pill"><input type="radio" name="genre" value="Jazz"><span>Jazz</span></label><label class="option-pill"><input type="radio" name="genre" value="EDM"><span>EDM</span></label><label class="option-pill"><input type="radio" name="genre" value="Punjabi"><span>Punjabi</span></label><label class="option-pill"><input type="radio" name="genre" value="Bollywood"><span>Bollywood</span></label><label class="option-pill"><input type="radio" name="genre" value="K-pop"><span>K-pop</span></label><label class="option-pill"><input type="radio" name="genre" value="Any good vibe"><span>Any good vibe</span></label></div><img class="gif-line" src="https://media.giphy.com/media/ASd0Ukj0y3qMM/giphy.gif" alt="music gif"><button type="button" class="btn primary next-step">Next 🎵</button></section>
      <section class="card"><div class="section-top">🎤 Artist + Spotify</div><h2>My fav music artist...</h2><input name="artist" type="text" placeholder="Type your favourite artist..."><h3 class="mini">Now, I would like to know your spotify account, tho i don't hv a premium lol but still i would like to know it maybe any day we jammed.</h3><input name="spotify" type="text" placeholder="Spotify username or link..."><button type="button" class="btn primary next-step">Next 💞</button></section>
      <section class="card"><div class="section-top">☕ Warm drink</div><h2>I'm a coffee person or a chai person?</h2><div class="choice-row"><label class="option-pill"><input type="radio" name="drink" value="Coffee"><span>☕ Coffee</span></label><label class="option-pill"><input type="radio" name="drink" value="Chai"><span>🫖 Chai</span></label></div><img class="gif-line" src="https://media.giphy.com/media/xUPGcEliCc7bETyfO8/giphy.gif" alt="coffee gif"><button type="button" class="btn primary next-step">Next 🌼</button></section>
      <section class="card"><div class="section-top">🎀 Hobbies</div><h2>Let's know about your hobbies now....</h2><div class="choice-grid"><label class="option-pill"><input type="radio" name="hobbies" value="I listen music"><span>I listen music</span></label><label class="option-pill"><input type="radio" name="hobbies" value="I dance"><span>I dance</span></label><label class="option-pill"><input type="radio" name="hobbies" value="I do random"><span>I do random</span></label><label class="option-pill"><input type="radio" name="hobbies" value="I cook"><span>I cook</span></label><label class="option-pill"><input type="radio" name="hobbies" value="I explore"><span>I explore</span></label><label class="option-pill"><input type="radio" name="hobbies" value="I play sports/go to the gym"><span>I play sports/go to the gym</span></label><label class="option-pill"><input type="radio" name="hobbies" value="Other"><span>Other</span></label></div><input name="hobbyOther" type="text" placeholder="If other, mention it here..."><button type="button" class="btn primary next-step">Next ✈️</button></section>
      <section class="card"><div class="section-top">📱 Scroll mode</div><h2>I like to scroll...</h2><div class="choice-grid"><label class="option-pill"><input type="radio" name="scroll" value="music"><span>music</span></label><label class="option-pill"><input type="radio" name="scroll" value="arts"><span>arts</span></label><label class="option-pill"><input type="radio" name="scroll" value="professional"><span>professional</span></label><label class="option-pill"><input type="radio" name="scroll" value="news"><span>news</span></label><label class="option-pill"><input type="radio" name="scroll" value="political"><span>political</span></label><label class="option-pill"><input type="radio" name="scroll" value="funny"><span>funny</span></label><label class="option-pill"><input type="radio" name="scroll" value="kuch bhi bss dekhne se mtlb 😄"><span>kuch bhi bss dekhne se mtlb 😄</span></label></div><img class="gif-line" src="https://media.giphy.com/media/26BRv0ThsHCqDrG/giphy.gif" alt="scrolling gif"><button type="button" class="btn primary next-step">Next 🌸</button></section>
      <section class="card"><div class="section-top">💌 Thank you</div><h2>Thank you for staying with me...</h2><p class="spark">I GOT U, LAVANYA!!</p><p>You have a great taste!!</p><img class="gif-line" src="https://media.giphy.com/media/111ebonMs90YLu/giphy.gif" alt="applause gif"><button type="button" class="btn primary next-step">Continue 🫶</button></section>
      <section class="card"><div class="section-top">⭐ Feedback</div><h2>How did you like this?</h2><div class="choice-row"><label class="option-pill"><input type="radio" name="feedback" value="I loved it!"><span>I loved it!</span></label><label class="option-pill"><input type="radio" name="feedback" value="I hated it"><span>I hated it</span></label><label class="option-pill"><input type="radio" name="feedback" value="Theek tha...ok!"><span>Theek tha...ok!</span></label></div><textarea name="feedbackNote" placeholder="Tell me your honest feelings..."></textarea><button type="submit" class="btn primary">Finish 🎉</button></section>
    </form>
  </main>
  <script>
    const cards=[...document.querySelectorAll('.card')];let current=0;document.addEventListener('click',e=>{if(e.target.classList.contains('next-step')){current=Math.min(cards.length-1,current+1);cards.forEach((c,i)=>c.classList.toggle('active',i===current))}});cards.forEach((c,i)=>c.classList.toggle('active',i===0));
  </script>
</body>
</html>
'''

RESULT_HTML = r'''
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Secret Responses</title><style>body{margin:0;font-family:Arial,sans-serif;background:#120b1f;color:#fff;padding:24px}.box{max-width:1100px;margin:auto;background:#1b1233;border-radius:20px;padding:24px;border:1px solid #ffffff1a}table{width:100%;border-collapse:collapse;background:#0d0a1c;border-radius:16px;overflow:hidden}th,td{padding:14px 16px;border-bottom:1px solid #ffffff12;vertical-align:top;text-align:left}th{background:#ffffff12}td{color:#eadff7}h1{margin-top:0}</style></head>
<body><div class="box"><h1>Responses</h1><table><thead><tr><th>Question</th><th>Answer</th></tr></thead><tbody>{% for row in rows %}<tr><td>{{ row.question }}</td><td>{{ row.answer }}</td></tr>{% endfor %}</tbody></table></div></body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict(flat=True)
    rows = []
    for key, question in QUESTIONS.items():
        value = data.get(key, '').strip()
        if value:
            rows.append({'question': question, 'answer': value})
    token = str(uuid.uuid4())
    session[f'responses_{token}'] = rows
    return redirect(url_for('secret_responses', token=token))

@app.route('/secret-responses/<token>', methods=['GET'])
def secret_responses(token):
    rows = session.get(f'responses_{token}', [])
    return render_template_string(RESULT_HTML, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
