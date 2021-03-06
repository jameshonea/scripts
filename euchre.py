import random
cards = ['As','Ks','Qs','Js','10s','9s',
         'Ac','Kc','Qc','Jc','10c','9c',
          'Ad','Kd','Qd','Jd','10d','9d',
          'Ah','Kh','Qh','Jh','10h','9h']
suits = {'spades': ['As','Ks','Qs','Js','10s','9s'],
         'clubs': ['Ac','Kc','Qc','Jc','10c','9c'],
         'diamonds': ['Ad','Kd','Qd','Jd','10d','9d'],
         'hearts': ['Ah','Kh','Qh','Jh','10h','9h']
         }

suit_names = ['SPADES', 'CLUBS','HEARTS', 'DIAMONDS']

def determine_winner(tru, lead, played_cards):
    # construct a list of card rankings and give trick to highest card holder
    # only need to construct list of trump cards and leading card suit as
    # these will be the highest ranking cards and one of them must be played.

    ranking = []
    if tru == 'spades':
        ranking.append(suits[tru][3])
        ranking.append(suits['clubs'][3])
        for card in suits[tru]:
            ranking.append(card) # can append jack twice because it wont affect ranking, less computationally expensive.
        for card in suits[lead]:
            ranking.append(card)

    if tru == 'clubs':
        ranking.append(suits[tru][3])
        ranking.append(suits['spades'][3])
        for card in suits[tru]:
            ranking.append(card) # can append jack twice because it wont affect ranking, less computationally expensive.
        for card in suits[lead]:
            ranking.append(card)

    if tru == 'diamonds':
        ranking.append(suits[tru][3])
        ranking.append(suits['hearts'][3])
        for card in suits[tru]:
            ranking.append(card) # can append jack twice because it wont affect ranking, less computationally expensive.
        for card in suits[lead]:
            ranking.append(card)

    if tru == 'hearts':
        ranking.append(suits[tru][3])
        ranking.append(suits['diamonds'][3])
        for card in suits[tru]:
            ranking.append(card) # can append jack twice because it wont affect ranking, less computationally expensive.
        for card in suits[lead]:
            ranking.append(card)


        # now iterate through rankings, and check if each card is in list
        # return index for first card to show up. thats the trick winner.

    print(ranking)

    for i in ranking:
        if i in played_cards:
            return played_cards.index(i)

def get_key(val):
    for key, li in suits.items():
        for value in li:
            if value == val:
                return key


def determine_tru(dealer, flip_up_card):

    first_to_act = dealer

    flip_up_suit = get_key(flip_up_card)

    

    for i in range(3):
        print('Player {}: Tell Player {} to pick up {}? Y/N'.format((first_to_act + (i+1))%4 + (1), (first_to_act)%4 + (1), flip_up_card))
        answer = input()
        if answer.upper() == 'Y':
            return flip_up_suit

    print('Player {}: Pick up {}? Y/N'.format((first_to_act)%4 + 1, flip_up_card))
    answer = input()
    if answer.upper() == 'Y':
        return flip_up_suit

    for i in range(4):
        t = False
        while t == False:
            print('Player {}: Choose suit or pass.'.format((first_to_act + (i+1))%4 + 1))
            answer = input()
            if answer.upper() in suit_names:
                if answer.upper() == flip_up_suit.upper():
                    print('Cannot pick {}.'.format(flip_up_suit))
                else:
                    return answer.lower()
            elif answer.upper() == 'PASS':
                t = True
            else:
                print('Error: Please re-enter.')

    print('REDEAL..')
    return 'redeal'

def trick(first_to_act, trump, hand_list): # works but need to include left bower with right bower's suit in check somehow
    
    played_cards = []
    t = False
    while t == False:
        print('Player {}: Play card'.format(first_to_act + 1))
        card = input()
        if card in hand_list[first_to_act]:
            hand_list[first_to_act].remove(card)
            suit = get_key(card)
            played_cards.append(card)
            t = True
        else:
            print('Please enter card in your hand.')

    for i in range(3):
        t = False
        while t == False:
            print('Player {}: Play your card.'.format((first_to_act + (i+2))%4))
            card = input()
            hand = hand_list[(first_to_act + (i+1))%4]
            if card in hand:
                if get_key(card) != suit: # check for no cards of leading suit in hand if not same suit
                    suit_check = False
                    for e in hand:
                        if get_key(e) == suit:
                            suit_check = True
                    if suit_check == True:
                        print('Must play leading suit.')
                    else:
                        hand_list[(first_to_act + (i+1))%4].remove(card)
                        played_cards.append(card)
                        t = True

                else:
                    hand_list[(first_to_act + (i+1))%4].remove(card)
                    played_cards.append(card)
                    t = True
            else:
                print('Must play card in your hand')
    winner = determine_winner(trump, suit, played_cards)
    return winner, hand_list
    
                
    

p1p3_score = 0
p2p4_score = 0

player_list = [1,2,3,4]
dealer = 0
turn_counter = 0

while (p1p3_score < 10) & (p2p4_score < 10):
    print('lol')

    # determine trump loop until trump is chosen
    done = False
    while done == False:
        print('lol')
        random.shuffle(cards)
        hands = [cards[0:5],cards[5:10],cards[10:15],cards[15:20]]
        for e in hands:
            print(e)
        flip = cards[20]
        tru = determine_tru(dealer, flip)
        dealer = (dealer+1)%3
        if tru != 'redeal':
            done = True
    # next, complete 5 tricks and score
    

    scores = [0,0,0,0]

    for _ in range(5):
        winner, hands = trick((dealer+1)%4, tru, hands) # this wont work for a sec. need to tie it to index corresponding to player. currently i think it's gonna treat whoever played first in the trick as player 0.
        scores[winner] += 1

    # next find hand winner and increment score. not calculating euchres atm
    if (scores[0] + scores[2]) > (scores[1] + scores[3]):
        p1p3_score += 1
    else:
        p2p4_score += 1
        
    

    random.shuffle(cards)
    hands = [cards[0:5],cards[5:10],cards[10:15],cards[15:20]]
    flip = cards[20]
    
    tru = determine_tru(dealer, flip)
    while tru == 'redeal':
        dealer = (dealer+1)%3
        random.shu
    

    p1_hand = cards[0:5]
    p2_hand = cards[5:10]
    p3_hand = cards[10:15]
    p4_hand = cards[15:20]
    print(p1_hand)

    flip_up = cards[20]
    print(flip_up)

    

