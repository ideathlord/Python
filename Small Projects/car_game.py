def car_game():

    command = ""

    started = False

    print("*****    Car game :    *****")
    print("Type help for controls....")

    while True:
        command = input("> ")
        if command.lower() == "start":
            if started:
                print("The car is already started...")
            else:    
                started = True
                print("car started...")
        elif command.lower() == "stop":
            if not started:
                print("car is already stopped...")
            else:   
                started = False    
                print("car stopped....")
        elif command.lower() == "help":
            print("""
            start - to start the car
            stop  - to stop the car
            quit  - to quit the game
            """)  
        elif command.lower() == "quit":
            print("Quiting the game....")
            break
        else :
            print("Didn't Understand.. input again. ")
            
car_game()            