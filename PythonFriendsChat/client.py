#Client Side Gui Chat Room

import tkinter as tk,socket as soc,threading as thread
from tkinter import DISABLED,VERTICAL,END,NORMAL



#Define window
root = tk.Tk()
root.title("Chat Client")
root.iconbitmap("")
root.geometry("650x650")
root.resizable(0,0)

#Define image 
icon_img = tk.PhotoImage(file="PeopleFriends.64.png")
send_img = tk.PhotoImage(file="send.png")
connect_image= tk.PhotoImage(file="connected.png", width=24,height=24)
disconect_image= tk.PhotoImage(file="disconected.png")

#Define font and colors
my_font= ('SimSun', 14)
cyan = "#c9c9c9"
black = "#000000"
grow="#a3a3a3"
grow_grow ="#c3c3c3"
root.config(bg=cyan)

#Define soc constants
ENCODER = 'utf-8'
BYTESIZE = 1024
global client_soc


# Automatisch die lokale IP-Adresse ermitteln
def get_local_ip():
    hostname = soc.gethostname()
    ip = soc.gethostbyname(hostname)
	
    return ip

# Beispiel: Connect-Funktion mit automatischer IP
def connect():
    global client_soc

    # Name aus Eingabefeld holen
    name = name_entry.get()
    port = port_entry.get()
 
    # Lokale IP automatisch bestimmen
	
    ip = get_local_ip()
	
    if name and port:
        my_listbox.delete(0, END)
        my_listbox.insert(0, f"{name} versucht Verbindung zu {ip}:{port}...")

        client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        client_soc.connect((ip, int(port)))

        verify_connection(name)

    else:
        my_listbox.insert(0, "Name oder Port fehlt...")

def verify_connection(name):
	'''Verify that the server connection is valid and pass required information'''
	global client_soc

	#Server will send a NAME flag if a valid connection is made
	flag = client_soc.recv(BYTESIZE).decode(ENCODER)

	if flag == 'NAME':
		#Connection was made, send client name and await verification
		client_soc.send(name.encode(ENCODER))
		message = client_soc.recv(BYTESIZE).decode(ENCODER)

		if message:
			#Connection was made, send client name and await
			my_listbox.insert(0,message)
		
			#Change the Button states
			connect_button.config(state=DISABLED)
			disconnect_button.config(state=NORMAL)
			send_button.config(state=NORMAL)

			name_entry.config(state=DISABLED)
			ip_entry.config(state=DISABLED)
			port_entry.config(state=DISABLED)

			#Create a thread to contiuously recieve message from the server
			recieve_thread = thread.Thread(target=recieve_message)
			recieve_thread.start()
		else:
			#No verification nessage was recieved
			my_listbox.insert(0, "Connection not verified. Goodbye....")
			client_soc.close()
	else:
		#No name flag was sent, connection was refused

		my_listbox.insert(0,"Connection refused. Goodbye....")
		client_soc.close()



def disconnect():
	'''Disconnect from the server'''
	#Change the Button states
	connect_button.config(state=NORMAL)
	disconnect_button.config(state=DISABLED)
	send_button.config(state=DISABLED)

	name_entry.config(state=NORMAL)
	ip_entry.config(state=DISABLED)
	port_entry.config(state=DISABLED)
	client_soc.close()




def send_message():
	'''Send a message to the server to be broadcast'''
	global client_soc

	#send

	message = input_entry.get()
	client_soc.send(message.encode(ENCODER))

	#Clear the input entry
	input_entry.delete(0,END)

def recieve_message():
	'''Recieve an incoming message from the server'''
	global client_soc

	while True:
		try:
			#Recive an incoming message from Server
			message = client_soc.recv(BYTESIZE).decode(ENCODER)
			my_listbox.insert(0,message)
		except:
			#AN error occured, disconnect from the server
			my_listbox.insert(0, "Closing the connection. Goodbye...")
			disconnect()
			break




#Define GUI Layout
#Create Frames
info_frame = tk.Frame(root, bg=cyan)
output_frame = tk.Frame(root, bg=cyan)
input_frame = tk.Frame(root, bg=cyan)

info_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

#Info Frame Layout
name_label = tk.Label(info_frame,text="Client Name", font=my_font, fg=black,bg=cyan)
name_entry = tk.Entry(info_frame,borderwidth= 3, font=my_font)
ip_label = tk.Label(info_frame, text="Host IP: ",font=my_font, fg=black,bg=cyan)
ip_entry = tk.Entry(info_frame,borderwidth= 3, font=my_font,state=DISABLED)
port_label = tk.Label(info_frame, text="Port Num: ",font=my_font,fg=black,bg=cyan)
port_entry = tk.Entry(info_frame,borderwidth= 3, font=my_font,width=10)
connect_button = tk.Button(info_frame,text="Connect", font=my_font,borderwidth=10, width=40,command=connect,image=connect_image)
disconnect_button = tk.Button(info_frame,text= "Disconnect", font=my_font,borderwidth=10,width=40,state=DISABLED,command=disconnect,image= disconect_image)
								   

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
connect_button.grid(row=1, column=2, padx=2, pady=2 )
disconnect_button.grid(row=1, column=3, padx=1, pady=1)

#Output Frame Layout
my_scrollbar = tk.Scrollbar(output_frame,orient=VERTICAL)
my_listbox = tk.Listbox(output_frame,height=20, width=55, borderwidth=3, bg=black, fg= grow_grow,font=my_font)
my_scrollbar.config(command= my_listbox.yview)

my_listbox.grid(row=0,column=0)
my_scrollbar.grid(row=0,column=1,sticky="NS")

#Input Frame Layout
input_entry = tk.Entry(input_frame, width=40, borderwidth=5 ,font=my_font)
send_button = tk.Button(input_frame, text="send", width=50, borderwidth=5,font=my_font,state=DISABLED,command=send_message,image= send_img)
input_entry.grid(row=0, column=0,padx=3, pady=5)
send_button.grid(row=0, column=1,padx=5, pady=5)

#Run the Root wondow s mainloop()
root.mainloop()





