from random import randint

def get_random_char():
    """
    # random characters
    # list of list [['0','1',2','3','4','5','6','7','8','9'],
    #                ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',[...]],
    #                ['a','b','c','d','e',f','g',[...]]
    #                   ]
    #
    :return:
    """

    codes_list = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
    codes = codes_list[randint(0, 2)]
    faith = randint(0, len(codes) - 1)
    return codes[faith]

def send_email(otp: str):
    print(f"Your one time password is: {otp}. It will be active only for 5 minutes")