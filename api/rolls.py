import random
from typing import Annotated
from fastapi import Depends
from api.main import app, oauth2_scheme, get_user_from_token, db
from api.exceptions import InvalidBetException, GenericServerErrorException
from main import logger


def get_number_color(number: int) -> str:
    if number == 0:
        return "green"

    # In number ranges from 1 to 10 and 19 to 28, odd numbers are red and even are black. In ranges from 11 to 18 and
    # 29 to 36, odd numbers are black and even are red.
    if number in range(1, 11) or number in range(19, 29):
        if number % 2 == 0:
            return "black"
        else:
            return "red"
    else:
        if number % 2 == 0:
            return "red"
        else:
            return "black"


@app.get("/roll/roulette")
def roll_roulette(token: Annotated[str, Depends(oauth2_scheme)],
                  bet_target: str,
                  bet_sum: int):
    user = get_user_from_token(token)
    user_cash = user["cash"]
    if user_cash < bet_sum:
        raise InvalidBetException

    # Figure out bet multiplier and check bet validity
    bet_numerical = False
    try:
        bet_target = int(bet_target)
        logger.debug("Bet is numerical...")
        if bet_target < 0 or bet_target > 36:
            raise InvalidBetException
        bet_numerical = True
        bet_multiplier = 34
    except ValueError:
        logger.debug("Failed to convert to number...")
        if bet_target.lower() == "black" or bet_target.lower() == "red" or bet_target.lower() == "green":
            bet_multiplier = 1
        else:
            raise InvalidBetException
    if bet_multiplier == 0:
        raise GenericServerErrorException

    # Roll the roulette
    roll_result = random.randint(0, 36)
    if bet_numerical:
        if roll_result == bet_target:
            cash_change = bet_sum * bet_multiplier
        else:
            cash_change = -bet_sum
    else:
        roll_color = get_number_color(roll_result)
        if roll_color == bet_target:
            cash_change = bet_sum
        else:
            cash_change = -bet_sum

    db.changeCash(user["username"], cash_change)
    return {"result": roll_result, "gain": cash_change, "new_cash": user_cash + cash_change}