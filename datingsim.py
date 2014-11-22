class Decision(object):
    """A glorified list of Choices. Represents and provides an interface to a player decision."""
    def __init__(self, choices):
        for choice in choices:
            assert isinstance(choice, Choice)
        self.choices = choices
    def select(self, *args):
        raise Error("Not yet implemented")
    def make(self, *args):
        raise Error("Not yet implemented")

class RangeDecision(object):
    def __init__(self, choices):
        Decision.__init__(self, choices)
    def make(self):
        for i, choice in enumerate(self.choices):
            print("({num}) {desc})".format(num=i, desc=choice))
        n = range_input(0, len(self.choices)-1)



class Choice(object):
    """A choice that the player can choose."""
    def __init__(self, desc, post_desc, callback):
        """
        @param desc: a one-line string desc of this choice
        @param post_desc: a string or a list of strings that are displayed in order
        after the player decides on this Choice and before callback is called
        @param callback: the function that is called upon the user deciding this choice

        >>> c = Choice('hello', 10, None) #doctest: +ELLIPSIS
        Traceback (most recent call last):
          ...
        TypeError...
        >>> c = Choice('hello', ['asdf', 'asdf', 'asdf', []], None) #doctest: +ELLIPSIS
        Traceback (most recent call last):
          ...
        TypeError...
        >>> c = Choice('hai thar', 'hello', None)
        >>> c.desc
        'hai thar'
        >>> c.post_desc
        ['hello']
        >>> print(c.callback)
        None
        """
        self.desc = desc
        self.callback = callback
        if isinstance(post_desc, str):
            post_desc = [post_desc]
        elif isinstance(post_desc, list):
            for e in post_desc:
                if not isinstance(e, str):
                    raise TypeError("{} cannot only have str elements".format(post_desc))
        else:
            raise TypeError("{} must be str or list of str".format(post_desc))
        self.post_desc = post_desc
    def __str__():
        return desc

def loc_your_house():
    input("You are ensconced within your middle class home.")
    input("Suddenly, a ringing from the doorbell.")
    print("""What will you do?
    (1)Exit through the back door
    (2)Check on the front door to see who's there""")

    n = range_input(2)

    if (n == 1):
        input("""Wearing your favorite diamond mocassins, you slip through
        the backdoor with grace and finesse.""")
        input("You are now at the park.")
        return loc_the_park
    elif (n == 2):
        input("You tiptoe to the door. Neglecting to peer through the "
                "peephole, you\n unwisely swing open the hinges.")
        input("FAAACK! It's Proto Krippendorf!")
        return boy_proto_krippendorf


# Locations
def loc_the_park():
    input("Welcome to the fucking park.")
    print("""What will you do?
    (1)Play on the swings
    (2)Peer into the trash can""")

    n = range_input(2)

    if (n == 1):
        input("Yayyyyy!")
        input("Whoppeee!")
        return
    elif (n == 2):
        input("The trash can smells a little strange.")
        input("You are reminded of the city of Berkeley before "
                "you suddenly become very sleepy...")
        return loc_dont_know


def loc_dont_know():
    input("""You don't know where you are, but this place seems nice enough
    nevertheless. You detect a faint odor of musk.""")
    input("""Mmmmm. Smexy...""")
    print("""What will you do?
    (1) Exit the game
    (2) Return to the park""")

    n = range_input(2)

    if (n == 1):
        return util_exit
    elif (n == 2):
        print("It seems that you cannot leave this wonderful place.")
        input("Your willpower is lacking.")
        return


#Boyz
def boy_proto_krippendorf():
    print("""You approach Proto Krippendorf. What will you do?
    (1) Discuss proto-pre-algebra
    (2) Genghis Khan
    (3) Abscond
    (4) Beseech him to save you""")
    
    
    n = range_input(4)

    if (n == 1):
        input("Proto Krippendorf blushes.")
        input("You blush daintily.")
    elif n == 2:
        input("Proto Krippendorf glares at you")
        input("He is clearly bored, and you have clearly failed to entertain "
                "him.")
    elif n == 3:
        input("You make a mad dash for your house.")
        input("You have successfully absconded from Proto Krippendorf.")
        return loc_your_house
    elif n == 4:
        input("Krippendorf furrows his brow in concentration as he works on" \
                " granting your potentially troublesome request.")
        print("---BEGIN SAVE ATTEMPT---")

        from save import Save
        save = Save()
        data = {"location":boy_proto_krippendorf, "starting_msg": "test msg successfully loaded!"}
        save.dict["v0.1"] = data
        print("* save object generated: {}".format(str(data)))
        
        save.BURN_BABY_BURN()
        print("* save object successfully pickled.")
    else:
        input("lol wat? at boy_proto_krippendorf")

#Utility Locations
def util_exit():
    print()
    print("Thank you for playing Shitty Dating Sim.")
    quit()

#Input Utilities
def range_input(a, b=None, convert=False):
    if (b == None):
        r = range(1, a+1)
    else:
        r = range(a, b)
    return limited_input(r, int, error_prompt='not a choice', value_error_prompt='please enter an integer')

def limited_input(seq, process_fn=None, input_prompt=None, error_prompt=None, value_error_prompt=None):
    """Takes user input and processes, but only accepts that in seq"""
    process_fn = process_fn or (lambda x: x)
    prompt = input_prompt or "==> "
    error_prompt = error_prompt or 'invalid input. please try again'
    value_error_prompt = value_error_prompt or error_prompt
    complete = False
    while not complete:
        try:
            n = process_fn(input(prompt))
            if n in seq:
                complete = True
            else:
                print(error_prompt)
        except ValueError:
            print(value_error_prompt)
    return n
    

#begin here
def main():
    # first check for existence of save
    from save import Save
    s = Save.makeFromPickle()
    if not s:
        game_loop()
    else:
        # restore existing save
        # v 0.1 save is stored as a dict in s["v0.1"]
        #    location: pointer to function of save location
        #    starting_msg: print before restoring to location
        data = s.dict["v0.1"]
        print(data["starting_msg"])
        game_loop(data["location"])
        
def game_loop(initial_loc=loc_your_house):
    prev_loc = location = initial_loc
    while(location != 'quit'):
        print("current location is {}".format(location))
        location = location()
        if location == None:
            location = prev_loc
        else:
            prev_loc = location





if (__name__ == '__main__'):
    main()
else:
    print("lol why did you import")
