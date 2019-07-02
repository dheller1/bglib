class DecisionOption:
    def __init__(self, name='Unnamed option', data=None, description=None, icon=None, image=None):
        self.name = name
        self.description = description
        self.icon = icon
        self.image = image
        self.data = data

    def __repr__(self):
        return f'DecisionOption({self.name})'

    def __str__(self):
        return self.name


class Decision:
    Pending = 0
    Decided = 1
    Aborted = 2

    def __init__(self, owner, options, callback=None):
        self.owner = owner
        self.options = options
        self.callback = callback
        self.status = Decision.Pending
        self.picked_option = None

    def abort(self):
        assert self.status == Decision.Pending
        self.status = Decision.Aborted

    def decide(self):
        assert self.status == Decision.Pending
        self.picked_option = self.options[0]  # TODO: implement properly
        self.status = Decision.Decided
        if self.callback:
            self.callback(self)

    def execute(self):
        self.decide()

    def run_commandline(self):
        print(f'{self.owner}, please choose:')
        for i, opt in enumerate(self.options):
            print(' [{}] {}'.format(i+1, opt))

        allowed_input = [str(i+1) for i in range(len(self.options))]
        user_input = None
        while user_input not in allowed_input:
            user_input = input('Choice: ')

        self.picked_option = self.options[int(user_input)-1]
        self.status = Decision.Decided
        if self.callback:
            self.callback(self)
        return self.picked_option
