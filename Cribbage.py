
# coding: utf-8

# In[ ]:

#defines the crib_score() and crib_discard() functions - with comments

#OBJECTIVE 1: THE SCORING FUNCTION

#Defines a function "crib_score()" which takes 5 string arguments and returns their cribbage score (where the first four inputs
#are player's hand and the fifth input is the starter.  Has one optional readout arugment which defaults to "num".  
#If set to "num", the function only returns the score, if set to "nice", the function will return the cribbage score 
#as well as where the score comes from (i.e. pairs, 15s, etc.).  

def crib_score(card1, card2, card3, card4, starter, readout="num"):
       
    #creates some lists which will be useful for calculating the score
    
    deal_4 = [card1, card2, card3, card4] #raw list of player's original hand
    hand = []  
    suits_4=[]
    for i in range(len(deal_4)):
        suits_4.append(deal_4[i][-1]) #saves the suits of player's kept cards; needed for scoring a flush
        hand.append(deal_4[i]) #creates a duplicate of deal_4, but we append the starter card in the next step
   
    hand.append(starter)
    
    #here are some elif conditionals which determine whether the function runs; start by setting proceed as a gate
    #and deck as a list of the valid possible entries
    
    proceed = 1   
    deck = ["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
            "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
            "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
            "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"]
    
    #iterates over player's hand, makes sure the entries are 1) valid cards and 2) non-duplicates.
    #proceed is reset to 0 if a problem is detected; an error message is printed
    
    for i in range(len(hand)):
        if hand[i] not in deck:
            print("Invalid hand!  " + str(hand[i]) + " is not a valid card.\n\nEnter cards as strings where the card value immediately precedes the suit.  E.g.\n\n2 of hearts = '2H'\nJack of spades = 'JS'\n\nThe fifth entry should be the starter.")
            proceed = 0
            break
        elif len(hand) != len(set(hand)):
            print("Invalid hand!  Your hand has duplicate cards.")
            proceed = 0
            break    
    
    if proceed == 1:
    
    #checkpoint passed; import itertools which is extremely useful for computing subsets.  Make more lists which will be used
    #for calculating specific parts of the score
    
        import itertools
        
        hand_raw = []
        hand_nums = []
        hand_runs = []
        
        #hand_raw is an intermediary list which contains the value (i.e. A,2-10,J,Q,K) of each card.

        for i in range(len(hand)):
            hand_raw.append((hand[i][:-1]))
            
        #we use hand_raw to make some other useful lists.  For computing the runs score, we need to have all cards values as 
        #sequential numbers (1-13), while for computing the 15s, we need to reassign any ace values to "1" and any jack, queen,
        #or king values to "10".  This code loops through hand_raw and creates new lists with reassigned card values for 
        #sequencing(in hand_runs) or for summation (in hand_nums).

        for i in range(len(hand_raw)):
            if hand_raw[i] == "A":
                hand_nums.append(1)
                hand_runs.append(1)
            elif hand_raw[i] == "J":
                hand_nums.append(10)
                hand_runs.append(11)
            elif hand_raw[i] == "Q":
                hand_nums.append(10)
                hand_runs.append(12)
            elif hand_raw[i] == "K":
                hand_nums.append(10)
                hand_runs.append(13)
            else:
                hand_nums.append(int(hand_raw[i]))
                hand_runs.append(int(hand_raw[i]))
                
        #Time to start scoring!

        #Pairs: use itertools to generate all unique subsets of 2 in the hand (note we use hand_runs not hand_nums, since we 
        #want face cards to be treated as having unique values from each other) and store in pairs; this is a list of
        #tuples.  We iterate over these and check if the first value equals the second - when this occurs, increase the pair
        #score by 2.
    
        score_pairs = 0

        pairs = list(itertools.combinations(hand_runs, 2))
        for i in range(len(pairs)):
            if pairs[i][0] == pairs[i][1]:
                score_pairs += 2

        ###Runs: use itertools to generate all unique subsets of 3, 4, and 5 in runs, store as list of tuples.  We
        #iterate over this list and check if it meets these conditions: a set of unique numbers for which the (max-min)
        #is equal to the length-1.  If this is true, we should have a run, i.e. a set of sequential integers.  We store the 
        #length of each run in a new list, homeruns (because there will be runs scored!).  We do this to avoid a problem:
        #we need to score double (or more0 runs (e.g. 5-5-6-7) as multiple unique runs, but we need it to not count 
        #higher-order runs as multiple lower-order runs (i.e. 4-5-6-7 is one run of 4, not two runs of 3).  So, for scoring,
        #we check if homeruns is empty; if it isn't, we identify the max of homeruns (the longest run in player's hand), 
        #and we score the length of all the runs that are equal to the longest run.

        score_runs = 0

        nums = [3,4,5]
        runs = []
        homeruns = []

        for i in range(len(nums)):
            runs.append(list(itertools.combinations(hand_runs, nums[i])))

        for i in range(len(runs)):
            for j in range(len(runs[i])):
                if len(runs[i][j]) == len(set(runs[i][j])) and max(runs[i][j])-min(runs[i][j]) == len(runs[i][j]) - 1:
                    homeruns.append(len(runs[i][j]))

        if len(homeruns) != 0:
            score_runs += max(homeruns)*homeruns.count(max(homeruns))

        #Fifteens:  We use itertools to store a list (fifs) of all subsets of the hand which could sum to fifteen.  Here, we
        #use the hand_nums list generated above, which has already converted the values of aces, jacks, queens, and kings.
        #For each subset, we simply use the sum function and add 2 points when the sum is 15.

        score_fifteens = 0

        nums2 = [2,3,4,5]
        fifs = []

        for i in range(len(nums2)):
            fifs.append(list(itertools.combinations(hand_nums, nums2[i])))

        for i in range(len(fifs)):
            for j in range(len(fifs[i])):
                if sum(fifs[i][j]) == 15:
                    score_fifteens += 2

        #Flushes:  We check for a 5 card flush first; see if the suits (already stored in suits_4) of all of player's
        #cards are equal strings, and if the starter card's suit (will be at the [-1] position) is also equal.  If this is the 
        #case, add 5 points.  If not, check for a flush in just the player's hand.  If not, there is no flush.

        score_flush = 0

        if suits_4[0] == suits_4[1] == suits_4[2] == suits_4[3] == starter[-1]:
            score_flush += 5
        elif suits_4[0] == suits_4[1] == suits_4[2] == suits_4[3]:
            score_flush += 4
        else:
            score_flush = 0


        #Nobs:  Finally, look for any jacks in the player's hand - two conditionals need to be met for player to recieve a Nobs
        #score: 1) player must have a jack (check for cards where character [0] is "J") and 2) that jack must be in the same suit
        #as the starter (check for cards where the suit, the character at [-1] in deal_4, is the same as the starter suit).

        score_nobs = 0

        for i in range(len(deal_4)):
            if deal_4[i][0] == 'J' and deal_4[i][-1] == starter[-1]:
                score_nobs += 1
                
        #Now we simply total player's score so far...
        
        total_score = score_fifteens + score_runs + score_pairs + score_flush + score_nobs
        
        #and report the result!  If readout was specified to being "nice" when calling the function, we give a more comprehensive
        #output.
        
        if readout == "num":
            return total_score
        elif readout == "nice":
            print("\nFifteens:", score_fifteens)
            print("Runs:",score_runs)
            print("Pairs:",score_pairs)
            print("Flush:",score_flush)
            print("His Nobs:",score_nobs)
        
            print("\nTotal: " + str(total_score))
            

def crib_discard(card1,card2,card3,card4,card5,card6):

    deck = ["AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
                "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
                "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
                "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"]
    

    deal_6 = [card1, card2, card3, card4, card5, card6]

    proceed = 1
    
    for i in range(len(deal_6)):
        if deal_6[i] not in deck:
            print("Invalid hand!  " + str(deal_6[i]) + " is not a valid card.")
            proceed = 0
            break
        elif len(deal_6) != len(set(deal_6)):
            print("Invalid hand!  Your hand has duplicate cards.")
            proceed = 0
            break
    
    if proceed == 1:      
    
        deck_rem = []
        for i in range(len(deck)):
            if deck[i] not in deal_6:
                deck_rem.append(deck[i])

        import itertools

        hand_possible_4 = list(itertools.combinations(deal_6, 4))


        handavg = []
        hand_final = []
        discard_final = []
        for i in range(len(hand_possible_4)):
            handx = []
            hand_final.append(list(hand_possible_4[i]))
            discard_final.append(list(set(deal_6)-set(list(hand_possible_4[i]))))
            for j in range(len(deck_rem)):
                ls=[]
                ls = list(hand_possible_4[i])
                ls.append(deck_rem[j])
                handx.append((crib_score(ls[0],ls[1],ls[2],ls[3],ls[4])))
            handavg.append(sum(handx)/len(handx))

        best_hand =(hand_final[(handavg.index(max(handavg)))])
        best_discard = list(set(deal_6)-set(best_hand))

        import matplotlib.pyplot as plt

        nice_labels = []
        for i in range(len(discard_final)):
            nice_labels.append(discard_final[i]) 
        for i in range(len(nice_labels)):
            nice_labels[i]=[w.replace("H","♡") for w in nice_labels[i]]
            nice_labels[i]=[w.replace("D","♢") for w in nice_labels[i]]
            nice_labels[i]=[w.replace("C","♣") for w in nice_labels[i]]
            nice_labels[i]=[w.replace("S","♠") for w in nice_labels[i]]

        real_nice_labels = []
        for i in range(len(nice_labels)):
            real_nice_labels.append(nice_labels[i][0]+ " " + nice_labels[i][1])

        barlist = plt.bar(range(len(handavg)), handavg, color="b")
        max_inds = []
        for i in range(len(handavg)):
            if handavg[i] == max(handavg):
                max_inds.append(i)
                barlist[i].set_color('r')
        plt.xticks(range(len(handavg)), real_nice_labels, rotation=90)
        plt.ylabel("Average score")
        plt.xlabel("Discard")
        plt.show()
        plt.figure(figsize=(10,10))

        if len(max_inds) == 1:
            print("The best discard is " + str(real_nice_labels[handavg.index(max(handavg))]) + ".")
            print("\nAverage score with this discard: " + str(max(handavg)))
        elif len(max_inds) > 1:
            print('Any of these discards are best:\n')
            for i in range(len(real_nice_labels)):
                if i in max_inds:
                    print(real_nice_labels[i])
            print("\nAverage score with these discards: " + str(max(handavg)))

