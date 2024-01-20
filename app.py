from component import *
from customtkinter import *
import sqlite3
import base64
import shutil
from PIL import ImageTk
import os
import threading
import webbrowser
from datetime import datetime

con = sqlite3.connect('postdb.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Website_name CHAR(200),
                consumer_key CHAR(200),
                consumer_secret CHAR(200),
                Category_name CHAR(200)
            )  
            ''')


data_check = cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check == None:
    cur.execute('''
                    INSERT INTO Postdata(
                        Website_name,
                        consumer_key,
                        consumer_secret,
                        Category_name)
                    VALUES(
                        'https://ebookwise.com/',
                        'ck_2f9c3979e726fe187d91be14d5156358191f55eb',
                        'cs_bc39de27b69cd558bb33199ea23472c1a3b5e429',
                        'category name'
                        )
                    
                    ''')
# TK part
window = CTk()
set_default_color_theme("green")
set_appearance_mode("light")
window.title("AI Writing App by Samrat Biswas")
window.geometry("1050x700")
iconpath = ImageTk.PhotoImage(file=os.path.join("logo.ico"))
window.wm_iconbitmap()
window.iconphoto(False, iconpath)


# Create a Frame + Content Frame with scrollbar
frame = CTkFrame(window)
frame.pack(fill=BOTH, expand=True)
canvas = CTkCanvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event:on_mousewheel(event))  # Labda have to use when function is below
scrollbar = CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = CTkFrame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)


today = datetime.now().date()

targeted_date = datetime(2050, 1, 2).date()  # Change this to your targeted date


if today < targeted_date:

    year_difference = targeted_date.year - today.year
    # Trail Section
    if year_difference <= 1:
        trail_frame = CTkFrame(content_frame)
        trail_frame.grid(pady=10, padx=20)
        # label section
        trail_time = CTkLabel(trail_frame, font=('',18), text_color=('#B53C33','#B53C33'), text=f"Your trial will be finish after : {targeted_date.day} - {targeted_date.month} - {targeted_date.year}")
        trail_time.grid(row=0, column=0, padx=10, pady=3)

    # website info widgets
    webinfo_frame = CTkFrame(content_frame)
    webinfo_frame.grid(pady=10, padx=20)

    # label section
    website_name = CTkLabel(webinfo_frame, text="Website Name")
    website_name.grid(row=1, column=0, padx=10, pady=3)

    consumer_key = CTkLabel(webinfo_frame, text="Consumer Key")
    consumer_key.grid(row=1, column=1, padx=10, pady=3)

    consumer_secret = CTkLabel(webinfo_frame, text="Consumer Secret Key")
    consumer_secret.grid(row=1, column=2, padx=10, pady=3)

    app_guide = CTkLabel(webinfo_frame, text="🔗")
    app_guide.grid(row=1, column=3, padx=10, pady=3)

    category = CTkLabel(webinfo_frame, text="Category")
    category.grid(row=1, column=4, padx=10, pady=3)

    status = CTkLabel(webinfo_frame, text="Post Status")
    status.grid(row=1, column=5, padx=10, pady=3)


    # Input section
    website_entry = CTkEntry(webinfo_frame, width=230, border_width=1)
    website_entry.insert(0, str(cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()[0]))  # Default data
    website_entry.grid(row=2, column=0, padx=10, pady=10)

    username_entry = CTkEntry(webinfo_frame, width=150, border_width=1)
    username_entry.insert(0, str(cur.execute('''SELECT consumer_key FROM Postdata WHERE ID=1''').fetchone()[0]))
    username_entry.grid(row=2, column=1, padx=10, pady=10)

    consumer_secret_entry = CTkEntry(webinfo_frame, width=220, border_width=1)
    consumer_secret_entry.insert(0, str(cur.execute('''SELECT consumer_secret FROM Postdata WHERE ID=1''').fetchone()[0]))
    consumer_secret_entry.grid(row=2, column=2, padx=0, pady=0)

    consumer_secret_guide = CTkButton(webinfo_frame, text="Guide", width=40, fg_color=('#2374E1'), command=lambda : webbrowser.open_new('https://woo.com/document/woocommerce-rest-api/'))
    consumer_secret_guide.grid(row=2, column=3, padx=10, pady=10)

    category = CTkEntry(webinfo_frame, width=140, border_width=1)
    category.insert(0, str(cur.execute('''SELECT Category_name FROM Postdata WHERE ID=1''').fetchone()[0]))
    category.grid(row=2, column=4, pady=10, padx=10)

    status = CTkComboBox(webinfo_frame, width=110, border_width=1, values=['draft', 'publish'], state='readonly')
    status.set('publish')
    status.grid(row=2, column=5,pady=10, padx=10)


    # Terminal
    terminal = CTkFrame(content_frame)
    terminal.grid(row=15, column=0)

    keyword_label = CTkLabel(terminal, text="Input Keywords")
    keyword_label.grid(row=16, column=0, pady=5)

    output_label = CTkLabel(terminal, text="Output")
    output_label.grid(row=16, column=1, pady=5)

    keyword_input = CTkTextbox(terminal, width=486, height=300)
    keyword_input.insert('1.0', "Input keyword list here...")
    keyword_input.grid(row=17, column=0, pady=0, ipadx=5)

    output = CTkTextbox(terminal, fg_color=('black', 'white'), text_color=('white', 'black'), width=486, height=300)
    output.grid(row=17, column=1, pady=0, ipadx=5)


    # Command
    command_label = CTkFrame(content_frame, bg_color=('#DBDBDB'), fg_color=('#DBDBDB'))
    command_label.grid(row=18,column=0, padx=10, pady=(30, 30))

    start = CTkButton(command_label, text=" ▶ Run", fg_color=('#2AA26F'), command=lambda:operation_start()) # Labda have to use when function is below
    start.grid(row=19, column=0, padx=20, pady=10, ipadx=20)

    Update = CTkButton(command_label, text=' ➡️ Save Update', fg_color=("#2AA26F"), command=lambda:db_save())
    Update.grid(row=19, column=1, padx=20, pady=10, ipadx=20)

    Reset = CTkButton(command_label, text=' ↻ Reset Commands', fg_color=("#EB4C42"), command=lambda:reset_data())
    Reset.grid(row=19, column=2, padx=20, pady=10, ipadx=20)

    # Log
    log_label = CTkLabel(content_frame, text="Logs", font=('',20), fg_color=("#EB4C42"), text_color=('white', 'black'))
    log_label.grid(row=20, column=0, pady=0, ipadx=20)

    log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=990, height=200)
    log.grid(row=21, column=0, padx=5,  pady=(5, 10))

    copyright = CTkLabel(content_frame, text="Need any help ?")
    copyright.grid(row=22, column=0, padx=5,  pady=(5, 0))

    copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'), command=lambda : webbrowser.open_new('https://www.facebook.com/samratprodev/'))
    copy_button.grid(row=23, column=0, padx=5,  pady=(5, 300))
else:
    # website info widgets
    webinfo_frame = CTkFrame(content_frame, fg_color=("#F0F0F0"))
    webinfo_frame.grid(pady=10, padx=20)
    warning = CTkLabel(webinfo_frame, width=1000, height=300, text="Your trail has been finished \nPlease contact with Developer to unloack the Software")
    warning.grid(row=0, column=0, padx=10, pady=3)
    copy_button = CTkButton(webinfo_frame, text="Contact With Developer", fg_color=('#2374E1'), command=lambda : webbrowser.open_new('https://www.facebook.com/samratprodev/'))
    copy_button.grid(row=1, column=0, padx=5,  pady=(5, 300))


def db_save():
    website_name = str(website_entry.get())
    username = str(username_entry.get())
    consumer_secret = str(consumer_secret_entry.get())
    category_name = str(category.get())
    cur.execute(f'''
                    UPDATE Postdata
                    SET
                        Website_name= "{website_name}",
                        consumer_key = "{username}",
                        consumer_secret = "{consumer_secret}",
                        Category_name = "{category_name}",
                    WHERE ID = 1
                    
                    ''')

def reset_data():
    cur.execute('''
                    UPDATE Postdata
                    SET
                        Website_name = 'https://ebookwise.com/',
                        consumer_key = ''ck_2f9c3979e726fe187d91be14d5156358191f55eb',
                        consumer_secret = 'cs_bc39de27b69cd558bb33199ea23472c1a3b5e429',
                        Category_name = 'category name', 
                    WHERE ID = 1
                    ''')
    window.destroy()

def operation_start():
    thread = threading.Thread(target=operation_start_thread)
    thread.start()

def operation_start_thread():
    website_url = website_entry.get()
    Username = username_entry.get()
    consumer_secret = consumer_secret_entry.get()
    category_name = category.get()
    status_value = status.get()



    i = 1
    keyword_list = keyword_input.get('1.0', 'end-1c')
    all_keywords = keyword_list.splitlines()
    output.delete('0.0', END)
    output.insert('0.0', '>>> Start Working...\n')
    for keyword in all_keywords:
        pass
        i += 1

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


if __name__== '__main__':
    window.mainloop()

con.commit()
cur.close()