from typing import List


class StateException(Exception):
    ...


class ParserException(Exception):
    ...


class State:

    def __init__(self, remainders: dict = None):
        if remainders is None:
            remainders = {}
        self.remainders = remainders

    def set_value(self, pos: int, value: int):
        if pos not in self.remainders:
            self.remainders[pos] = value
        self.remainders[pos] = min(self.remainders[pos], value)

    def items(self):
        return self.remainders.items()

    def multiply(self, s: 'State') -> 'State':
        result = State()

        for remainder, value in self.items():
            result.set_value(remainder, value)

        for remainder, value in s.items():
            result.set_value(remainder, value)

        return result

    def concatenate(self, s: 'State', k: int) -> 'State':
        result = State()

        for remainder, value in self.items():
            for s_remainder, s_value in s.items():
                result.set_value((remainder + s_remainder) % k, value + s_value)

        return result

    def star(self, k: int) -> 'State':
        if not self.remainders.keys():
            raise StateException('ERROR')

        items = ['INF' for i in range(k)]

        for remainder, value in self.items():
            for counter in range(0, k):
                weight = (remainder * counter) % k
                cost = value * counter
                if items[weight] == 'INF' or items[weight] > cost:
                    items[weight] = cost

        dp = [['INF' for i in range(k)] for j in range(len(items))]

        for weight, cost in enumerate(items):
            dp[weight][weight] = cost

        for weight in range(1, k):
            i = weight
            cost = items[weight]
            for w in range(k):
                if dp[i - 1][w] != 'INF':
                    dp[i][w] = dp[i - 1][w]
            if cost != 'INF':
                for w in range(k):
                    old_w = w - weight
                    if old_w < 0:
                        old_w += k
                    if dp[i - 1][old_w] != 'INF':
                        if dp[i][w] == 'INF' or dp[i][w] > dp[i - 1][old_w] + cost:
                            dp[i][w] = dp[i - 1][old_w] + cost

        result = State()

        for i in range(len(items)):
            for j in range(k):
                if dp[i][j] != 'INF':
                    result.set_value(j % k, dp[i][j])

        return result

    def find_answer(self, pos: int):
        if pos not in self.remainders:
            return 'INF'
        return self.remainders[pos]


class Parser:

    def __init__(self, regular: str, k: int):
        self.regular = regular
        self.k = k
        self.final_state = None

    def _calc(self) -> State:
        stack: List[State] = []
        regular = self.regular

        for c in regular:
            try:
                if c == '1':
                    stack.append(State({0: 0}))
                elif c in 'abc':
                    stack.append(State({1: 1}))
                elif c == '+':
                    state_1 = stack.pop()
                    state_2 = stack.pop()
                    stack.append(state_1.multiply(state_2))
                elif c == '.':
                    first_state = stack.pop()
                    second_state = stack.pop()
                    stack.append(first_state.concatenate(second_state, self.k))
                elif c == '*':
                    current_state = stack.pop()
                    stack.append(current_state.star(self.k))
            except Exception:
                raise ParserException("ERROR")

        if len(stack) == 1:
            return stack[0]
        else:
            raise ParserException("ERROR")

    def get_answer(self, pos: int):
        self.final_state = self._calc()
        return self.final_state.find_answer(pos)


if __name__ == '__main__':
    input_data = input().split()
    regular = input_data[0]
    k = int(input_data[1])
    l_remainder = int(input_data[2])
    print(Parser(regular, k).get_answer(l_remainder))
