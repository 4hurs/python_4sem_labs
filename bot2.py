import os
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters
import io
import tempfile

DIRECTION_TO_DEGREES = {
    "севера": 0,
    "северо-северо-востока": 22.5,
    "северо-востока": 45,
    "востоко-северо-востока": 67.5,
    "востока": 90,
    "востоко-юго-востока": 112.5,
    "юго-востока": 135,
    "юго-юго-востока": 157.5,
    "юга": 180,
    "юго-юго-запада": 202.5,
    "юго-запада": 225,
    "западо-юго-запада": 247.5,
    "запада": 270,
    "западо-северо-запада": 292.5,
    "северо-запада": 315,
    "северо-северо-запада": 337.5,
    "Штиль, безветрие": 0,
    "Переменное направление": 0  
}

def extract_degrees(direction_str):
    """Extract wind direction in degrees from the direction string"""
    if not isinstance(direction_str, str) or pd.isna(direction_str):
        return 0  
    
    for direction, degrees in DIRECTION_TO_DEGREES.items():
        if direction in direction_str:
            return degrees
    return 0  

def process_csv(file_path):
    """Process the CSV file and return wind speed and direction data"""
    try:
        df = pd.read_csv(
            file_path, 
            sep=';', 
            encoding='ansi', 
            skiprows=6,
            on_bad_lines='skip',
            quoting=3  
        )
        
        df.columns = df.columns.str.strip('"').str.strip()
        
        required_columns = ['DD', 'Ff']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV file doesn't contain required columns (DD and Ff)")
        
        df['direction_deg'] = df['DD'].apply(extract_degrees)
        df['speed_m_s'] = pd.to_numeric(df['Ff'], errors='coerce').fillna(0)
        
        return df['direction_deg'], df['speed_m_s']
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return None, None

def create_wind_rose(directions, speeds):
    """Create a wind rose plot from direction and speed data"""
    fig = plt.figure(figsize=(10, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    ax.bar(directions, speeds, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title="Скорость ветра (м/с)", bbox_to_anchor=(1.1, 1))
    plt.title("Роза ветров - Аэропорт Храброво", pad=20)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    buf.seek(0)
    return buf

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Привет! Отправьте мне CSV файл с данными о ветре с RP5.ru "
        "для аэропорта Храброво, и я построю розу ветров.\n\n"
        "Файл должен быть в формате CSV с разделителем ';' и содержать "
        "столбцы 'DD' (направление ветра) и 'Ff' (скорость ветра)."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the uploaded CSV file."""
    if not update.message.document.file_name.lower().endswith('.csv'):
        await update.message.reply_text("Пожалуйста, отправьте файл в формате CSV.")
        return
    
    file = await context.bot.get_file(update.message.document.file_id)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        await file.download_to_drive(temp_file.name)
        temp_path = temp_file.name
    
    try:
        directions, speeds = process_csv(temp_path)
        
        if directions is not None and speeds is not None and len(directions) > 0:

            wind_rose = create_wind_rose(directions, speeds)

            await update.message.reply_photo(
                photo=wind_rose, 
                caption="Роза ветров для аэропорта Храброво"
            )
        else:
            await update.message.reply_text(
                "Не удалось обработать файл. Пожалуйста, убедитесь, что:\n"
                "1. Это CSV файл с RP5.ru\n"
                "2. Файл содержит столбцы 'DD' и 'Ff'\n"
                "3. Данные корректны и не повреждены"
            )
    
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def main():
    """Start the bot."""
    application = Application.builder().token("7379708354:AAHGYaxWpF1reXg3CFtmIwzwEl2diFVrJdk").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.FileExtension("csv"), handle_document))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()