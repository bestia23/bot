from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Data produk
products = {
    1: {"name": "VIU PREMIUM", "price": 50000, "stock": 10},
    2: {"name": "NETFLIX", "price": 120000, "stock": 5},
    3: {"name": "CANVA LIFETIME", "price": 300000, "stock": 3},
    4: {"name": "VIDIO PLATINUM", "price": 45000, "stock": 8},
    5: {"name": "RCTI+", "price": 30000, "stock": 10},
    6: {"name": "VISION+", "price": 40000, "stock": 7},
    7: {"name": "YOUTUBE PREMIUM", "price": 100000, "stock": 6},
    8: {"name": "WETV PREMIUM", "price": 60000, "stock": 9},
}

# Data user (contoh saldo default)
user_data = {}

# Fungsi /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    username = user.username or "Unknown"
    
    # Inisialisasi saldo pengguna jika belum ada
    if user_id not in user_data:
        user_data[user_id] = {"saldo": 100000}  # Default saldo 100000
    
    saldo = user_data[user_id]["saldo"]

    text = (
        "𝗦𝗲𝗹𝗮𝗺𝗮𝘁 𝗗𝗮𝘁𝗮𝗻𝗴 𝗗𝗶 𝗝𝗮𝘆 𝗦𝘁𝗼𝗿𝗲\n\n"
        "⫘⫘⫘⫘⫘⫘⫘⫘⫘\n"
        f"𝐔𝐒𝐄𝐑 : {username}\n"
        f"𝐈𝐃   : {user_id}\n"
        f"𝐒𝐀𝐋𝐃𝐎: {saldo}\n"
        "⫘⫘⫘⫘⫘⫘⫘⫘⫘\n"
        "𝗔𝗗𝗠𝗜𝗡: @jayvpn\n"
        "𝗖𝗛𝗔𝗡𝗡𝗘𝗟: @jayvpnch"
    )
    
    keyboard = [
        [InlineKeyboardButton("✨𝗞𝗔𝗧𝗔𝗟𝗢𝗚✨", callback_data="catalog")],
        [InlineKeyboardButton("🏦𝗧𝗢𝗣 𝗨𝗣🏦", url="https://t.me/jayvpn")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# Fungsi untuk katalog
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    text = (
        "𝗦𝗶𝗹𝗮𝗵𝗸𝗮𝗻 𝗣𝗶𝗹𝗶𝗵 𝗣𝗿𝗼𝗱𝘂𝗸 𝘆𝗮𝗻𝗴 𝗜𝗻𝗴𝗶𝗻 𝗗𝗶𝗯𝗲𝗹𝗶\n\n"
    )
    for idx, product in products.items():
        text += f"{idx}. {product['name']}\n"
    text += "\n𝗨𝗻𝘁𝘂𝗸 𝗠𝗲𝗺𝗲𝘀𝗮𝗻, 𝗞𝗲𝘁𝗶𝗸 𝗔𝗻𝗴𝗸𝗮 𝗣𝗿𝗼𝗱𝘂𝗸"

    await query.edit_message_text(text)

# Fungsi untuk memproses pemesanan
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    saldo = user_data[user_id]["saldo"]
    try:
        product_id = int(update.message.text)
        if product_id not in products:
            await update.message.reply_text("Produk tidak ditemukan!")
            return
        
        product = products[product_id]
        text = (
            "﹌﹌﹌﹌﹌﹌﹌﹌﹌\n"
            f"▶𝗡𝗮𝗺𝗮 𝗣𝗿𝗼𝗱𝘂𝗸: {product['name']}\n"
            f"▶𝗛𝗮𝗿𝗴𝗮    : {product['price']}\n"
            f"▶𝗦𝘁𝗼𝗸     : {product['stock']}\n"
            "﹌﹌﹌﹌﹌﹌﹌﹌﹌"
        )
        keyboard = [[InlineKeyboardButton("𝗞𝗢𝗡𝗙𝗜𝗥𝗠𝗔𝗦𝗜", callback_data=f"confirm_{product_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text("Harap masukkan angka yang valid!")

# Fungsi untuk konfirmasi pesanan
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    saldo = user_data[user_id]["saldo"]
    product_id = int(query.data.split("_")[1])
    product = products[product_id]

    if saldo >= product["price"]:
        user_data[user_id]["saldo"] -= product["price"]
        product["stock"] -= 1
        with open(f"{product['name']}.txt", "w") as f:
            f.write(f"Produk: {product['name']}\nHarga: {product['price']}\n")
        await query.answer("Pesanan berhasil!")
        await query.edit_message_text("Pesanan berhasil, produk telah dikirim!")
    else:
        await query.answer("Saldo Tidak Cukup!")
        await query.edit_message_text("Saldo Tidak Cukup!")

# Main function
def main():
    application = Application.builder().token("7800809510:AAGLvEoeixLFcFefo6cVIBZIDCtSTQfsLF8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_catalog, pattern="catalog"))
    application.add_handler(CallbackQueryHandler(confirm_order, pattern="confirm_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
