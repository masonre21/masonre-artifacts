#!/usr/bin/env python3
"""Encrypt an HTML file into a password-gated static page.

Key derivation: PBKDF2-SHA256 (310k iterations) -> 64 bytes
(32 for AES-256-CBC via the openssl CLI, 32 for an HMAC-SHA256 tag).
The output file contains only ciphertext, so it is safe to host on a
public static site like GitHub Pages. Decryption happens in the browser
via WebCrypto.

Usage: python3 scripts/protect.py <source.html> <output.html> <password> [title]
"""

import base64
import hashlib
import hmac
import os
import subprocess
import sys

ITERATIONS = 310_000

if len(sys.argv) < 4:
    sys.exit("Usage: python3 scripts/protect.py <source.html> <output.html> <password> [title]")

src, out, password = sys.argv[1:4]
title = sys.argv[4] if len(sys.argv) > 4 else "Protected page"

html = open(src, "rb").read()
salt = os.urandom(16)
iv = os.urandom(16)

dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS, dklen=64)
enc_key, mac_key = dk[:32], dk[32:]

ciphertext = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-K", enc_key.hex(), "-iv", iv.hex()],
    input=html, capture_output=True, check=True,
).stdout
tag = hmac.new(mac_key, iv + ciphertext, hashlib.sha256).digest()

b64 = lambda b: base64.b64encode(b).decode()

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{--teal:#004540;--teal-lt:#0F9187;--gray:#1A1A19;--hair:#D9DED9;--muted:#6E7370;--wash:#F4F7F6}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:"Work Sans",system-ui,sans-serif;background:var(--wash);color:var(--gray);
    min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
  .gate{{background:#fff;border-top:3px solid var(--teal);box-shadow:0 18px 50px rgba(0,0,0,.12);
    max-width:400px;width:100%;padding:40px 38px 34px;text-align:center}}
  .eyebrow{{color:var(--teal-lt);font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase}}
  h1{{font-weight:300;font-size:26px;color:var(--teal);margin:10px 0 4px}}
  p.hint{{font-size:12.5px;color:var(--muted);margin-bottom:22px}}
  input{{width:100%;padding:12px 14px;font:inherit;font-size:15px;border:1px solid var(--hair);
    outline:none;text-align:center;letter-spacing:.08em}}
  input:focus{{border-color:var(--teal-lt)}}
  button{{width:100%;margin-top:12px;padding:12px;font:inherit;font-size:13px;font-weight:600;
    letter-spacing:.06em;background:var(--teal);color:#fff;border:none;cursor:pointer}}
  button:hover{{background:var(--teal-lt)}}
  button:disabled{{background:var(--muted);cursor:wait}}
  .err{{color:#A33;font-size:12.5px;margin-top:12px;min-height:18px}}
  .wordmark{{margin-top:26px;font-weight:700;font-size:13px;color:var(--teal)}}
</style>
</head>
<body>
<form class="gate" id="gate">
  <span class="eyebrow">Private · Abrams family</span>
  <h1>{title}</h1>
  <p class="hint">Enter the family password to open the itinerary.</p>
  <input type="password" id="pw" placeholder="Password" autocomplete="current-password" autofocus>
  <button type="submit" id="go">Open</button>
  <div class="err" id="err"></div>
  <div class="wordmark">masonre</div>
</form>
<script>
const SALT="{b64(salt)}", IV="{b64(iv)}", DATA="{b64(ciphertext)}", TAG="{b64(tag)}", ITER={ITERATIONS};
const fromB64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
async function decrypt(pw){{
  const salt = fromB64(SALT), iv = fromB64(IV), data = fromB64(DATA), tag = fromB64(TAG);
  const baseKey = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
  const bits = new Uint8Array(await crypto.subtle.deriveBits(
    {{name:"PBKDF2", salt, iterations:ITER, hash:"SHA-256"}}, baseKey, 512));
  const macKey = await crypto.subtle.importKey("raw", bits.slice(32), {{name:"HMAC", hash:"SHA-256"}}, false, ["verify"]);
  const signed = new Uint8Array(iv.length + data.length);
  signed.set(iv); signed.set(data, iv.length);
  if(!await crypto.subtle.verify("HMAC", macKey, tag, signed)) throw new Error("bad password");
  const aesKey = await crypto.subtle.importKey("raw", bits.slice(0, 32), "AES-CBC", false, ["decrypt"]);
  const plain = await crypto.subtle.decrypt({{name:"AES-CBC", iv}}, aesKey, data);
  return new TextDecoder().decode(plain);
}}
async function attempt(pw, silent){{
  const btn = document.getElementById("go"), err = document.getElementById("err");
  btn.disabled = true; err.textContent = "";
  try{{
    const html = await decrypt(pw);
    try{{ sessionStorage.setItem("pw", pw); }}catch(e){{}}
    document.open(); document.write(html); document.close();
  }}catch(e){{
    btn.disabled = false;
    if(!silent) err.textContent = "That's not it — try again.";
  }}
}}
document.getElementById("gate").addEventListener("submit", e => {{
  e.preventDefault();
  attempt(document.getElementById("pw").value, false);
}});
try{{
  const saved = sessionStorage.getItem("pw");
  if(saved) attempt(saved, true);
}}catch(e){{}}
</script>
</body>
</html>
"""

open(out, "w").write(page)
print(f"Encrypted {src} -> {out} ({len(ciphertext)} bytes ciphertext)")
