from flask import Flask
from threading import Thread
import stats

app = Flask('')

@app.route('/health')
def health():
    return {"status": "ok"}, 200

@app.route('/')
def home():
    s = stats.get_stats()

    history_rows = ""
    for date, count in s["history"].items():
        history_rows += f"<tr><td>{date}</td><td><b>{count}</b></td></tr>"
    if not history_rows:
        history_rows = "<tr><td colspan='2' style='color:#888'>Belum ada data</td></tr>"

    per_bot_rows = ""
    bot_labels = {
        'random_pacar_bot': '🤖 @random_pacar_bot',
        'AnonyMeetBot':     '🤖 @AnonyMeetBot',
        'chatbot':          '🤖 @chatbot',
        'mechat':           '🤖 @mechat',
        'auto_reply':       '💬 Auto-Reply DM',
    }
    for bot, count in sorted(s["per_bot"].items(), key=lambda x: -x[1]):
        if bot.startswith('grup_'):
            label = f"👥 @{bot[len('grup_'):]}"
        else:
            label = bot_labels.get(bot, f"🤖 @{bot}")
        per_bot_rows += f"<tr><td>{label}</td><td><b>{count}</b></td></tr>"
    if not per_bot_rows:
        per_bot_rows = "<tr><td colspan='2' style='color:#888'>Belum ada data</td></tr>"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="10">
  <title>Bot Monitor</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Arial, sans-serif; background: #0f0f0f; color: #fff; padding: 24px; }}
    h1 {{ color: #00e676; margin-bottom: 20px; font-size: 22px; }}
    h2 {{ color: #aaa; font-size: 15px; margin: 20px 0 8px; }}
    .cards {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    .card {{ background: #1e1e1e; border-radius: 12px; padding: 20px 28px; text-align: center; }}
    .card .num {{ font-size: 48px; font-weight: bold; color: #00e676; }}
    .card .label {{ color: #aaa; margin-top: 6px; font-size: 13px; }}
    table {{ width: 100%; max-width: 420px; border-collapse: collapse; margin-top: 6px; }}
    th {{ background: #00e676; color: #000; padding: 9px 14px; text-align: left; }}
    td {{ padding: 9px 14px; border-bottom: 1px solid #2a2a2a; }}
    .badge {{ display: inline-block; background: #00e676; color: #000; border-radius: 6px; padding: 2px 8px; font-size: 12px; font-weight: bold; }}
    .status {{ color: #555; font-size: 12px; margin-top: 20px; }}
  </style>
</head>
<body>
  <h1>📊 Bot Promo Monitor</h1>

  <div class="cards">
    <div class="card">
      <div class="num">{s['today']}</div>
      <div class="label">Terkirim Hari Ini<br>{s['date']}</div>
    </div>
    <div class="card">
      <div class="num">{s['total']}</div>
      <div class="label">Total Semua Waktu</div>
    </div>
  </div>

  <p style="margin-top:14px">🕐 Terakhir kirim: <span class="badge">{s['last_sent'] or '-'}</span></p>

  <h2>📌 Per Bot (Total)</h2>
  <table>
    <tr><th>Bot</th><th>Kirim</th></tr>
    {per_bot_rows}
  </table>

  <h2>📅 Riwayat Harian</h2>
  <table>
    <tr><th>Tanggal</th><th>Jumlah Kirim</th></tr>
    {history_rows}
  </table>

  <p class="status">⟳ Auto-refresh setiap 10 detik</p>
</body>
</html>"""

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
