import tkinter as tk
from tkinter import ttk
import random
import time
import statistics #M libreria tiempos

class FCFS:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación FCFS")
        self.root.geometry("800x600")
        
        self.processes = []
        self.current_process = None
        self.process_index = 0
        self.global_count = 0
        self.finished_processes = 0
        self.idle_count = 0
        self.busy_count = 0
        self.after_id = None

        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.cpu_title = ttk.Label(root,text="CPU",font=("Arial",12))
        self.cpu_title.place(x=650,y=30)

        self.counter_label = ttk.Label(root, text="Tiempo: 0", font=("Arial", 10))
        self.counter_label.place(x=650, y=60) 

        self.idle_label = ttk.Label(root,text="Idle: 0",font=("Arial",10))
        self.idle_label.place(x=650,y=80)

        self.busy_label = ttk.Label(root,text="Ocupado: 0",font=("Arial",10))
        self.busy_label.place(x=650,y=100)

        self.tiempo_respuesta_label = ttk.Label(root, text="Tiempo de Respuesta", font=("Arial", 11))
        self.tiempo_respuesta_label.place(x=620, y=140)

        self.min_label = ttk.Label(root, text="Min: 0", font=("Arial", 10))
        self.min_label.place(x=650, y=160)

        self.media_label = ttk.Label(root, text="Media: 0", font=("Arial", 10))
        self.media_label.place(x=650, y=180)

        self.max_label = ttk.Label(root, text="Max: 0", font=("Arial", 10))
        self.max_label.place(x=650, y=200)

        self.standar_desviation_label = ttk.Label(root, text="Desviación Estándar: 0", font=("Arial", 10))
        self.standar_desviation_label.place(x=620, y=220)

        #M etiquetas time around
        self.tiempo_turnaround_label = ttk.Label(root, text="Tiempo Turnaround", font=("Arial", 11))
        self.tiempo_turnaround_label.place(x=620, y=250)

        self.min2_label = ttk.Label(root, text="Min: 0", font=("Arial", 10))
        self.min2_label.place(x=650, y=270)

        self.media2_label = ttk.Label(root, text="Media: 0", font=("Arial", 10))
        self.media2_label.place(x=650, y=290)

        self.max2_label = ttk.Label(root, text="Max: 0", font=("Arial", 10))
        self.max2_label.place(x=650, y=310)

        #Metiquetas desviacion estandar
        self.standar_desviation2_label = ttk.Label(root, text="Desviación Estándar: 0", font=("Arial", 10))
        self.standar_desviation2_label.place(x=620, y=330)
        
        self.add_button = ttk.Button(self.root, text="Agregar Proceso", command=self.add_process)
        self.add_button.pack()

        self.start_button = ttk.Button(self.root, text="Iniciar", command=self.start_simulation)
        self.start_button.pack()

        self.restart_button = ttk.Button(self.root, text="Reanudar", command=self.restart_process)
        self.restart_button.pack()

        self.pause_button = ttk.Button(self.root, text="Pausar", command=self.pause_process)
        self.pause_button.pack()

        self.stop_button = ttk.Button(self.root, text="Matar", command=self.kill_process)
        self.stop_button.pack()

        self.update_canvas()

    # Cuenta la cantidad de procesos listos
    def count_ready_processes(self):
        count = 0
        for process in self.processes:
            if process.state == "Listo" or process.state == "Ejecucion":
                count += 1
        return count
    

    # Encuentra el índice del proceso que se encuentre listo
    def find_ready_process(self):
        index = 0


        for process in self.processes:
            if process.state == "Listo":
                return index
            else:
                index += 1
                
    # Encuentra el proceso con menor tiempo esperado
    def find_minor_process(self):
        minor = 1000

        for process in self.processes:
            if minor > process.expected_time:
                minor = process.expected_time

        return minor
    
    # Encuentra el proceso con menor tiempo rotativo
    def find_minor_total_time(self):
        minor = 1000

        for process in self.processes:
            if minor > process.total_time:
                minor = process.total_time

        return minor
    
    # Encuentra el proceso con mayor tiempo rotativo
    def find_major_total_time(self):
        major = 0

        for process in self.processes:
            if major < process.total_time:
                major = process.total_time

        return major
    
    def average_turnaorund_time(self):
        average = 0
        total = 0

        for process in self.processes:
            total += process.total_time

        average = total / len(self.processes)

        return round(average,2)

    def add_process(self):
        process = Process()
        process.name = "Proceso " + str(len(self.processes) + 1)
        process.ID = self.process_index
        self.processes.append(process)
        self.update_canvas()


    def restart_process(self):
        # Si el indice general llego a la cantidad de procesos...
        # busca el proceso que se pauso y lo ejecuta
        if self.count_ready_processes() > 0:
            if self.current_process:
                self.root.after_cancel(self.current_process.after_id)
                self.current_process.state = "Listo"

            index = self.find_ready_process()
            self.current_process = self.processes[index]
            self.current_process.state = "Listo"
            self.process_index = index
            self.update_canvas()
            self.run_process()


    def start_simulation(self):
        if self.global_count == 0:
            self.root.after(1000, self.increment_global_count)
            
        minor_time = self.find_minor_process()
        self.min_label.config(text="Min: {}".format(minor_time))

        #M calcula y muestra el tiempo de respuesta
        tiempo_respuesta = self.calculate_response_time()
        self.update_response_labels(tiempo_respuesta)

        #M calcula y muestra el tiempo tour around
        tiempo_turnaround = self.calculate_turnaround_time()
        self.update_turnaround_labels(tiempo_turnaround)
        
        if not self.current_process:    
            if self.process_index < len(self.processes):
                self.current_process = self.processes[self.process_index]
                self.process_index += 1
                self.update_canvas()
                self.run_process()
            else:
                minor_rotative_time = self.find_minor_total_time()
                self.min2_label.config(text="Min: {}".format(minor_rotative_time))
                media_time = self.average_turnaorund_time()
                self.media2_label.config(text="Media: {}".format(media_time))
                major_rotative_time = self.find_major_total_time()
                self.max2_label.config(text="Max: {}".format(major_rotative_time))

    def calculate_response_time(self):
        response_times = [process.progress - process.arrival_time for process in self.processes] #M calcula los tiempos de respuesta. (resta el tiempo de llegada)
        return response_times #M tiempos de respuesta calculados

    def calculate_turnaround_time(self):
        turnaround_times = [process.total_time for process in self.processes] #M tiempo total de los procesos
        return turnaround_times#M tiempos tour around
    
    #M calculan los tiempos con la biblioteca stastics
    def update_response_labels(self, response_times):
        min_resp = min(response_times)
        max_resp = max(response_times)
        mean_resp = statistics.mean(response_times)
        std_dev_resp = statistics.stdev(response_times)
        #M actualizacion de los labels
        self.min_label.config(text="Min: {}".format(min_resp))
        self.media_label.config(text="Media: {:.2f}".format(mean_resp))
        self.max_label.config(text="Max: {}".format(max_resp))
        self.standar_desviation_label.config(text="Desviación Estándar: {:.2f}".format(std_dev_resp))

    #M calculan los tiempos con la biblioteca stastics
    def update_turnaround_labels(self, turnaround_times):
        min_turnaround = min(turnaround_times)
        max_turnaround = max(turnaround_times)
        mean_turnaround = statistics.mean(turnaround_times)
        std_dev_turnaround = statistics.stdev(turnaround_times)
        #M actualizacion de los labels
        self.min2_label.config(text="Min: {}".format(min_turnaround))
        self.media2_label.config(text="Media: {:.2f}".format(mean_turnaround))
        self.max2_label.config(text="Max: {}".format(max_turnaround))
        self.standar_desviation2_label.config(text="Desviación Estándar: {:.2f}".format(std_dev_turnaround))

    def run_process(self):
        if self.current_process:

            for process in self.processes:
                if process.state != "Terminado" and process.state != "Muerto":
                    process.total_time += 1

            if self.current_process.progress < self.current_process.expected_time:
                if self.process_index == 0:
                    if self.processes[self.process_index].state not in ["Muerto", "Terminado"]:
                        self.processes[self.process_index].state = "Ejecucion"
                else:
                    if self.current_process.state not in ["Muerto", "Terminado"]:
                        self.current_process.state = "Ejecucion"

                if self.current_process.pause_flag:
                    self.current_process.pause_flag = False
                    self.current_process.state = "Listo"
                    # Guardamos el proceso del proceso pausado, debido a que se usará cuando vuelva su turno
                    self.processes[self.process_index - 1].progress = self.current_process.progress
                    self.current_process = None
                    self.start_simulation()
                elif self.processes[self.process_index - 1].state == "Muerto":
                    self.current_process = None
                    self.start_simulation()

                else:
                    self.current_process.progress += 1

                    self.busy_label.config(text="Ocupado: {}".format(self.busy_count))
                    self.busy_count += 1

                    self.update_canvas()
                    self.current_process.after_id = self.root.after(1000, self.run_process)
            else:
                if self.process_index == 0:
                    self.processes[self.process_index].state = "Terminado"
                    self.current_process = None
                    self.start_simulation()
                else:
                    self.processes[self.process_index - 1].state = "Terminado"
                    self.finished_processes += 1
                    self.current_process = None
                    self.update_canvas()
                    self.start_simulation()

                    if self.count_ready_processes() == 0:
                        self.after_id = self.root.after(1000,self.increment_idle_count)
                    
    # Activa una bandera cuando el proceso actual es pausado
    def pause_process(self):
        if self.current_process:
            self.current_process.pause_flag = True


    def kill_process(self):
        # Matar el proceso actual y reiniciar
        self.root.after_cancel(self.current_process.after_id)
        self.processes[self.process_index - 1].state = "Muerto"
        self.current_process = None
        self.update_canvas()
        self.start_simulation()


    def update_canvas(self):
        self.canvas.delete("all")
        for i, process in enumerate(self.processes):
            x1, y1 = 50, 50 + i * 50
            x2, y2 = x1 + process.progress * 10, y1 + 30

            if process.state == "Listo":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                self.canvas.create_text(x1, y1 - 10, anchor="w", text=process.name)
            elif process.state == "Terminado":
                if process.progress >= process.expected_time:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    self.canvas.create_text(x1, y1 - 10, anchor="w", text=process.name)
            elif process.state == "Ejecucion":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                self.canvas.create_text(x1, y1 - 10, anchor="w", text=process.name)
            elif process.state == "Muerto":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                self.canvas.create_text(x1, y1 - 10, anchor="w", text=process.name+" - Muerto")

    def increment_global_count(self):
        self.global_count += 1
        self.counter_label.config(text="Tiempo: {}".format(self.global_count))
        self.root.after(1000, self.increment_global_count)


    def increment_idle_count(self):
        #! Falta solucionar el aumento de idle cuando el último proceso está muerto
        if self.count_ready_processes() > 0:
            return

        self.root.after_cancel(self.after_id)
        self.idle_label.config(text="Idle: {}".format(self.idle_count))
        self.idle_count += 1
        self.after_id = self.root.after(1000,self.increment_idle_count)


class Process:
    def __init__(self):
        self.ID = -1
        self.name = "-"
        self.arrival_time = -1
        self.expected_time = 10
        self.expected_time = random.randint(1,6)
        self.start_time = -1
        self.finish_time = -1
        self.total_time = 0
        self.state = "Listo"
        self.progress = 0
        self.pause_flag = False
        self.after_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = FCFS(root)
    root.mainloop()