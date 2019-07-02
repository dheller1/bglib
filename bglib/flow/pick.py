import logging
from bglib.flow.decision import Decision


class PickBetweenPlayers:
    UntilEmpty = 1
    OneEach = 2

    def __init__(self, choice_pool, pick_order, mode, remove_picked_choices=True):
        if len(choice_pool) < len(pick_order):
            raise ValueError('Not enough choices ({}) to make {} picks.'.format(
                len(choice_pool), len(pick_order)))
        if not remove_picked_choices and mode == PickBetweenPlayers.UntilEmpty:
            raise ValueError("'UntilEmpty' cannot be used if picked choices are not removed.")

        self.choice_pool = choice_pool
        self.mode = mode
        self.pick_order = pick_order
        self.remove_picked_choices = remove_picked_choices
        self._already_picked = []

    def next_pick(self):
        if not self.pick_order:
            raise ValueError('No picks left.')
        logging.info('Still picking: ' + ', '.join([str(picker) for picker in self.pick_order]))
        decision_maker = self.pick_order.pop(0)
        if self.mode == PickBetweenPlayers.UntilEmpty:
            self.pick_order.append(decision_maker)
        decision = Decision(owner=decision_maker, options=self.choice_pool,
                            callback=self.pick_made)
        return decision

    def pick_made(self, decision):
        assert decision.status == Decision.Decided
        logging.info('{} picked option {}'.format(decision.owner, decision.picked_option))
        self._already_picked.append((decision.owner, decision.picked_option))
        if self.remove_picked_choices:
            self.choice_pool.remove(decision.picked_option)

    def run_commandline(self):
        while self.choice_pool and self.pick_order:
            self.next_pick().run_commandline()
