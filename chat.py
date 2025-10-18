from tkinter import *

from lib import llm

def reply():
    prompt = textarea_1.get(1.0, END) 
    prompt += f'/no_think'
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    textarea_2.delete(1.0, END)
    textarea_2.insert(END, reply)

root = Tk() 

width = 100
height = 60

frame_1 = Frame(root)
frame_1.pack(side=LEFT)
textarea_1 = Text(frame_1, width=width, height=height)
textarea_1.pack()
button = Button(frame_1, text='reply', command=reply)
button.pack()

frame_2 = Frame(root)
frame_2.pack(side=LEFT)
textarea_2 = Text(frame_2, width=width, height=height)
textarea_2.pack()

root.mainloop()
