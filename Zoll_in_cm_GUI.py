import ttkbootstrap as ttk
import tkinter as tk

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoll/CM Rechner")
        self.root.geometry("400x400")
        self.root.maxsize(400, 400)
        self.root.minsize(400, 400)

        self.entry_frame = ttk.Frame(root)
        self.entry_frame.pack(side='top')


        ttk.Label(self.entry_frame).grid(row=0, column=1)
        self.output_widget = ttk.Text(self.entry_frame, font=("Helvetica", 25), height=1, width=10, wrap=tk.WORD)
        self.output_widget.grid(row=0, column=1, pady=20)

        ttk.Label(self.entry_frame, text='Gib einen wert in cm ein').grid(row=1, column=1)
        self.entry_zoll = ttk.Entry(self.entry_frame)
        self.entry_zoll.grid(row=2, column=1, pady=5)

        ttk.Label(self.entry_frame, text='Gib einen wert in Zoll ein').grid(row=4, column=1)
        self.entry_cm = ttk.Entry(self.entry_frame)
        self.entry_cm.grid(row=5, column=1, pady=5)

        ttk.Label(self.entry_frame, text='Gib deine Bogenlänge an um die Sehnenlänge in Zoll zu erhalten').grid(row=7, column=1)
        self.entry_bow = ttk.Entry(self.entry_frame)
        self.entry_bow.grid(row=8, column=1, pady=5)

        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_Zoll).grid(row=3, column=1, pady=5)
        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_cm).grid(row=6, column=1, pady=5)
        ttk.Button(self.entry_frame, text='Berechnen', command=self.output_bow).grid(row=9, column=1, pady=5)


    def data_get_bow(self):
        bow = self.entry_bow.get()
        bow = float(bow) - 3
        self.bow_result = bow

    def output_bow(self):
        self.data_get_bow()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.bow_result} Zoll')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)  

    def data_get_cm(self):
        cm = self.entry_cm.get()
        cm = round(float(cm) / 0.3937, 2)
        self.cm_result = cm

    def output_cm(self):
        self.data_get_cm()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.cm_result} cm')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)


    def data_get_Zoll(self):
        zoll = self.entry_zoll.get()
        zoll = round(float(zoll) * 0.3937, 2)
        self.zoll_result = zoll

    def output_Zoll(self):
        self.data_get_Zoll()
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.insert(ttk.END, f'{self.zoll_result} Zoll')  
        self.output_widget.configure(fg="yellow")
        self.output_widget.see(ttk.END)  

        


root = ttk.Window(themename="solar")
main = Main(root)
root.mainloop()