# Data-Monotoring
Data Monitoring and Plotting in Python Tkinter

A live data monitoring and plotting program for a HIL simulator in Python 2.
This program receives the simulator attitude data, measured by its sensors, using the serial port.
These data are sent in the form of some string, containing a header for identifying them on receiver.
Then the program split each strings according to its predetermined format and extracts the data of each sensor in a specific way. 

The data are contained within a dictionary structure together with the corresponding headings for interpreting them in the tabConfig module.
Because tkinter is used for gui, the guiloop module has been used to prevent the hang of the system because of the mainloop and the infinite while loop associated with the plotting.
