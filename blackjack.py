#Alien Blackjack
#  
#This is a game expanded from an exercise In Tim Bulchlaka and Jean-Paul Robert's excellent Learn Python Programming Masterclass
#(https://www.udemy.com/course/python-the-complete-python-developer-course/)
#and inspired by Tony Ramunni's beilliant artwork for the 1980 Williams pinball table 'Alien Poker'
#The card images were adapted from David Bellot's Svg Cards: http://svg-cards.sourceforge.net/
#
#Copyright Nick Greenfield 2022 
#This program is released under the GNU Lesser General Public License v3.0



from multiprocessing.sharedctypes import Value
import random
from unittest import result
from fontTools.ttLib import TTFont
import winsound

try:
    import tkinter
    
except ImportError:
    import TKinter as tkinter
import pyglet
from tkinter import BOTTOM, ttk
#initialise main window
mainWindow = tkinter.Tk()
mainWindow.title("Alien Blackjack")
mainWindow.geometry("640x480")
mainWindow.configure(background="black")

def main_menu():
    '''Generates the main menu frame and creates three buttons corresponding to the three difficulty settings'''
    global main_button_frame
    global easy_button
    global medium_button
    global hard_button
    global Logoimg
    global EasyPortrait
    global MediumPortrait
    global HardPortrait
    global dealerPortrait
    global easybuttonimg
    global mediumbuttonimg
    global hardbuttonimg
    global easy_Portrait_label
    global medium_Portrait_label
    global hard_Portrait_label
    global Ab_font_File
    global Ab_font
    global logo_label
    global ButtonStyle
    global Sound_button
    
    
    ButtonStyle.configure('BlackJackButton', background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5, font=('DBXLNightfever', 14, "bold" ))
    
    #get images
    
    logo_label = tkinter.Label(mainWindow,image=Logoimg, borderwidth=0)
    logo_label.grid(row=0, column=1, pady=50)
    
    main_button_frame = tkinter.Frame(mainWindow, background="black",  borderwidth=0)
    main_button_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=140, pady=0,)

    easy_Portrait_label = tkinter.Label(main_button_frame,image=EasyPortrait, borderwidth=0)
    easy_Portrait_label.grid(row=1, column=0)
    easy_button = tkinter.Button(main_button_frame, text=" Easy ", background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ), command=easy_init)
    easy_button.grid(row=2, column=0 )
    medium_Portrait_label = tkinter.Label(main_button_frame,image=MediumPortrait, borderwidth=0)
    medium_Portrait_label.grid(row=1, column=1)
    medium_button = tkinter.Button(main_button_frame, text="Medium", background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ), command=medium_init)
    medium_button.grid(row=2, column=1, pady=10)
    hard_Portrait_label = tkinter.Label(main_button_frame,image=HardPortrait, borderwidth=0)
    hard_Portrait_label.grid(row=1, column=2)
    hard_button  = tkinter.Button(main_button_frame, text=" Hard ", command=hard_init, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    hard_button.grid(row=2, column=2 )
    
    Sound_button = tkinter.Button(mainWindow, text="Sound Off", command=Turn_sound_off, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 8, "bold" ))
    Sound_button.place(x=560,y=440)

def Turn_sound_off():
    '''Turn sound off, replace button with sound on'''
    global playSounds
    global Sound_button
    playSounds = 0
    Sound_button.destroy()
    Sound_button = tkinter.Button(mainWindow, text="Sound On", command=Turn_sound_on, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 8, "bold" ))
    Sound_button.place(x=560,y=440)

def Turn_sound_on():
    '''Turn sound on, replace button with sound off'''
    global playSounds
    global Sound_button
    playSounds = 1
    Sound_button.destroy()
    Sound_button = tkinter.Button(mainWindow, text="Sound Off", command=Turn_sound_off, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 8, "bold" ))       
    Sound_button.place(x=560,y=440)

def easy_init():
    '''initiates easy mode, giving player and dealer equal cash and making dealer less aggressive'''
    if playSounds == 1:
        winsound.PlaySound('Speech/AlienBlackJack.wav', winsound.SND_FILENAME)
    
    global player_cash
    global dealer_cash
    global difficulty
    global dealerPortrait
    global EasyPortrait
    global i_win_sound
    global i_deal_sound
    global you_win_sound
    dealerPortrait = EasyPortrait
    i_win_sound = 'Speech/East -  I_Win.wav'
    you_win_sound = 'Speech/East -  You_Win.wav'
    i_deal_sound = 'Speech/East -  I Deal.wav'


    player_cash = 250
    dealer_cash = 250
    difficulty = 0
    place_bet()


def medium_init():
    '''initiates normal mode, giving dealer slightly more cash and having dealer stick on 17'''
    if playSounds == 1:
        winsound.PlaySound('Speech/AlienBlackJack.wav', winsound.SND_FILENAME)
    global player_cash
    global dealer_cash
    global difficulty
    global dealerPortrait
    global MediumPortrait
    global i_win_sound
    global i_deal_sound
    global you_win_sound

    dealerPortrait = MediumPortrait
    i_win_sound = 'Speech/med - i win.wav'
    you_win_sound = 'Speech/med - you win.wav'
    i_deal_sound = 'Speech/med - I deal.wav'
    player_cash = 200
    dealer_cash = 300
    difficulty = 1
    place_bet()


def hard_init():
    
    '''initiates hard mode, giving dealer much more cash and the ability to know the next card when on 17'''
    if playSounds == 1:
        winsound.PlaySound('Speech/AlienBlackJack.wav', winsound.SND_FILENAME)
    global player_cash
    global dealer_cash
    global difficulty
    global dealerPortrait
    global HardPortrait
    global i_win_sound
    global i_deal_sound
    global you_win_sound
    
    dealerPortrait = HardPortrait
    i_win_sound = 'Speech/Hard - I_Win.wav'
    you_win_sound = 'Speech/Hard - You_Win.wav'
    i_deal_sound = 'Speech/Hard - I_Deal.wav'
    player_cash = 100
    dealer_cash = 400
    difficulty = 2
    place_bet()


def place_bet():
    '''initiates betting screen. Generates the minimum wager amount with buttons to increase, decrease and set. Wager cannot go above 20 or smaller than 5'''
    global bet_amount
    global bet_frame
    global wager_label
    global decreasebetImage
    global increasebetImage
    global setbetImage
    global dealerPortrait
    global Dealer_Portrait_label
    global cash_frame 
    global cash_label 
    global player_cash_label
    global dealer_cash_label
    global logo_label
    global Sound_button
    

    bet_amount = 5
    main_button_frame.destroy()
    logo_label.grid_remove()
    cash_frame = tkinter.Frame(mainWindow, background="black", highlightthickness=0, borderwidth=0)
    cash_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=240, pady=60)
    player_cash_label = tkinter.IntVar()

    cash_label= tkinter.Label(cash_frame, text="Player Cash:", background="black", fg="yellow", font=Ab_font)
    cash_label.grid(row=0, column=2)
    tkinter.Label(cash_frame, textvariable=player_cash_label, background="black", fg="yellow", font=Ab_font).grid(row=0,column=4, sticky='w')
    player_cash_label.set(player_cash)
    Dealer_Portrait_label = tkinter.Label(mainWindow, image=dealerPortrait, borderwidth=0)
    Dealer_Portrait_label.grid(row=2,column=1)
    bet_frame = tkinter.Frame(mainWindow, background="black", highlightthickness=0, borderwidth=0, highlightcolor="black")
    bet_frame.grid(row=3, column=0, columnspan=3, sticky='ew', padx=70)
    
    wager_label = tkinter.IntVar()   
    wager_label.set(bet_amount)
   
    tkinter.Label(bet_frame, text="Wager", background="black", fg="yellow", font = Ab_font).grid(row=0, column=1)
    tkinter.Label(bet_frame, textvariable=wager_label, background="black", fg="yellow", font=Ab_font).grid(row=1,column=1, padx=20)

    smaller_button = tkinter.Button(bet_frame, text="Decrease Wager", command=decrese_bet, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    smaller_button.grid(row=2, column=0, padx=5 )
    select_button = tkinter.Button(bet_frame, text="    Place Wager    ", command=select_bet, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ) )
    select_button.grid(row=2, column=1, padx=5)
    larger_button  = tkinter.Button(bet_frame, text="Increase Wager", command=increase_bet, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    larger_button.grid(row=2, column=2, padx=5) 


def decrese_bet():
    '''decreases wager if larger than 5'''
    global bet_amount
    if bet_amount > 5:
        bet_amount -= 5
        wager_label.set(bet_amount)


def increase_bet():
    '''increases wager smaller than 20 and the player can afford it!'''
    global player_cash
    global bet_amount
    if bet_amount < 20:
        if bet_amount < player_cash:
            bet_amount += 5
            wager_label.set(bet_amount)


def select_bet():
    '''Removes wager from player, gives to dealer and initiates main game screen'''
    global dealer_cash
    global player_cash
    dealer_cash = dealer_cash + bet_amount
    player_cash = player_cash - bet_amount
    setup_game()




def setup_game():
    '''Main game screen creates card, button frames and a frame showing money/wager. Shuffles deck and does initial deal'''
    global mainWindow
    global result_text
    global player_score_label
    global dealer_score_label
    global dealer_hand
    global player_hand
    global cards
    global card_frame
    global dealer_card_frame
    global player_card_frame
    global button_frame
    global deck
    global money_frame
    global player_cash_label 
    global dealer_cash_label
    global player_cash
    global dealer_cash
    global doubleWager_button
    global double_destroyed
    global player_button
    global dealer_button
    global theresult
    global dealerPortrait
    global SurrenderExists
    global Surrender_button
    global SurrenderBut
   
    
    #destroy place_bet
    bet_frame.destroy()
    cash_frame.destroy()
    Dealer_Portrait_label.destroy()

    


    result_text = tkinter.StringVar()
    theresult = tkinter.Label(mainWindow, textvariable = result_text, background="black", fg="yellow", font=Ab_font)
    theresult.grid(row=0, column=0, columnspan=3)

    card_frame = tkinter.Frame(mainWindow, borderwidth=0, background="black")
    card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2, padx=100)

    dealer_score_label = tkinter.IntVar()
    tkinter.Label(card_frame, image=dealerPortrait, background="black", fg='yellow').grid(row=0, column=0)
    tkinter.Label(card_frame, textvariable=dealer_score_label, background="black", fg="yellow", font= Ab_font).grid(row=1, column=0)
    #embed frame  to hold the card images
    dealer_card_frame = tkinter.Frame(card_frame, background="black")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2, )

    player_score_label = tkinter.IntVar()   
    tkinter.Label(card_frame, text="You", background="black", fg="yellow", font=Ab_font).grid(row=2, column=0, pady=10)
    tkinter.Label(card_frame, textvariable=player_score_label, background="black", fg="yellow", font=Ab_font).grid(row=3,column=0)

    #embedded frame to hold the card images
    player_card_frame = tkinter.Frame(card_frame, background="black")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2,pady=5)

    button_frame = tkinter.Frame(mainWindow, background="black")
    button_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=100, pady=10)

    
    player_button = tkinter.Button(button_frame, text="     Hit     ", command=deal_player, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    player_button.grid(row=0, column=0, padx=5)
    doubleWager_button = tkinter.Button(button_frame, text="Double Wager", command=double_wager, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    doubleWager_button.grid(row=0, column=1, padx=5)
    Surrender_button = tkinter.Button(button_frame, text=" Surrender ", command=Surrender_Hand, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    Surrender_button.grid(row=0, column=2, padx=5)
    SurrenderExists = 1
    #Money!
    money_frame = tkinter.Frame(mainWindow, background="black",)
    money_frame.grid(row=4, column=0, sticky='ew', rowspan=2,padx=100, pady=10)
    player_cash_label = tkinter.IntVar()
    dealer_cash_label = tkinter.IntVar()  
    tkinter.Label(money_frame, text="Player Cash", background="black", fg="yellow",font=Ab_font).grid(row=2, column=0)
    tkinter.Label(money_frame, textvariable=player_cash_label, background="black", fg="yellow",font=Ab_font).grid(row=3,column=0)
    tkinter.Label(money_frame, text="Dealer Cash", background="black", fg="yellow",font=Ab_font).grid(row=2, column=1)
    tkinter.Label(money_frame, textvariable=dealer_cash_label, background="black", fg="yellow",font=Ab_font).grid(row=3,column=1)
    tkinter.Label(money_frame, text="Wager", background="black", fg="yellow",font=Ab_font).grid(row=2, column=2)
    tkinter.Label(money_frame, textvariable=wager_label, background="black", fg="yellow", font=Ab_font).grid(row=3,column=2)
    dealer_cash_label.set(dealer_cash)
    player_cash_label.set(player_cash)
    double_destroyed = 1
    #create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []

    #deck
    #load cards
    cards =[]
    load_images(cards)

    #create new deck and shuffle
    deck = list(cards)
    random.shuffle(deck)
    #scores
    player_score = 0
    dealer_score = 0
    deal_player()
    if playSounds == 1:
        winsound.PlaySound(i_deal_sound, winsound.SND_FILENAME)
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    double_destroyed = 0


def load_images(card_images):
    '''loads all of the card images'''
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    if tkinter.TkVersion >= 8.6:
        extention = 'png'
    else:
        extention = 'ppm'
    #for each suit, retrirve the image of the cards
    for suit in suits:
        for card in range(1,11):
            name = 'cards/{}_{}.{}'.format(str(card),suit,extention)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        #next face card
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extention)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10,image))


def deal_card(frame):
    '''deal card by popping from the top of the deck'''
    #pop the next card from the deck
    next_card = deck.pop(0)
    #add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], borderwidth=0).pack(side='left')
    #now return cards face vaule
    return next_card         


def score_hand(hand):
    '''Score the hand, taking account of the potential ace vaules'''
    #calculate the total score of all cards in the list
    #only one ace can have the value 11 and this will reduce to 1 if hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value=next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    '''once player has stuck, deal to the dealer. If difficulty is set to hard, allow dealer to know to twist if the next card is less than 3 '''
    global player_button
    global dealer_button
    global bet_amount
    global dealer_cash
    global player_cash
    global deck
    global SurrenderExists
    global Surrender_button
    dealer_quit = 0
    runonce = 0
    if difficulty == 0:
        dealer_quit = 16

    if difficulty > 0:
        dealer_quit = 17
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < dealer_quit:
     dealer_hand.append(deal_card(dealer_card_frame))
     dealer_score = score_hand(dealer_hand)
     dealer_score_label.set(dealer_score)
     #hard mode cheats
    if difficulty == 2:
        
        for next_card in deck:
            if runonce == 0:
                print(next_card)
                print(runonce)
                thecard_value= next_card[0]
                runonce = 1
                if thecard_value < 3:
                    dealer_hand.append(deal_card(dealer_card_frame))
                    dealer_score = score_hand(dealer_hand)
                    dealer_score_label.set(dealer_score)
    #check for win
    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins")
        player_button.destroy()
        dealer_button.destroy()
        if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
        if double_destroyed == 0:
            doubleWager_button.destroy()
        add_new_game()
        if playSounds == 1:
            winsound.PlaySound(i_win_sound, winsound.SND_FILENAME)
 
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
        player_button.destroy()
        dealer_button.destroy()
        if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
        if double_destroyed == 0:
            doubleWager_button.destroy()
        bet_amount = bet_amount * 2
        player_cash += bet_amount
        dealer_cash -= bet_amount
        dealer_cash_label.set(dealer_cash)
        player_cash_label.set(player_cash)
        add_new_game()
        if playSounds == 1:
            winsound.PlaySound(you_win_sound, winsound.SND_FILENAME)

    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
        player_button.destroy()
        dealer_button.destroy()
        if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
        if double_destroyed == 0:
            doubleWager_button.destroy()
        add_new_game()
        if playSounds == 1:
            winsound.PlaySound(i_win_sound, winsound.SND_FILENAME)

    else:
        result_text.set("Draw!")
        player_button.destroy()
        dealer_button.destroy()
        if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
        if double_destroyed == 0:
            doubleWager_button.destroy()
        player_cash += bet_amount
        dealer_cash -= bet_amount
        dealer_cash_label.set(dealer_cash)
        player_cash_label.set(player_cash)
        add_new_game()


def deal_player():
    '''deal player. Automatic dealer win if the player busts'''
    global double_destroyed
    global player_button
    global player_hand
    global dealer_button
    global player_button
    global SurrenderExists
    global Surrender_button
    global doubleWager_button
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    if len(player_hand) == 3:
        doubleWager_button.destroy()
        double_destroyed = 1
    if player_score == 21:
        player_button.destroy()
        doubleWager_button.destroy()
        double_destroyed = 1
        Surrender_button.destroy()
        SurrenderExists = 0
    player_score_label.set(player_score)
    #add stick button
    if len(player_hand) == 2:
        dealer_button = tkinter.Button(button_frame, text="    Stick    ", command=deal_dealer, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
        dealer_button.grid(row=0, column=1)
        doubleWager_button.grid(row=0, column=2)
        Surrender_button.grid(row=0,column=3)
    if len(player_hand) == 3:
        if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
        
    if player_score > 21:
        result_text.set("Dealer Wins!")
        player_button.destroy()
        dealer_button.destroy()
        if double_destroyed == 0:
            doubleWager_button.destroy()
        add_new_game()
        if playSounds == 1:
            winsound.PlaySound(i_win_sound, winsound.SND_FILENAME)
    
    

def Surrender_Hand():
    '''Return half of player hand. Initiate next game'''
    global bet_amount
    global player_cash
    global dealer_cash
    global Surrender_button
    global SurrenderExists
    global player_button
    global doubleWager_button
    global dealer_button
    bet_amount = round((bet_amount/2))
    player_cash = (player_cash + bet_amount)
    dealer_cash_label.set(dealer_cash)
    player_cash_label.set(player_cash)
    result_text.set("Player Surrendered!")
    player_button.destroy()
    doubleWager_button.destroy()
    Surrender_button.destroy()
    SurrenderExists = 0
    if len(player_hand) == 2:
        dealer_button.destroy()

    add_new_game()

def double_wager():
    '''Allows the player to double their wager if they haven't taken extra cards. Add some spice'''
    global player_cash
    global dealer_cash
    global doubleWager_button
    global bet_amount
    global Surrender_button
    global SurrenderExists
    if SurrenderExists == 1:
            Surrender_button.destroy()
            SurrenderExists = 0
    if player_cash >= bet_amount:
        player_cash -= bet_amount
        dealer_cash += bet_amount
        bet_amount = bet_amount * 2
        wager_label.set(bet_amount)
        dealer_cash_label.set(dealer_cash)
        player_cash_label.set(player_cash)
    doubleWager_button.destroy()
    double_destroyed = 1
    



def add_new_game():
    '''Add the next hand button (was originally the 'new game' button'''
    global newgame_button
    newgame_button = tkinter.Button(button_frame, text="Next Hand", command=start_new, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    newgame_button.grid(row=0, column=2 )


def start_new():
    '''Destroy the main game window and return to wagering, or game over screen if player or dealer has run out of cash'''
    global dealer_hand
    global player_hand
    global dealer_card_frame
    global player_card_frame
    global money_frame
    global button_frame
    global theresult
    global hand_number

    #destroy and remake card frames
    money_frame.destroy()
    button_frame.destroy()
    card_frame.destroy()
    theresult.destroy()
    result_text.set("")
    newgame_button.destroy()

    if player_cash > 5 and dealer_cash > 0:
        hand_number += 1
        place_bet()
    else:
        game_over()

def game_over():
    '''end the game! Shows A congratulations/commiseration frame depending on who's run out of cash. Adds restart button'''
    global game_Over_frame
    global restart_button
    game_Over_frame = tkinter.Frame(mainWindow, background="black")
    game_Over_frame.grid(row=0, column=0, sticky='ew', padx=130, pady=120)
    go_header = tkinter.Label(game_Over_frame, text="Game Over", background='Black', foreground='Yellow', highlightcolor = "Yellow", font=('DBXLNightfever', 20, "bold" )).grid(row=0, column=1, pady=20)
    go_label = tkinter.IntVar()   
    tkinter.Label(game_Over_frame, textvariable=go_label, background='Black', foreground='Yellow', highlightcolor = "Yellow", font=('DBXLNightfever', 14, "bold" )).grid(row=1, column=1)
    if player_cash > 5:
        go_label.set(f"Well done! you took the dealer\nto the cleaners. You won in \n{hand_number} hands")
    if player_cash < 5:
        go_label.set(f"Oh no! You didn't win this time.\nYou kept the game going for {hand_number} hands,\n but now its time to take the bus home")
    
    restart_button= tkinter.Button(game_Over_frame, text="Restart Game", command=restart_game, background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5,  font=('DBXLNightfever', 14, "bold" ))
    restart_button.grid(row=2, column=1, pady=10 )

def restart_game():
    '''reinitialise values and returns to difficulty select'''
    global game_Over_frame
    global player_cash
    global dealer_cash
    global hand_number
    game_Over_frame.destroy()
    player_cash = 0
    dealer_cash = 0
    hand_number = 1
    main_menu()


    
    
############################### Main script ###########################

player_cash = 0
dealer_cash = 0
hand_number = 1
#Define images on load
SurrenderBut = tkinter.PhotoImage(file="Ui/SurrenderButton.png").subsample(6,6)
stickBut = tkinter.PhotoImage(file="Ui/StickButton.png").subsample(6,6)
hitBut = tkinter.PhotoImage(file="Ui/HitButton.png").subsample(6,6)
WagerBut = tkinter.PhotoImage(file="Ui/DoubleWagerButton.png").subsample(6,6)
Logoimg = tkinter.PhotoImage(file="Ui/logo.png").subsample(2,2)   
EasyPortrait = tkinter.PhotoImage(file="Ui/EasyPortrait.png").subsample(2,2) 
MediumPortrait = tkinter.PhotoImage(file="Ui/MediumPortrait.png").subsample(2,2)
HardPortrait = tkinter.PhotoImage(file="Ui/HardPortrait.png").subsample(2,2)
easybuttonimg = tkinter.PhotoImage(file="Ui/Easy.png").subsample(6,6)
mediumbuttonimg = tkinter.PhotoImage(file="Ui/Medium.png").subsample(6,6)
hardbuttonimg = tkinter.PhotoImage(file="Ui/Hard.png").subsample(6,6)
decreasebetImage = tkinter.PhotoImage(file="Ui/Decrease_bet_Button.png").subsample(6,6)
increasebetImage = tkinter.PhotoImage(file="Ui/Increase_bet_Button.png").subsample(6,6)
setbetImage = tkinter.PhotoImage(file="Ui/Place_betButton.png").subsample(6,6)
nexthandBut = tkinter.PhotoImage(file="Ui/NextHandBut.png").subsample(6,6)


#font
pyglet.font.add_file('font/DBXLNN_.ttf')
Ab_font_File = pyglet.font.load("DBXLNightfever", size=14, bold=True)
Ab_font = ("DBXLNightfever", 14, "bold")

#configure button
ButtonStyle = ttk.Style()
ButtonStyle.configure('BlackJackButton', background='Black', foreground='Yellow', highlightcolor = "Yellow", borderwidth=5, font=('DBXLNightfever', 14, "bold" ))
#play sounds
playSounds = 1
main_menu()








mainWindow.mainloop()
