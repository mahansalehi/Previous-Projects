
def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global card_disabled
    global MONTHLY_INTEREST_RATE
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    last_country = None
    last_country2 = None   
    
    card_disabled = False 
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(test_day, test_month, previous_day, previous_month):
    
    '''If and only if date (test_day, test_month) is the same as 
    date (previous_day, previous_month) or occurs later 
    than date (previous_day, previous_month), return True.
    
    Arguments:
    test_day -- a number
    test_month -- a number
    previous_day -- a number
    previous_month -- a number
    '''
    
    if previous_month == test_month:
        if test_day >= previous_day:
            return True
            
    if test_month < previous_month:
        return False
    
    if previous_month < test_month:
        return True
    
    return False


def test_date_same_or_later():
    
    ''' Test the function date_same_or_later for all cases.
    The base is 3 because there are 3 cases; <, >, and =.
    The number of digits is 2.
    The number of possible choices is 3^2 = 9.
    '''
    
    assert date_same_or_later     (2, 3, 2, 3)
    assert date_same_or_later     (2, 3, 1, 3)
    assert not date_same_or_later (1, 3, 2, 3)
   
    assert not date_same_or_later (2, 2, 2, 3)
    assert not date_same_or_later (2, 2, 1, 3)
    assert not date_same_or_later (1, 2, 2, 3)
    
    assert date_same_or_later     (2, 4, 2, 3)
    assert date_same_or_later     (2, 4, 1, 3)
    assert date_same_or_later     (1, 4, 2, 3)
    
        
def all_three_different(c1, c2, c3):
    
    '''If and only if the values of the three
    strings c1, c2, and c3 are all different from
    each other, return True.
    
    Arguments:
    
    c1 -- a valid country given as a capitalized string
    c2 -- a valid country given as a capitalized string
    c3 -- a valid country given as a capitalized string
    '''
    
    if c1 != c2 and c1 != c3 and c2 != c3:
        return True
    else:
        return False
        
        
def test_all_three_different ():
    
    ''' Test the function all_three_different.
    The base is actually the total number of countries (hundreds)
    but the smallest number of countries we can use to satisfy
    the test is 3; c1, c2, and c3.
    The number of digits is 3.
    The number of possible choices is 3^3 = 27.
    '''
    
    assert not all_three_different ("a", "a", "a")
    assert not all_three_different ("a", "a", "b")
    assert not all_three_different ("a", "a", "c")
    
    assert not all_three_different ("a", "b", "a")
    assert not all_three_different ("a", "b", "b")
    assert     all_three_different ("a", "b", "c")
    
    assert not all_three_different ("a", "c", "a")
    assert all_three_different     ("a", "c", "b")
    assert not all_three_different ("a", "c", "c")  
      
    
    assert not all_three_different ("b", "a", "a")
    assert not all_three_different ("b", "a", "b")
    assert     all_three_different ("b", "a", "c")
    
    assert not all_three_different ("b", "b", "a")
    assert not all_three_different ("b", "b", "b")
    assert not all_three_different ("b", "b", "c")
    
    assert     all_three_different ("b", "c", "a")
    assert not all_three_different ("b", "c", "b")
    assert not all_three_different ("b", "c", "c")  
    
    
    assert not all_three_different ("c", "a", "a")
    assert     all_three_different ("c", "a", "b")
    assert not all_three_different ("c", "a", "c")
    
    assert     all_three_different ("c", "b", "a")
    assert not all_three_different ("c", "b", "b")
    assert not all_three_different ("c", "b", "c")
    
    assert not all_three_different ("c", "c", "a")
    assert not all_three_different ("c", "c", "b")
    assert not all_three_different ("c", "c", "c")  
            
            
def purchase(amount, day, month, country):
    
    '''Add amount to balanced owed unless:
    
    1. Input date is before last update date.
    2. Transaction is made in three different 
       countries in a row (card is disabled).
    3.Card is disabled.
    
    If any of these three conditions are true,
    return "error".
    
    Call the function amount_owed() to update interest.
    
    Arguments:
    
    amount -- assume number greater than 0.
    day -- a number
    month -- a number
    Assume day and month are valid dates in 2016.
    country -- a valid country, given as a 
    capitalized string
    '''
    
    global card_disabled

    if card_disabled:
        return "error"
    
    global last_update_day
    global last_update_month
    
    if not date_same_or_later (day, month, last_update_day, last_update_month):
        return "error"
        
    global last_country
    global last_country2
    
    if all_three_different (country, last_country, last_country2):
        card_disabled = True
        return "error"
        
    amount_owed(day, month)
    
    last_update_day = day
    last_update_month = month
    
    last_country2 = last_country
    last_country = country
    
    if last_country2 == None:
        last_country2 = country
    
    global cur_balance_owing_recent
    cur_balance_owing_recent += amount
    

def test_purchase():
    
    ''' Test the function purchase.'''

    #Test purchase on earlier date
    
    initialize()
    
    assert purchase (0, 2, 3, 0) == None
    assert purchase (0, 1, 3, 0) == "error"
    assert purchase (0, 2, 3, 0) == None
    assert purchase (0, 3, 3, 0) == None
    
    #Test country error
    
    initialize()
    
    assert purchase (0, 0, 0, "Canada") == None
    assert purchase (0, 0, 0, "France") == None
    assert purchase (0, 0, 0, "Canada") == None
    assert purchase (0, 0, 0, "France") == None
    assert purchase (0, 0, 0, "U.S.") == "error"
    
    #Test for amount owed after purchase
    
    initialize()
    
    assert purchase (10, 5, 1, "Canada") == None
    assert cur_balance_owing_recent == 10
    
    #Test for no transaction when date error occurs
    
    initialize()
    
    assert purchase (10, 5, 1, "Canada") == None
    assert purchase (10, 4, 1, 0) == "error"
    assert cur_balance_owing_recent == 10, "No purchase after error"
    assert purchase (10, 5, 1, "Canada") == None
    assert cur_balance_owing_recent == 20
    
    #Test for no transaction after country error
    
    assert purchase (10, 5, 1,"France") == None
    assert cur_balance_owing_recent == 30
    assert purchase (10, 5, 1, "U.S.") == "error"
    assert cur_balance_owing_recent == 30
    
    #Test for no transaction after card disabled
    
    assert purchase (10, 5, 1, "Canada") == "error"


def amount_owed(day, month):
    
    '''If and only if there wasn't a simluation 
    operation on a date later than (day, month) 
    (ex. purchase of check amount owed) return total
    amount owed (amount accruing interests and amount
    of purchases). Otherwise, return "error"
    
    Arguments:
    
    day -- a number
    month -- a number
    Assume day and month are valid dates in 2016.
    '''
    
    global last_update_day
    global last_update_month
    
    if not date_same_or_later (day, month, last_update_day, last_update_month):
        return "error"
    
    global cur_balance_owing_recent
    global cur_balance_owing_intst
    
    global MONTHLY_INTEREST_RATE
    
    for x in range (last_update_month, month):
        
        cur_balance_owing_intst *= (1+MONTHLY_INTEREST_RATE)
        
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_recent = 0
        
    last_update_month = month
    last_update_day = day
    
    return cur_balance_owing_intst + cur_balance_owing_recent


def test_amount_owed():
    
    #There should be no money accruing interest
    #on the money spent on purchases during 
    #the month that a purchase is made
    
    initialize()
    purchase (10, 5, 1, "Canada")
    assert amount_owed (30, 1) == 10
    assert cur_balance_owing_recent == 10
    assert cur_balance_owing_intst == 0
    
    #If the cur_balance_owing_recent is not paid
    #during the month of purchase, it will be 
    #transferred into cur_balance_owing_intst
    
    assert amount_owed (1, 2) == 10
    assert cur_balance_owing_recent == 0
    assert cur_balance_owing_intst == 10
    
    #If the cur_balance_owing_intst is not paid off
    #during the month it was transferred, it will
    #be charged an interest of 5% at the end of the 
    #month regardless of purchases made that month.
    
    purchase (10, 4, 3, "Canada")
    assert cur_balance_owing_recent == 10
    assert cur_balance_owing_intst == 10*1.05
    assert amount_owed (5, 3) == 10 + 10*1.05
    
    #Test for interest accruing starting with a purchase in
    # #January, until December
    #Due to rounding error, the difference between the 
    #amount_owed and estimated value is considered true
    #if the absolute value of the difference is less than 
    #an arbitrarily small value -- 0.0005
    
    initialize()
    purchase (10, 1, 1, "Canada")
    for i in range (2, 13):
        assert abs(amount_owed (1, i) - 10*1.05**(i-2)) < 0.0005
        
        
def pay_bill(amount, day, month):
    
    '''Pay off balance.
    If amount does not equal total amount
    owed, the first payment goes to pay the amount 
    that is accruing interest, and only then to 
    pay the amount that is not accruing interest.
    If amount is greater than total amount owed, 
    return "error"
    
    Arguments:
    
    amount -- a number greater than zero
    day -- a number
    month -- a number
    Assume day and month are valid dates in 2016.
    '''
    
    global last_update_day
    global last_update_month
    
    if not date_same_or_later (day, month, last_update_day, last_update_month):
        return "error"
        
    amount_owed(day, month)
        
    last_update_day = day
    last_update_month = month
    
    global cur_balance_owing_recent
    global cur_balance_owing_intst
    
    if amount == (cur_balance_owing_intst + cur_balance_owing_recent):
        cur_balance_owing_recent, cur_balance_owing_intst = 0, 0
    elif amount > (cur_balance_owing_intst + cur_balance_owing_recent):
        return "error"
    else:
        if amount <= cur_balance_owing_intst:
            cur_balance_owing_intst -= amount
        elif amount > cur_balance_owing_intst:
            amount = amount - cur_balance_owing_intst
            cur_balance_owing_intst = 0
            cur_balance_owing_recent -= amount


def test_pay_bill ():
    
    #Test for no simulation after date error
    
    initialize()
    purchase (10, 5, 1, "Canada")
    assert pay_bill (10, 4, 1) == "error"
    pay_bill (10, 5, 1)
    assert amount_owed (6, 1) == 0
    
    #Test for amount equal to cur_balance_owing_recent 
    #+ cur_balance_owing_intst
    
    initialize()
    purchase (10, 5, 1, "Canada")
    purchase (10, 5, 3, "U.S.")
    purchase (10, 5, 6, "Canada")
    pay_bill (33.1800625, 7, 6)
    assert amount_owed (8, 6) == 0
    
    #Test for amount greater than cur_balance_owing_recent 
    #+ cur_balance_owing_intst
    
    initialize()
    purchase (10, 5, 1, "Canada")
    purchase (10, 5, 3, "U.S.")
    purchase (10, 5, 6, "Canada")
    pay_bill (40, 7, 6)
    assert amount_owed (8, 6) == 33.1800625
    
    #Test for amount equal to cur_balance_intst
    
    initialize()
    purchase (10, 5, 1, "Canada")
    purchase (10, 5, 3, "U.S.")
    purchase (10, 5, 6, "Canada")
    pay_bill (23.1800625, 7, 6)
    assert amount_owed (8, 6) == 10
    
    #Test for amount greater than cur_balance_intst
    #but less than cur_balance_owing_recent 
    #+ cur_balance_owing_intst
    
    initialize()
    purchase (10, 5, 1, "Canada")
    purchase (10, 5, 3, "U.S.")
    purchase (10, 5, 6, "Canada")
    pay_bill (30.1800625, 7, 6)
    assert amount_owed (8, 6) == 3
            

initialize()	

if __name__ == '__main__':
    
    test_date_same_or_later()
    test_all_three_different()
    test_purchase()
    test_amount_owed()
    test_pay_bill()

    initialize()
    
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      #30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      #31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      #71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      #41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      #83.65375 
    print(purchase(50, 3, 5, "United States"))  #error    (3 diff. countries in 
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      #83.65375 (no change, purchase
                                                #          declined)
    print(purchase(150, 3, 5, "Canada"))        #error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      #85.8364375 
                                                #(43.65375*1.05+40)
    print (pay_bill(90, 5, 6))                  #error (paid too much!)