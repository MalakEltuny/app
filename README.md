# Real-time Monitor Simulator

## Project Overview:
- This project implements a real-time medical monitoring system using Python, PyQt5 for the GUI, and Redis for the Database.
- Using the Socket Programming and TCP/IP as the communication method between the client and the server
- The client is a GUI that handles both sending random data in the range of the specific vital Sign and visualize these data in a Line Graph or in a Table
- The server handles the request from the client side sent in a JSON format to standardize the request method and saves the data in redis database the key is the id, name, and the vital sign name joined together with a sperator as _ and the values is stored in the array linked to that specific key

## Components
- Server: Manages incoming connections and data from the client, storing received medical data into Redis.
- GUI: Simulates patient data generation and sends this data to the server. Allows users to visualize the medical data in real-time, search for specific patients, and control the monitoring process.
- Redis: Used as a datastore to hold the medical data for all patients.

## Screen-Shots:



## Team Members
- Malak ahmed hosny 1210378
- Youssef Ahmed Afify 1200883
