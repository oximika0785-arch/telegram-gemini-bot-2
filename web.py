
from flask import Flask, request from telegram import Bot, Update from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters import google.generativeai as genai import os

TELEGRAM_TOKEN = os.environ["8371875305:AAEUSUH1HCYsQX9me0MTRv_f9GYZ1-LPC3I"] GEMINI_KEY = os.environ["AIzaSyCbMn3zbDNSHwkms4O_tlKUNXLyarYYyL8"]

bot = Bot(token=TELEGRAM_TOKEN) dp = Dispatcher(bot, None, workers=0)

genai.configure(api_key=GEMINI_KEY)

def start(update, context): update.message.reply_text("✅ ربات روشنه و به Gemini وصله!")

def chat(update, context): user_text = update.message.text or "" try: resp = genai.GenerativeModel("gemini-1.5-flash").generate_content(user_text) update.message.reply_text(resp.text) except Exception as e: update.message.reply_text("❌ خطا: " + str(e))

dp.add_handler(CommandHandler("start", start)) dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

app = Flask(name)

@app.route("/") def index(): return "OK"

@app.route("/webhook", methods=["POST"]) def webhook(): update = Update.de_json(request.get_json(force=True), bot) dp.process_update(update) return "OK"
