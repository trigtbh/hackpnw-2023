import tkinter

class EventInput:
    def __init__(self, master):
        self.master = master
        self.frame = tkinter.Frame(self.master)
        self.frame.pack()

        self.button = tkinter.Button(self.frame, text="Quit", fg="red", command=self.frame.quit)
        self.button.pack(side=tkinter.LEFT)

        self.text = tkinter.Text(root, height=10,
                width=35,
                bg="gray",
                fg="red")  # <- HERE
        self.text.pack(side=tkinter.RIGHT)

    def say_hi(self):
        print("hi there, everyone!")

root = tkinter.Tk()
root.configure(background='#e88eed')
b = EventInput(root)
root.mainloop()