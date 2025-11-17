import random
from collections import Counter


def create_shoe(decks=8):
    """Create and shuffle 8 decks of cards, then take half."""
    single_deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4
    shoe = single_deck * decks
    random.shuffle(shoe)
    return shoe[:len(shoe)//2]


def hand_value(hand):
    """Return best hand value considering aces as 1 or 11."""
    value = sum(11 if card==1 else card for card in hand)
    aces = hand.count(1)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(hand):
    names = {1:'A',11:'J',12:'Q',13:'K'}
    return [names.get(card,str(card)) for card in hand]

def deal_card(shoe):
    if len(shoe) == 0:
        raise Exception("No more cards in shoe!")
    return shoe.pop()


# Dealer play according to rules
def dealer_play(dealer_hand, shoe):
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(shoe))
    return dealer_hand


# Simulate win probability via Monte Carlo
def estimate_win_prob(player_hand, dealer_upcard, shoe, trials=5000):
    wins = 0
    pushes = 0
    original_shoe = shoe.copy()

    for _ in range(trials):
        sim_shoe = original_shoe.copy()
        # Remove known dealer upcard
        sim_shoe.remove(dealer_upcard)
        # Deal hidden card to dealer
        dealer_hand = [dealer_upcard, sim_shoe.pop(random.randrange(len(sim_shoe)))]
        # Copy player hand
        phand = player_hand.copy()
        # Dealer plays
        dealer_play(dealer_hand, sim_shoe)
        # Determine outcome
        pv = hand_value(phand)
        dv = hand_value(dealer_hand)
        if pv > 21:
            continue  # player bust
        elif dv > 21 or pv > dv:
            wins += 1
        elif pv == dv:
            pushes += 1
        # else lose

    win_rate = wins/trials
    push_rate = pushes/trials
    return win_rate, push_rate


# Main game
def main():
    shoe = create_shoe()
    players = [[] for _ in range(7)]
    dealer = []

    seat = int(input("Choose your seat (1-7): ")) - 1

    while True:
        action = input("Add a card manually? (y/n): ").lower()
        if action != 'y':
            break
        target = input("Add card to (dealer, 1-7): ").lower()
        card = input("Card value (A,2-10,J,Q,K): ").upper()
        value = 1 if card=='A' else 10 if card in ['J','Q','K'] else int(card)
        if target=='dealer':
            dealer.append(value)
        else:
            idx = int(target)-1
            players[idx].append(value)
        if value in shoe:
            shoe.remove(value)

    for i in range(7):
        if len(players[i])==0:
            players[i] = [deal_card(shoe), deal_card(shoe)]
    if len(dealer)==0:
        dealer = [deal_card(shoe), deal_card(shoe)]

    # Player
    player_hand = players[seat]
    while True:
        print(f"\nYour hand: {display_hand(player_hand)} (Value: {hand_value(player_hand)})")
        print(f"Dealer upcard: {display_hand([dealer[0]])[0]}")
        # Estimate win probability
        win_rate, push_rate = estimate_win_prob(player_hand, dealer[0], shoe)
        print(f"Estimated win rate: {win_rate:.2f}, push rate: {push_rate:.2f}")

        if hand_value(player_hand) > 21:
            print("You busted!")
            break
        action = input("Choose action: [h]it, [s]tand, [d]ouble, s[p]lit: ").lower()
        if action=='h':
            player_hand.append(deal_card(shoe))
        elif action=='s':
            break
        elif action=='d':
            player_hand.append(deal_card(shoe))
            print("Doubled down! Hand is now:", display_hand(player_hand))
            break
        elif action=='p':
            if len(player_hand)==2 and player_hand[0]==player_hand[1]:
                split_hand = [player_hand.pop()]
                new_card = deal_card(shoe)
                player_hand.append(new_card)
                split_hand.append(deal_card(shoe))
                print(f"Split into hands: {display_hand(player_hand)} and {display_hand(split_hand)}")
                # For simplicity, just play first hand now
            else:
                print("Cannot split this hand.")
        else:
            print("Invalid action.")

    # Dealer plays
    dealer = dealer_play(dealer, shoe)
    print(f"\nDealer hand: {display_hand(dealer)} (Value: {hand_value(dealer)})")

    # Determine result
    pv = hand_value(player_hand)
    dv = hand_value(dealer)
    if pv>21:
        print("You busted. Dealer wins.")
    elif dv>21 or pv>dv:
        print("You win!")
    elif pv==dv:
        print("Push!")
    else:
        print("Dealer wins.")

if __name__=="__main__":
    main()
