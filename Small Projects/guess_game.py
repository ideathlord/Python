def guess_game():

    secret_num = 7
    guess_count = 0
    max_guess = 3

    while guess_count < max_guess :
        guess = int(input('Guess :'))
        guess_count += 1
        if guess == secret_num:
            print('Correct Guess')
            break
        else:
            print('Wrong guess')

guess_game()            
