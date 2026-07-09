from flask import Flask
from threading import Thread
import stats

app = Flask('')

@app.route('/')
def home():
    s = stats.get_stats()
    history_rows = ""
    for date, count in s["history"].items():
        history_rows += f"<tr><td>{date}</td><td><b>{count}</b></td></tr>"
    if not history_rows:
        history_rows = "<tr><td colspan='2' style='color:#888'>Belum ada data</td></tr>"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="10">
  <title>Bot Monitor</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #0f0f0f; color: #fff; margin: 0; padding: 20px; }}
    h1 {{ color: #00e676; }}
    .card {{ background: #1e1e1e; border-radius: 12px; padding: 20px; margin: 10px 0; display: inline-block; min-width: 180px; text-align: center; }}
    .card .num {{ font-size: 48px; font-weight: bold; color: #00e676; }}
    .card .label {{ color: #aaa; margin-top: 5px; }}
    table {{ width: 100%; max-width: 400px; border-collapse: collapse; margin-top: 20px; }}
    th {{ background: #00e676; color: #000; padding: 10px; }}
    td {{ padding: 10px; border-bottom: 1px solid #333; text-align: center; }}
    .status {{ color: #00e676; font-size: 13px; margin-top: 20px; }}
  </style>
</head>
<body>
  <h1>📊 Bot Monitor — @random_pacar_bot</h1>
  <div>
    <div class="card">
      <div class="num">{s['today']}</div>
      <div class="label">Terkirim Hari Ini</div>
    </div>
    &nbsp;&nbsp;
    <div class="card">
      <div class="num">{s['total']}</div>
      <div class="label">Total Semua</div>
    </div>
  </div>
  <p>🕐 Terakhir kirim: <b>{s['last_sent'] or '-'}</b></p>
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
