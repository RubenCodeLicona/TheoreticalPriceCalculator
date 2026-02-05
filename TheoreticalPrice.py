import math
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv






def parse_number(s: str) -> float:
    return float(s.strip().replace(',', '.'))


def interp_yield_curve(x0, y0, x1, y1, x, ndigits=None):
    if x0 == x1:
        raise ValueError("Los nodos x0 y x1 (Fractions Of Year) no pueden ser iguales")
    m = (y1 - y0) / (x1 - x0)
    y = y0 + m * ( (x) - x0)
    return round(y, ndigits) if ndigits is not None else y
    #return (y)

# def Calculation_date(Today_Date, EXP_Date):
#     Today_Date = datetime(Today_Date)
#     EXP_Date = datetime(EXP_Date)
#     Number_TodayDay = Today_Date.timetuple().tm_yday
#     Number_EXPDay = EXP_Date.timetuple().tm_yday
#     return (Number_EXPDay - Number_TodayDay)/360
def Calculation_date(Today_Date, EXP_Date): #Provisional
    return (EXP_Date - Today_Date)/360

## Calculation for Index Future
def Calculation_Index_Future(i,T,S,var1):
    TP= S * ( 1 + ( (i-var1) * T ))
    return TP

## Calculation for Equity Future
def Calculation_Equity_Future(i,T,S,monto,FY,curva):
    D = (monto * math.exp(-FY * curva))
    TP= (S - D) * ( 1 + (i*T))
    print("Valor de D:",D)
    print("Valor de FY:",FY)
    print("Valor de Curva:",curva)
    print("Valor de T:",T)
    return TP

## Calculation for Equity Future
def Calculation_FX_Future(i,T,S,d):
    TP= (S - d)* (1+(i*T))
    return TP
#def Calculation_FX_Future(i,T,S,d):
 #   TP= S * (1+(i-d)*T)
  #  return TP

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Theoretical Price Calculation       (:))")
        self.geometry("620x620")
        self.resizable(True, True)

        main = ttk.Frame(self, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

#Definition of the names used for creater the
        self.x0_var = tk.StringVar()        # Fractions Of Year (x0)
        self.y0_var = tk.StringVar()        # Annualized Rate (y0)
        self.x1_var = tk.StringVar()        # Fractions Of Year (x1)
        self.y1_var = tk.StringVar()        # Annualized Rate (y1)
        self.x_var  = tk.StringVar()        # Fractions Of Year objetivo (T/360) #Maturity date MD
        self.TD_var  = tk.StringVar()      # Today's day 
        self.S_var  = tk.StringVar()        # S
        self.var1_var  = tk.StringVar()     #entry used for d
        self.var2_var  = tk.StringVar()     #entry used for Amount
        self.var3_var  = tk.StringVar()     #entry used for FY
        self.ANNR_var  = tk.StringVar()     #entry used for ANN_R
        self.i2_var  = tk.StringVar()       #entry used for i2
        self.combo_var = tk.StringVar()     # Variable para el combobox
        self.nd_var = tk.IntVar(value=16)

#definition of the labes for the Entries 
        rows = [
            ("Fractions Of Year x₀", 0), ("Annualized Rate y₀", 1),
            ("Fractions Of Year x₁", 2), ("Annualized Rate y₁", 3),
            ("Date of Maturity date", 4), ("Today's date",5), ("Decimales", 6), ("Price (S)", 7)
        ]
#Definition for the entries. 
        for label, r in rows:
            ttk.Label(main, text=label+":").grid(row=r+1, column=0, sticky="e", padx=(0,8), pady=4)
        
        ttk.Entry(main, textvariable=self.x0_var, width=24).grid(row=1, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.y0_var, width=24).grid(row=2, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.x1_var, width=24).grid(row=3, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.y1_var, width=24).grid(row=4, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.x_var,  width=24).grid(row=5, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.TD_var,  width=24).grid(row=6, column=1, sticky="w")

        tk.Spinbox(main, from_=0, to=50, textvariable=self.nd_var, width=6).grid(row=7, column=1, sticky="w")
        ttk.Entry(main, textvariable=self.S_var,  width=24).grid(row=8, column=1, sticky="w")
##############################################################################################################        
        #definitio of the boxex that will be hid
        self.var1_label= ttk.Label(main, text="Dividend rate (d)")    # Define el nombre que se muestra en a interfaz de la casilla 
        self.var1_label.grid(row=13, column=0, sticky="w", padx=(0,0), pady=0) 
        self.var1_label.grid_remove() #No se muestre 
        self.var1_entry= ttk.Entry(main, textvariable=self.var1_var,  width=20)
        self.var1_entry.grid(row=13, column=0, sticky="e",padx=(0,0), pady=0)
        self.var1_entry.grid_remove()
        # La definicion del segundo combo (Etiquetas y su entrada)
        self.var2_label= ttk.Label(main, text="Dividend Amount")    # Define el nombre que se muestra en a interfaz de la casilla 
        self.var2_label.grid(row=13, column=0, sticky="w", padx=(0,0), pady=0) 
        self.var2_label.grid_remove() #No se muestre 
        self.var2_entry= ttk.Entry(main, textvariable=self.var2_var,  width=20)
        self.var2_entry.grid(row=13, column=1, sticky="e")
        self.var2_entry.grid_remove()
        ### Definiendo las puras etiqueta
        self.FY_label= ttk.Label(main, text="Payment Date")    # Define el nombre que se muestra en a interfaz de la casilla 
        self.FY_label.grid(row=13, column=1, sticky="w", padx=(10,5), pady=0) 
        self.FY_label.grid_remove() #No se muestre
        #
        self.i2_label= ttk.Label(main, text="i2")    # Define el nombre que se muestra en a interfaz de la casilla 
        self.i2_label.grid(row=13, column=0, sticky="w", padx=(0,0), pady=0) 
        self.i2_label.grid_remove() #No se muestre  


        ttk.Label(main, text="x = Fractions Of Year, y = Annualized Rate.", foreground="#555").grid(row=0, column=0, columnspan=2, sticky="w", pady=(2,8))

        btns = ttk.Frame(main)
        btns.grid(row=9, column=0, columnspan=2, pady=6, sticky="w")
        ttk.Button(btns, text="Calculate Values", command=self.on_calc).pack(side=tk.LEFT)
        
#Name
        ttk.Label(main,text="Interpolation (i): ", foreground="#555").grid(row=10, column=0, columnspan=2, sticky="w", pady=(10,8))
        self.out_i = tk.Text(main, height=4, width=70)
##Definition of the box where the i result will be showed. 
        self.out_i.grid(row=11, column=0, columnspan=2, pady=(6,0))
        self.out_i.configure(state=tk.DISABLED)

 ##insertar un menu con las opciones a calcular de los instrumentos para el tipo de calculo que deseas realizar

        ### Dropdown options  Setup 
        instruments = ["Index Future", "Equity Futuro", "FX Future", "Pinapple", "Cherry"]
        cb = ttk.Combobox(main, values=instruments, textvariable=self.combo_var, width=34)
        cb.grid(row=12, column=0, columnspan=3, pady=6, sticky="w")
        cb.set("Select instrument type to calculate")
        cb.bind("<<ComboboxSelected>>", self.instrument_Selected)

##Definition of the box where the TH_PR result will be showed.
        ttk.Label(main, text="Theoretical Price Result: ", foreground="#555").grid(row=15, column=0, columnspan=2, sticky="w", pady=(2,8))
        self.out = tk.Text(main, height=4, width=70)
        self.out.grid(row=16, column=0, columnspan=2, pady=(6,0))
        self.out.configure(state=tk.DISABLED)

    def instrument_Selected(self, event =None):
    
#Select what happen when is selected each instrument 
        selected = self.combo_var.get()

        if selected == "Index Future":
            self.var1_label.grid()
            self.var1_entry.grid()
            
            self.i2_label.grid_remove() #No se muestre
            self.var2_label.grid_remove() #No se muestre
            self.FY_label.grid_remove() #No se muestre
            self.var2_entry.grid_remove() #Oculta la entrada

            
        elif selected == "Equity Futuro":
            self.var2_label.grid()
            self.var1_entry.grid()
            self.FY_label.grid()
            self.var2_entry.grid()

            self.var1_label.grid_remove() #No se muestre
            self.i2_label.grid_remove() #No se muestre
            

        elif selected == "FX Future":
            self.i2_label.grid()
            self.var1_entry.grid()
            
            self.var1_label.grid_remove() #No se muestre
            self.var2_label.grid_remove() #No se muestre
            self.FY_label.grid_remove() #No se muestre
            self.var2_entry.grid_remove()
            
        else:
            self.var1_label.grid_remove()
            self._entry.grid_remove()
        return selected

    def on_calc(self):
        try:
            x0 = parse_number(self.x0_var.get())
            y0 = parse_number(self.y0_var.get())
            x1 = parse_number(self.x1_var.get())
            y1 = parse_number(self.y1_var.get())
            x  = parse_number(self.x_var.get())  #Cambiar por MD 
            TD_Date =parse_number(self.TD_var.get())
            S  = parse_number(self.S_var.get())
            #d  = parse_number(self.d_var.get())
            var1  = parse_number(self.var1_var.get()) 
            #var2  = parse_number(self.var2_var.get())
            #var3  = parse_number(self.var3_var.get())
            nd = int(self.nd_var.get())
            nd = 0 if nd < 0 else 50 if nd > 50 else nd

            #Calculo de T (Time to Maturity)
            T = Calculation_date(TD_Date,x)
            

            #Calculo para  i 
            y = interp_yield_curve(x0, y0, x1, y1, T, ndigits=nd)
            self.write_out(f"(Yield Curve) i = {y:.{nd}f}")
            
            # print("Valor de T:",T)
            # print("Valor de S:",S)
            # print("Valor de d:",var1)
            

            #Calculo para TH
            selected = self.combo_var.get() 

            if selected == "Index Future":
                result=Calculation_Index_Future(y,T,S,var1)
                self.write_out2(f"Theoretical Price for an Index Future Result = {result:.{nd}f}")
       
                
            
            elif selected == "Equity Futuro":
                var2  = parse_number(self.var2_var.get())
                FX = Calculation_date(TD_Date,var2)

                curve= interp_yield_curve(x0, y0, x1, y1, FX, ndigits=nd)
                result=Calculation_Equity_Future(y,T,S,var2,FX,curve)
                self.write_out2(f"Theoretical Price for an Index Future Result = {result:.{nd}f}")
                
                
            
            elif selected == "FX Future":
                result=Calculation_FX_Future(y,T,S,var1)
                self.write_out2(f"Theoretical Price for an Index Future Result = {result:.{nd}f}")
            

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ## El recuadro para el resultado de i.
    def write_out(self, text: str):
        self.out_i.configure(state=tk.NORMAL)
        self.out_i.delete("1.0", tk.END)
        self.out_i.insert(tk.END, text)
        self.out_i.configure(state=tk.DISABLED)
    ## El nuevo recuadro para el resultado del Theoretical Price.
    def write_out2(self, text: str):
        self.out.configure(state=tk.NORMAL)
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, text)
        self.out.configure(state=tk.DISABLED)
    
    

if __name__ == "__main__":
    App().mainloop()

