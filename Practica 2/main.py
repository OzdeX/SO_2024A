import tkinter as tk
from tkinter import ttk, END, messagebox

######## OPERACIONES ########

def potencia(base, exponente):
    return base ** exponente

def porcentaje(numero, porcentaje):
    return numero * (porcentaje / 100)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

def raiz(numero):
    return numero ** 0.5

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b != 0:
        return a / b
    else:
        messagebox.showerror("Error", "División por cero no permitida")


######## CONVERSIONES ########
        
def dec_a_bin(decimal):
    parte_entera = int(decimal)
    return bin(parte_entera)[2:]

def dec_a_oct(decimal):
    return oct(decimal)[2:]

def dec_a_hex(decimal):
    return hex(decimal)[2:]

def bin_a_dec(binario):
    return int(binario, 2)

def oct_a_dec(octal):
    return int(octal, 8)

def hex_a_dec(hexadecimal):
    return int(hexadecimal, 16)


######## CALCULADORA ########

def actualizar_resultados():
    contenido = txtDisplay.get()

    if modo_actual == "DEC":
        resultado = float(contenido)
    elif modo_actual == "OCT":
        resultado = oct_a_dec(dec_a_oct(int(float(contenido))))
    elif modo_actual == "HEX":
        resultado = hex_a_dec(dec_a_hex(int(float(contenido))))
    elif modo_actual == "BIN":
        resultado = bin_a_dec(dec_a_bin(float(contenido)))

    txtDec.delete(0, END)
    txtDec.insert(0, str(resultado))

    txtOct.delete(0, END)
    txtOct.insert(0, dec_a_oct(int(resultado)))

    txtHex.delete(0, END)
    txtHex.insert(0, dec_a_hex(int(resultado)))

    txtBin.delete(0, END)
    txtBin.insert(0, dec_a_bin(int(resultado)))

    txtDisplay.delete(0, END)


def cambiar_modo(modo):
    global modo_actual
    modo_actual = modo
    txtDisplay.delete(0, END)
    txtDec.delete(0, END)
    txtOct.delete(0, END)
    txtHex.delete(0, END)
    txtBin.delete(0, END)


    # if modo_actual == "DEC":
    #     txtBin.grid()
    #     txtHex.grid()
    #     txtOct.grid()
    if modo == "DEC":
        txtDec.place(x=60, y=60)
        txtOct.place(x=60, y=90)
        txtHex.place(x=60, y=120)
        txtBin.place(x=60, y=150)
    elif modo == "OCT":
        txtHex.place_forget()
        txtBin.place_forget()
        txtDec.place(x=60, y=60)
        txtOct.place(x=60, y=90)
    elif modo == "HEX":
        txtOct.place_forget()
        txtBin.place_forget()
        txtDec.place(x=60, y=60)
        txtHex.place(x=60, y=120)
    elif modo == "BIN":
        txtOct.place_forget()
        txtHex.place_forget()
        txtDec.place(x=60, y=60)
        txtBin.place(x=60, y=150)

def operador(x):
    global signo, aux
    contenido = txtDisplay.get()

    try:
        if modo_actual == "DEC":
            aux = float(contenido)
        elif modo_actual == "OCT":
            aux = oct_a_dec(contenido)
        elif modo_actual == "HEX":
            aux = hex_a_dec(contenido)
        elif modo_actual == "BIN":
            aux = bin_a_dec(contenido)
        
        if x == "!":
            resultado = factorial(float(aux))
            txtDisplay.delete(0, END)
            txtDisplay.insert(0, str(resultado))
            actualizar_resultados()
        elif x == "√":
            resultado = raiz(float(aux))
            txtDisplay.delete(0, END)
            txtDisplay.insert(0, str(resultado))
            actualizar_resultados()
        else:
            signo = x
            txtDisplay.delete(0, END)

    except ValueError:  
        messagebox.showerror("Error", "Valor inválido")

def operacion():
    global signo, aux
    contenido = txtDisplay.get()

    try:
        if modo_actual == "DEC":
            resultado = float(contenido)
        elif modo_actual == "OCT":
            resultado = oct_a_dec(contenido)
        elif modo_actual == "HEX":
            resultado = hex_a_dec(contenido)
        elif modo_actual == "BIN":
            resultado = bin_a_dec(contenido)

        if signo == "+":
            resultado = suma(aux, resultado)
        elif signo == "-":
            resultado = resta(aux, resultado)
        elif signo == "*":
            resultado = multiplicacion(aux, resultado)
        elif signo == "/":
            resultado = division(aux, resultado)
        elif signo == "^":
            resultado = potencia(aux, resultado)
        elif signo == "%":
            resultado = porcentaje(aux, resultado)
        elif signo == "!":
            resultado = factorial(float(aux))
        elif signo == "√":
            resultado = raiz(aux)

        txtDisplay.delete(0, END)
        txtDisplay.insert(0, str(resultado))
        aux = 0
        actualizar_resultados()
    
    except ValueError:
        txtDisplay.delete(0, END)
        messagebox.showerror("Error", "Entrada inválida")


""" 
DESDE AQUÍ COMIENZA LA INTERFAZ
"""

######## CALCULADORA - ETIQUETAS Y ESPACIOS DE TEXTO ########

root = tk.Tk()
root.title("Calculadora")
root.geometry("400x450")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", padding=5, font=('Helvetica', 12))
style.configure("TEntry", padding=5, font=('Helvetica', 14))

aux = 0
signo = ""
resultado = 0
modo_actual = "DEC"

txtDisplay = ttk.Entry(root, style="TEntry")
txtDisplay.place(x=10, y=20, width=380)

tk.Label(root, text="DEC:", font=('Helvetica', 12)).place(x=10, y=60)
txtDec = ttk.Entry(root, style="TEntry")
txtDec.place(x=60, y=60)

tk.Label(root, text="OCT:", font=('Helvetica', 12)).place(x=10, y=90)
txtOct = ttk.Entry(root, style="TEntry")
txtOct.place(x=60, y=90)

tk.Label(root, text="HEX:", font=('Helvetica', 12)).place(x=10, y=120)
txtHex = ttk.Entry(root, style="TEntry")
txtHex.place(x=60, y=120)

tk.Label(root, text="BIN:", font=('Helvetica', 12)).place(x=10, y=150)
txtBin = ttk.Entry(root, style="TEntry")
txtBin.place(x=60, y=150)


######## CALCULADORA - BOTONES ########

btnSuma = ttk.Button(root, text="+", command=lambda: operador("+"))
btnSuma.place(x=280, y=200, width=40, height=40)

btnResta = ttk.Button(root, text="-", command=lambda: operador("-"))
btnResta.place(x=330, y=200, width=40, height=40)

btnMultiplicacion = ttk.Button(root, text="*", command=lambda: operador("*"))
btnMultiplicacion.place(x=280, y=250, width=40, height=40)

btnDivision = ttk.Button(root, text="/", command=lambda: operador("/"))
btnDivision.place(x=330, y=250, width=40, height=40)

btnIgual = ttk.Button(root, text="=", command=operacion)
btnIgual.place(x=280, y=300, width=90, height=40)

btnPotencia = ttk.Button(root, text="^", command=lambda: operador("^"))
btnPotencia.place(x=10, y=200, width=40, height=40)

btnPorcentaje = ttk.Button(root, text="%", command=lambda: operador("%"))
btnPorcentaje.place(x=60, y=200, width=40, height=40)

btnFactorial = ttk.Button(root, text="!", command=lambda: operador("!"))
btnFactorial.place(x=10, y=250, width=40, height=40)

btnRaiz = ttk.Button(root, text="√", command=lambda: operador("√"))
btnRaiz.place(x=60, y=250, width=40, height=40)

btnDec = ttk.Button(root, text="DEC", command=lambda: cambiar_modo("DEC"))
btnDec.place(x=10, y=370, width=70, height=40)

btnOct = ttk.Button(root, text="OCT", command=lambda: cambiar_modo("OCT"))
btnOct.place(x=90, y=370, width=70, height=40)

btnHex = ttk.Button(root, text="HEX", command=lambda: cambiar_modo("HEX"))
btnHex.place(x=170, y=370, width=70, height=40)

btnBin = ttk.Button(root, text="BIN", command=lambda: cambiar_modo("BIN"))
btnBin.place(x=250, y=370, width=70, height=40)

root.mainloop()
