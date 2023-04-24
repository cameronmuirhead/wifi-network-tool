# wifi-network-tool
Wi-Fi network tool code for RGU Honours Project 2023

After completing the experiment, a tool will be developed to provide the user with some insight onto their current connected network. This tool will be run from the clients’ machine, sending the information to a web server that handles and produces the information in a graphical way. 
Firstly, a python script will need to be created that will be run from the client’s device to generate the information required to send to the web server. For this, we will need to import pre-existing modules to meet the requirements of the program. These modules are filled with existing Python code, that has usable functions, classes and variables that can integrate with our program.
The following modules will need to be imported for each individual purpose:

•	Subprocess: this module helps to provide a way to spawn new processes. It can also connect to their input/output pipes, allow execution of shell commands, and obtain returned code. This module will be used to help obtain information about the wireless network interface.

•	PyWiFi: this module provides an interface that is programmable with wireless networks and computer interfaces. It can be used for processes such as available network scanning, connected networks, and managing the profiles of networks. This will be used to obtain specific information from the connected network, such as signal strength and security types.

•	Time: this includes multiple time-related functions that can be used without the program for timings.

•	Requests: this module will be used to send the generated traffic to the specified web server through a series of HTTP requests. It can send GET, POST, set headers and handle cookies.

•	PSUtil: is a module that can similarly discover adapter options and will be used to gather information about current VPN connections on the user’s device.

•	JSON: this will be the file format used to send the traffic across to the web server.

Once the Python script has been configured following the above criteria, the information will be sent to a web server using the imported modules. The web server will be created using PythonAnywhere. This is a free online platform that allows the hosting and delivery of an application in one. The web application will be written using the popular framework Flask application, known as Flask App. The popular use for Flask allows the creation of a Python module that contains the code that will be run.
In our instance we will be running multiple instances that contain different web pages, each should display various criteria. The structure of these web pages will be written in HTML and formatted with the help of CSS. They are two separate technologies that can be used to create and style web pages, HTML mainly structures the content and CSS aids the visual appearance. The main function of the web page will be to display the user information sent across and separate this into separate sections that contain the information pulled from the user. It will also display recommendations for this user based on the network detail. This will all be accessible through the web interface publicly from any location.
