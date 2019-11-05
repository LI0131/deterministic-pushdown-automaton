import sys

class Stack:

    def __init__(self, data=None):
        self.data = data if (data and type(data) == list) else []

    def isEmpty(self):
        return len(self.data) == 0

    def pop(self):
        if not self.isEmpty():
            elem = self.data[0]
            del self.data[0]
            return elem
        else:
            return None
    
    def push(self, elem):
        self.data.insert(0, elem)

    def peek(self):
        return self.data[0]

    def __str__(self):
        return str(self.data)


class DPDA:

    def __init__(self, states, alphabet, transitions, start, accept_states):
        self.states = states if True not in [
                          type(state) != int for state in states
                      ] else sys.exit('Invalid States')
        self.alphabet = alphabet if False not in [
                            (char.isalnum() and char != 'e') for char in alphabet
                        ] else sys.exit('Invalid Alphabet')
        self.stack = Stack()
        self.transitions = transitions if False not in [
                               self._isValidTransition(trans) for trans in transitions
                           ] else sys.exit('Invalid Transitions')
        self.start = start if type(start) == int else sys.exit('Invalid Start State')
        self.accept_states = accept_states if True not in [
                                 (state not in self.states) for state in accept_states
                             ] else sys.exit('Invalid Accepting States')


    def _isValidTransition(self, transition):
        if len(transition) != 3:
            return False
        start = transition[0]
        trans = transition[1]
        end = transition[2]
        if start not in self.states or end not in self.states:
            return False
    
        if len(trans) != 2:
            sys.exit(f'{trans} is not valid PUSH or POP')

        trans_type = trans[0]
        trans_char = trans[1]

        if trans_type not in ['PUSH', 'POP']:
            sys.exit(f'{trans_type} is not in {["PUSH", "POP"]}')

        if trans_char not in self.alphabet:
            sys.exit(f'{trans_char} is not in {self.alphabet}')

        return True

    
    def _getNextState(self, state, char):
        for trans in self.transitions:
            start = trans[0]
            trans_type = trans[1][0]
            trans_char = trans[1][1]
            end = trans[2]
            if start == state and trans_char == char:
                return end, trans_type    
        return None


    def accepts(self, string):
        
        if not string.isalnum():
            return False

        chars = Stack(list(string))
        current_state = self.start
        current_char = chars.pop()

        while True:

            (current_state, stack_action) = self._getNextState(
                current_state, current_char
            ) if self._getNextState(
                current_state, current_char
            ) else (None, None)

            if current_state == None or stack_action == None:
                return False

            if stack_action == 'PUSH':
                self.stack.push(current_char)
                current_char = chars.pop()
            
            if stack_action == 'POP':
                if current_char == self.stack.peek():
                    self.stack.pop()
                    current_char = chars.pop()
                else:
                    return False

            if self.stack.isEmpty() and chars.isEmpty():
                return True


    def __repr__(self):
        return f'''
            states: {self.states} \n
            alphabet: {self.alphabet} \n
            stack: {self.stack} \n
            transitions: {self.transitions} \n
            start state: {self.start} \n
            accept state: {self.accept_states} \n
        '''


def _test():

    state = [0, 1, 2, 3, 4]
    alphabet = ['a', 'b', 'c']
    transitions = [
        [0, ('PUSH', 'a'), 1],
        [1, ('PUSH', 'b'), 1],
        [1, ('PUSH', 'c'), 2],
        [2, ('POP', 'c'), 3],
        [3, ('POP', 'b'), 3],
        [3, ('POP', 'a'), 4],
    ]
    start = 0
    accept_states = [4]

    dpda = DPDA(state, alphabet, transitions, start, accept_states)

    print(dpda)

    string = 'abbbccbbba'
    print(f'Testing with string:{string}')
    print(dpda.accepts(string))

    string = 'abbbbbbbccbbbbbbba'
    print(f'Testing with string:{string}')
    print(dpda.accepts(string))

    string = 'abbbbbbbccbba'
    print(f'Testing with string:{string}')
    print(dpda.accepts(string))

    string = 'abccbbbbba'
    print(f'Testing with string:{string}')
    print(dpda.accepts(string))


if __name__ == '__main__':
    _test()