#import All Python Packages
from telegram import ParseMode
from telegram.ext import *
import logging
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileReader, PdfFileWriter
import random
import pandas as pd
import requests
from telegram import *

_ParseMode=ParseMode.HTML

#Here Is The Telegram Bot Token
BOT_TOKEN = os.getenv("5833966794:AAHSMIeCrAEZfyXWgtEg-BxgyRr61jDcDyc")


#Here Is Bot Status In Command Line
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#Start Command
def start_command(update, context):
    update.message.reply_text(f'''🔰 <b>Hello Dear, {update.message.chat.full_name} \n\n🛰 I'm Guess Paper BOT ⚡️\n\n😎 Please Send Your Gmail Address To Me⚡️ \n\n<a href="https://t.me/AP22R">🔥 2022 Main Revision - Anuradha Perera 🔥</a></b> ''',parse_mode=_ParseMode)
    update.message.reply_sticker("CAACAgIAAxkBAAIEd2JZLvjl2AG4exeqftRZrzaJKVAWAAIBAQACVp29CiK-nw64wuY0IwQ")

def  get_gmail(update,context):
    #Get User Message
    mail = update.message.text
    mail = str.lower(mail)
    #check User Gmail In Google Sheet...
    stm = update.message.reply_text('🚀Conecting to database...')

     #Here Is Spread Sheet Share ID
    with open('google_sheet_id.txt', 'r') as file:
        share_id = file.read()
        print(share_id)
   

    df =pd.read_csv(f"https://docs.google.com/spreadsheets/d/{share_id}/export?format=csv")

    with open('database_copy.txt', 'w') as f:
       dfAsString = df.to_string(header=False, index=False)
       f.write(dfAsString)
       f.close()
     
    with open('database_copy.txt', 'r') as file:
        # read all content of a file
        word=mail
        content = file.read()
        name = update.message.chat.first_name
        # check if string present in a file
        if word in content and len(word)>=11:
            print('string exist in a file')
            stm.edit_text(f"<b>Hello,{name} Your Gmail Address is Found🔥</b>",parse_mode=_ParseMode)
        else:
            stm.edit_text(f"<b>⚠️ Sorry,{name} Your Gmail Address Not Found..</b>",parse_mode=_ParseMode)
            update.message.reply_sticker("CAACAgIAAxkBAAEBj2ZjqJ_qnxzqMe4gqORr60SJFUY8eQACEgADwDZPEzO8ngEulQc3LAQ")
            return()
         #end Check gmail   

    #creating Watermark Template
    Path='watermark.pdf'
    uid=update.message.chat_id
    c=canvas.Canvas(Path)
    c.translate(cm,cm)
    c.setFont('Helvetica',20)
    c.setFillColorCMYK(0, 0, 0, 0, alpha=0.7)
    c.rect(204, 199, 157, 15, stroke=0, fill=1)
    c.setFillColorCMYK(0, 0, 0, 100, alpha=0.7)
    c.drawString(cm*6.4,cm*0.81,mail)
    c.drawString(cm*6.4,cm*14.81,mail)
    c.drawString(cm*6.4,cm*26.81,mail)
    c.setFont('Helvetica',10)
    c.drawString(cm*0,cm*26.81,f'Pdf Requester Telegram Id:-{uid}')
    c.drawString(cm*0,cm*1,f'Pdf Requester Telegram Id:-{uid}')
    c.showPage()
    c.save()
    #finshed Making Watermark
    status_st = update.message.reply_sticker('CAACAgIAAxkBAAEBjetjpWK4ww4fNlRXqp2syaby8sIPNQACugADMNSdEYTXxIjEUGdWLAQ')
    status_msg = update.message.reply_text('🚀 Loading File...')

    #Marage Watermark To PDf file 
    pdf_file = "paper.pdf"
    watermark = "watermark.pdf"
    merged = "Encrypted_paper.pdf"

    with open(pdf_file, "rb") as input_file, open(watermark, "rb") as watermark_file:
        input_pdf = PdfFileReader(input_file)
        watermark_pdf = PdfFileReader(watermark_file)
        watermark_page = watermark_pdf.getPage(0)
        output = PdfFileWriter()
        status_msg.edit_text('🚀Encrypting Pdf ...')

        for i in range(input_pdf.getNumPages()):
           pdf_page = input_pdf.getPage(i)
           pdf_page.mergePage(watermark_page)
           output.addPage(pdf_page)
           #Genarate Random Passwords
           password_length =10
           characters = "abcdezqrn12345"
           password = ""   
           for i in range(password_length):
               password = password + random.choice(characters)
        output.encrypt(password)
        with open(merged, "wb") as merged_file:
           output.write(merged_file)
           merged_file.close()
           watermark_file.close()
           input_file.close()



    chat_id = update.message.chat.id
    doc_file = open(f"Encrypted_paper.pdf", "rb")
    status_msg.edit_text('🚀Uploading Pdf ...')
    context.bot.send_document(chat_id,doc_file )
     #button
    btn= [[InlineKeyboardButton('🔥2022 GUESS PAPERS | PHYSICS අනුරාධ පෙරේරා🚀', url=f'https://t.me/APGUESS')]]
    reply_markup1 = InlineKeyboardMarkup(btn)
    status_msg.edit_text(f'''🔑 PDF Password is=<code>{password}</code>\n\n<b><a href="https://t.me/Project_Ceb">🚀 Powered By Project CEB 🚀</a>\n\n⭐️ Bot Developer:@Error_316</b>''',parse_mode=_ParseMode,reply_markup=reply_markup1)
    status_st.delete()

          

def main():
    print("Started")
    TOKEN = '5939101681:AAEfL5lCzHfcKw8CE7FtJyMtNoA_Ave2Coo'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, get_gmail))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()