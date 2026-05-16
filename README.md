# JilciyeBot - AI Somali Learning Hub (ASL) 🚀

Kusoo dhowoow kaydka (Repository) rasmiga ah ee **JilciyeBot**! Mashruucani waa Bot waxbarasho oo casri ah oo ku shaqeeya sirdoonka macmalka ah (AI), kaas oo loogu talagalay inuu dhalinyarada iyo ganacsatada Soomaaliyeed barto **AI iyo Chatbot Automation**. Bot-kan waxaa awooda siiya nidaamka furan ee **DeepTutor**.

## 🌟 Tilmaamaha Muhiimka ah (Key Features)
- **JilciyeBot Persona**: Bot ku hadla af-Soomaali dhiirigelin leh, kaas oo bixiya koorsooyin bilaash ah (ilaa 2028).
- **Koorsooyinka Uu Bixiyo**:
  - WhatsApp, Telegram, Messenger, & Instagram Automation Bots.
  - AI Video Editing, AI Web Design, iyo AI ChatGPT Data Writing.
- **Telegram Menu Cusub**: Bot-ku wuxuu wataa Menu (Badhamo) casri ah oo u sahlayo ardayga inuu doorto:
  - 👨‍💻 La Hadal Dadka
  - 🤖 La Hadal AI
  - 📝 Isqor (Register)

## ☁️ Xaggee Buu Ku Kaydsan Yahay Mashruucan?
Mashruucan wuxuu si rasmi ah ugu kaydsan yahay **Saddex (3) Meelood**:
1. **GitHub (Halkan):** Waa meesha koodhka rasmiga ah (Source Code) uu yaallo oo laga akhriyo.
2. **Kombuyuutarkaaga (Local VSCode):** Waa meesha aad koodhka ku bedesho oo aad tijaabada ku samayso.
3. **Google Cloud VPS (Live Server):** Waa meesha uu Bot-ku si dhab ah uga shaqeeyo **24/7** isagoo isticmaalaya Docker!

---

## 🛠 Sida Loo Kiciyo (How to Run)

### 1. Sida Loo Kiciyo Kombuyuutarkaaga (Local Testing)
Haddii aad rabto inaad koodhka ku tijaabiso kombuyuutarkaaga, raac tillaabooyinkan:
1. Hubi in faylka sirta ah ee `.env` uu ku jiro galka ugu weyn (Root folder), uuna ku qoran yahay furahaaga (API Key):
   ```env
   LLM_BINDING=openai
   LLM_MODEL=deepseek-chat
   LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
   LLM_HOST=https://api.deepseek.com/v1
   ```
2. Terminal-ka VSCode-ka ku dhufo amarkan:
   ```bash
   python -m deeptutor_cli.main serve
   ```
*(Fiiro Gaar ah: Haddii uu ku yiraahdo "no-key", macnaheedu waa inaadan haysan faylka `.env` ama aadan dib u kicin Server-ka markaad ku dartay kadib!)*

### 2. Sida Loo Saaro Live Server-ka (Google Cloud VPS Deployment)
Markaad koodhka wax ka bedesho kombuyuutarkaaga, raac 2-dan tallaabo si aad u geyso Server-ka Cloud-ka ee Google:

**Tallaabada A (Gudaha VSCode-kaaga):**
```bash
git add .
git commit -m "Updated bot code"
git push origin main
```

**Tallaabada B (Gudaha Cloud Shell / SSH):**
Fur Google Cloud Console, ku dhufo badhanka **SSH** ee ku yaalla Server-kaaga (`ustaadcaawiye`), kadibna ku dhufo amarradan:
```bash
cd ~/ASTAAD_AI
git pull origin main
sudo rm -f data/tutorbot/jilciyebot/config.yaml
sudo docker compose restart deeptutor
```

*(Hubi in faylka `.env` uu sidoo kale u dhex yaallo Server-kaaga Cloud-ka ah, haddii kale Cloud-ku wuxuu ku siinayaa qaladka "no-key").*

---
*Waxaa lagu dhisay ❤️ & 🤖 bulshada Soomaaliyeed.*
