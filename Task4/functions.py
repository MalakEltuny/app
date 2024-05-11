import socket
import random
import json
import time
import threading
import redis
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem



client_socket = None
redis_client = redis.Redis(host='localhost', port=6379, db=0)

patientId=""
patientName=""
vitalSign=""
vitalSignValues=[]

def startConnection(vitalNumber):
    global client_socket
    # Check if the client socket is already open
    if client_socket and client_socket.fileno() != -1:
        print("Connection is already open. Closing it.")
        client_socket.close()
    
    # Initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'  # or '127.0.0.1' to connect to the local machine
    port = 12345

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Receive initial message from the server
        message = client_socket.recv(1024)
        print(message.decode('ascii'))

        # Function to receive JSON response from the server
        def receive_json_response(client_socket):
            # Receive JSON data from the server
            json_data = client_socket.recv(1024).decode('ascii')
            
            # Decode JSON data
            try:
                response = json.loads(json_data)
                return response
            except json.JSONDecodeError:
                print("Received invalid JSON data from the server:", json_data)
                return None

        # Send JSON data to the server and receive JSON responses
        while True:
            # Prepare JSON data to send to the server
            if not client_socket:
                break
            data = {
                "id": int(patientId),
                "name": patientName,
                "vital_sign": vitalSign,
                "value": generateRandomVitalSign(vitalSign)
            }
            vitalNumber.display(int(data["value"]))

            # Convert data to JSON format
            json_data = json.dumps(data)

            # Send JSON data to the server
            client_socket.send(json_data.encode('ascii'))
            
            # Receive JSON response from the server
            response = receive_json_response(client_socket)
            if response:
                print("Received JSON response from the server:")
                print("ID:", response["id"])
                print("Name:", response["name"])
                print("Vital Sign:", response["vitalSign"])
                print("Values:", response["values"])
            
            # Wait for 1 second before sending the next data
            time.sleep(1)
    except Exception as e:
        print("Error:", e)
        if client_socket:
          client_socket.close()


def testConnection(self,vitalNumber):
    global client_socket
    print("Testing connection...")
    if client_socket and client_socket.fileno() != -1:
        print("Closing the connection.")
        client_socket.close()
        print("Connection closed.")
        client_socket = None  # Reset the client_socket variable
    else:
        print("Connection is open.")
        threading.Thread(target=startConnection, args=(vitalNumber,)).start()


def generateRandomVitalSign(vitalName):
    if vitalName == "respiratory":
        # Normal range for respiratory rate: between 12 and 20 breaths per minute
        return random.randint(12, 20)
      
    elif vitalName == "heart":
        # Normal range for heart rate: between 60 and 100 beats per minute
        return random.randint(60, 100)
        
    elif vitalName == "temperature":
        # Normal range for body temperature: between 36.1 and 37.2 degrees Celsius
        return round(random.uniform(36.1, 37.2), 1)
    else:
        print("Invalid vital sign name")

def handleRadioBtn(self,vitalName):
    global vitalSign
    vitalSign=vitalName

def handleTextChanged(self, text,boxType):
    global patientName
    global patientId
    if boxType=="name":
        patientName=text
    else:
        patientId=text


def handleSearchByIdButton(ID, name, vs):
  global vitalSignValues
  redis_name = redis_client.keys(f'{ID}_*')
  if not redis_name:
    QMessageBox.warning(None, "Alert", "Patient not found")
    return
  redis_name_str = redis_name[0].decode('utf-8')
  print(redis_name_str.split("_"))
  name.setText(redis_name_str.split("_")[1])  
  vs.setText(redis_name_str.split("_")[2])
  values=redis_client.lrange(redis_name_str, 0, -1)
  vitalSignValues=[float(value) for value in values] 
  print(vitalSignValues)
  QMessageBox.warning(None, "Alert", "Data Loaded press display button to see the data.")



    


def searchThread(ID, name, vs):
    global client_socket
    print("Testing connection...")
    if client_socket and client_socket.fileno() != -1:
        print("Closing the connection.")
        client_socket.close()
        print("Connection closed.")
        client_socket = None  # Reset the client_socket variable
    else:
      print("Connection is open.")
      handleSearchByIdButton(ID,name,vs)



def plotGraph(self,plot):
    global vitalSignValues
    plot.clear()
    plot.plot(vitalSignValues)
    plot.show()



def searchByVitalBtnClicked(self,searchByVitalTextBox, tableWidget):
    tableWidget.setRowCount(0)
    global redis_client
    
  
    # Search for relevant data in the Redis database
    keys = redis_client.keys(f'*_{searchByVitalTextBox}')
  
    for key in keys:
        key_str = key.decode('utf-8')
        patient_id = key_str.split("_")[0]
        name = key_str.split("_")[1]
        vital_sign = key_str.split("_")[2]
        values = redis_client.lrange(key, 0, -1)
        values = [float(value) for value in values]
        print(values)
      
        row_position = tableWidget.rowCount()
        tableWidget.insertRow(row_position)
        tableWidget.setItem(row_position, 0, QTableWidgetItem(patient_id))
        tableWidget.setItem(row_position, 1, QTableWidgetItem(name))
        tableWidget.setItem(row_position, 2, QTableWidgetItem(vital_sign))
        tableWidget.setItem(row_position, 3, QTableWidgetItem(str(values)))


def getAllData(self,tableWidget):
    
    global redis_client
    tableWidget.setRowCount(0)

  
    # Search for relevant data in the Redis database
    keys = redis_client.keys("*")
    print(keys)
  
    for key in keys:
        key_str = key.decode('utf-8')
        patient_id = key_str.split("_")[0]
        name = key_str.split("_")[1]
        vital_sign = key_str.split("_")[2]
        values = redis_client.lrange(key, 0, -1)
        values = [float(value) for value in values]
        print(values)
      
        row_position = tableWidget.rowCount()
        tableWidget.insertRow(row_position)
        tableWidget.setItem(row_position, 0, QTableWidgetItem(patient_id))
        tableWidget.setItem(row_position, 1, QTableWidgetItem(name))
        tableWidget.setItem(row_position, 2, QTableWidgetItem(vital_sign))
        tableWidget.setItem(row_position, 3, QTableWidgetItem(str(values)))