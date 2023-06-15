from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def do(self):
        pass


class StartState(State):
    pass


class StateMachine(ABC):
    """A simple state machine implementation.

    Usage:
    >>> class SM(StateMachine):
    >>>     class StateA(State): # This is the starting state
    >>>         def from_B_when(self):
    >>>	            ...
    >>>         def do(self):
    >>>	            ...
    >>>     class StateB(State):
    >>>         def from_A_when(self):
    >>>            ...
    >>>        def do(self):
    >>>            ...
    >>> sm = StateMachine(StateA, states)
    """

    states: dict[type[State], State]
    current_state: State
    transitions: dict[type[State], dict[type[State], str]]

    def __init__(self):
        # Initialize states, find start state
        state_types = [cls for cls in self.__class__.__dict__.values() if isinstance(cls, type)]
        self.states = {}
        for state_type in state_types:
            if state_type in self.states:
                raise ValueError(f"Duplicate state type {state_type.__name__}")
            state = state_type()
            self.states[state_type] = state
            if issubclass(state_type, StartState):
                if hasattr(self, "current_state") and self.current_state is not None:
                    raise ValueError(
                        f"Multiple start states: {self.current_state.__class__.__name__}, {state_type.__name__}"
                    )
                self.current_state = state
        if self.current_state is None:
            raise ValueError("Start state not found among states")
        # Initialize transitions
        self.transitions = {}
        for src_state in state_types:
            for trg_state in state_types:
                if src_state == trg_state:
                    continue
                method_name = f"from_{src_state.__name__}_when"
                if hasattr(trg_state, method_name):
                    if src_state not in self.transitions:
                        self.transitions[src_state] = {}
                    self.transitions[src_state][trg_state] = method_name

    def tick(self, *args, **kwargs):
        trans = self.transitions.get(type(self.current_state), {})
        for trg_state_type, cond_fn in trans.items():
            trg_state = self.states[trg_state_type]
            if getattr(trg_state, cond_fn)(*args, **kwargs):
                self.current_state = trg_state
                break
        self.current_state.do()
