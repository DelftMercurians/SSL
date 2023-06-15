import unittest

from lightning7_ssl.state_machine import StartState, State, StateMachine


class StateMachineTests(unittest.TestCase):
    def test_initial_state(self):
        class SM(StateMachine):
            class StateA(StartState):
                def do(self):
                    pass

            class StateB(State):
                def do(self):
                    pass

        sm = SM()
        self.assertIsInstance(sm.current_state, SM.StateA)

    def test_do_is_called(self):
        class SM(StateMachine):
            class StateA(StartState):
                def do(self):
                    self.called = True

        sm = SM()
        sm.tick()
        self.assertTrue(getattr(sm.current_state, "called", False))

    def test_transition(self):
        class SM(StateMachine):
            class StateA(StartState):
                def do(self):
                    pass

            class StateB(State):
                def do(self):
                    pass

                def from_StateA_when(self):
                    return True

        sm = SM()
        self.assertIsInstance(sm.current_state, SM.StateA)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateB)

    def test_transition_chain(self):
        class SM(StateMachine):
            class StateA(StartState):
                def do(self):
                    pass

            class StateB(State):
                def do(self):
                    pass

                def from_StateA_when(self):
                    return True

            class StateC(State):
                def do(self):
                    pass

                def from_StateB_when(self):
                    return True

            class StateD(State):
                def do(self):
                    pass

                def from_StateC_when(self):
                    return True

            class StateE(State):
                def do(self):
                    pass

                def from_StateD_when(self):
                    return True

            class StateF(State):
                def do(self):
                    pass

                def from_StateE_when(self):
                    return True

        sm = SM()
        self.assertIsInstance(sm.current_state, SM.StateA)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateB)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateC)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateD)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateE)
        sm.tick()
        self.assertIsInstance(sm.current_state, SM.StateF)
