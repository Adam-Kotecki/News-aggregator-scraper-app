import tkinter as tk
from tkinter import ttk
from tkinter import Entry
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from sys import exit
import requests
from bs4 import BeautifulSoup
import os

root = tk.Tk()

root.geometry('400x500')
root.resizable(False, False)
root.title('Scraping news app')

image1 = Image.open("scraping news.png").resize((400, 100))
test = ImageTk.PhotoImage(image1)

label1 = ttk.Label(image=test)
label1.place(x = 0, y = 0)


# label - select news aggregator
label2 = ttk.Label(text="Please select news aggregator:")
#label.pack(fill=tk.X, padx=5, pady=5)
label2.place(x=5 , y=120)

# create a combobox for selecting aggregator
selected_website = tk.StringVar()
website = ttk.Combobox(root, textvariable=selected_website)
website['values'] = ('Hacker News', 'Lobsters')

# prevent typing a value
website['state'] = 'readonly'
website.place(x=5, y=140)

# label - type keyword
label3 = ttk.Label(text="Keyword:")
#label2.pack(fill=tk.X, padx=5, pady=5)
label3.place(x=5 , y=170)

# textbox for keyword
keyword = tk.StringVar()
textbox1 = tk.Entry(root, width = 52, textvariable = keyword)
textbox1.place(x=5, y=190)

selected_pages = tk.IntVar()

# combobox for number of pages
hackers = ttk.Combobox(root, textvariable=selected_pages)
hackers['values'] = ('30', '60', '90', '120', '150')
hackers['state'] = 'readonly'

lobsters = ttk.Combobox(root, textvariable=selected_pages)
lobsters['values'] = ('25', '50', '75', '100', '125')
lobsters['state'] = 'readonly'

# bind the selected value changes
def website_changed(event):
    label3 = ttk.Label(text="Number of recent pages to be searched:")
    label3.place(x=5, y=220)
    
    if selected_website.get() == 'Hacker News':
        lobsters.place_forget()
        hackers.place(x=5, y=240)
        hackers.set('')
    else:
        hackers.place_forget()
        lobsters.place(x=5, y=240)
        lobsters.set('')
        
website.bind('<<ComboboxSelected>>', website_changed)

# label - type number of points/votes
label4 = ttk.Label(text="Minimal number of points/votes:")
label4.place(x=5 , y=270)

# textbox for votes
provided_points = tk.IntVar()
textbox2 = tk.Entry(root, width = 52, textvariable = provided_points)
textbox2.place(x=5, y=290)

label5 = ttk.Label(text="Save file as:")
label5.place(x=5, y=320)

file_name = tk.StringVar()

textbox3 = tk.Entry(root, width = 52, textvariable = file_name)
textbox3.place(x=5, y=340)
textbox3.insert(tk.END, "Daily content")


def clear():
    if selected_website.get() == 'Hacker News':
        hackers.set('')
        website.set('')
        textbox1.delete(0,"end")
        textbox2.delete(0,"end")
    if selected_website.get() == 'Lobsters':
        lobsters.set('')
        website.set('')
        textbox1.delete(0,"end")
        textbox2.delete(0,"end")
    if selected_website.get() == "":
        if hackers.winfo_exists() == 1:
            hackers.set('')
        if lobsters.winfo_exists() == 1:
            lobsters.set('')
        

def scrapp():
    if selected_website.get() == "":
        tk.messagebox.showinfo(message="Please select news aggregator")
        return
    if keyword.get() == "":
        tk.messagebox.showinfo(message="Please type keyword")
        return
    if selected_pages.get() == "":
        tk.messagebox.showinfo(message="Please select number of recent pages to be searched")
        return
    if provided_points.get() == "":
        tk.messagebox.showinfo(message="Please provide minimal number of points/votes")
        return
    if file_name.get() == "":
        tk.messagebox.showinfo(message="Please type file name")
        return
    
    
    if selected_website.get() == 'Hacker News':
        website_link = "https://news.ycombinator.com"
        class1 = '.titleline > a'
        class2 = '.subtext'
    if selected_website.get() == "Lobsters":
        website_link = "https://lobste.rs/"
        class1 = '.u-url'
        class2 = '.score'
    
    res = requests.get(website_link)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select(class1)
    score = soup.select(class2)
    
    stop = 1
    
    if selected_website.get() == 'Hacker News':
        if selected_pages.get() > 30:
            if selected_pages.get() == 60:
                stop = 2
            if selected_pages.get() == 90:
                stop = 3
            if selected_pages.get() == 120:
                stop = 4
            if selected_pages.get() == 150:
                stop = 5
    if selected_website.get() == "Lobsters":
        if selected_pages.get() > 25:
            if selected_pages.get() == 50:
                stop = 2
            if selected_pages.get() == 75:
                stop = 3
            if selected_pages.get() == 100:
                stop = 4
            if selected_pages.get() == 125:
                stop = 5
            
    if selected_website.get() == 'Hacker News':
        web_page = 'https://news.ycombinator.com/?p='
    if selected_website.get() == "Lobsters":
        web_page = 'https://lobste.rs/page/'
    
        
        for page in range(2, stop + 1):
            res = requests.get(web_page + str(page))
            if res.status_code == 200:
                soup2 = BeautifulSoup(res.text, 'html.parser')
                # Extracting only needed data:
                links2 = soup2.select(class1)
                score2 = soup2.select(class2)
                links = links + links2
                score = score + score2
    
    def interesting_content(links, score):
        content = []
        if selected_website.get() == 'Hacker News':
            for index, item in enumerate(links):
                title = item.getText()
                href = item.get('href', None)
                points = score[index].select('.score')
                # extracting only articles with points:
                if len(points) > 0:
                    points_no = int(points[0].getText().replace(' points', ''))
                    # selecting only ones which match criteria:
                if (points_no >= provided_points.get()) and (keyword.get().lower() in title.lower()):
                    content.append({'title': title, 'link': href, 'votes': points_no})
        if selected_website.get() == "Lobsters":
            for index, item in enumerate(links):
                title = item.getText()
                href = item.get('href', None)
                points = score[index].getText()
                # extracting only articles with points:
                #if len(points) > 0:
                points_no = int(points)
                if (points_no >= provided_points.get()) and (keyword.get().lower() in title.lower()):
                        content.append({'title': title, 'link': href, 'votes': points_no})
        write_content(content)
        return content
    
    def write_content(content):
        ind = 1
        username = os.environ.get('USER', os.environ.get('USERNAME'))
        with open('C:\\Users\\' + username + '\\Desktop\\' + file_name.get() + '.txt', 'w') as f:
            for dict in content:
                f.write(str(ind) + ". " + str(dict['title']) + " |votes: " + str(dict['votes']) + "|  " + str(dict['link']) + '\n' )
                ind = ind + 1
    
    interesting_content(links, score)
    tk.messagebox.showinfo(message="Completed")
    

button1 = tk.Button(root, text="OK", command=lambda: scrapp(), width=10, bg="blue4", fg="white", font=("ariel", 12, "bold") )
button1.place(x=5, y=460)

button2 = tk.Button(root, text="Clear", command=lambda: clear(), width=10, bg="blue4", fg="white", font=("ariel", 12, "bold") )
button2.place(x=285, y=460)

root.mainloop()
