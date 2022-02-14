def span(base_number: int, spread, negative: bool=False):
    if not type(base_number) in (int, float):
        raise TypeError(f"The 'base_number' argurment requires to be a number, instead of {type(base_number)}")
    if not type(spread) in (int, float, tuple):
        raise TypeError(f"The 'spread' argurment requires to be a number or a tuple type, instead of {type(spread)}")
    if not type(negative) == bool:
        raise TypeError(f"The 'negative' argurment requires to be a boolean type, instead of {type(negative)}")

    if type(spread) in (int, float):
        if negative:
            return (base_number-spread, base_number+spread)
        else:
            return (max(0, base_number-spread), base_number+spread)

    if type(spread) == tuple:
        if not len(spread) == 2:
            raise IndexError(f"The 'spread' argurment as a {type(spread)}, requeres only 2 numbers!")
        # Determining if all 2 value are numbers in tuple
        result = [True for value in spread if type(value) in (int, float)]
        if len(result) != 2:
            raise ValueError(f"The values in the spread arn't numbers!")
        if negative:
            return (base_number-spread[0], base_number+spread[1])
        else:
            return (max(0, base_number-spread[0]), base_number+spread[1])


if __name__ == "__main__":
    print(span(2, 5.6)) 
    print(len((5, 5)))
    print(span(2, (5, 5)))
    print(span(2, (5, 5), negative=True))

