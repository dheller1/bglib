class DecisionOption:
    def __init__(self, text='Unnamed option', data=None, description=None, icon=None, image=None):
        self.text = text
        self.description = description
        self.icon = icon
        self.image = image
        self.data = data

    def __repr__(self):
        return f'DecisionOption({self.text})'

    def __str__(self):
        return self.text


class Decision:
    Pending = 0
    Decided = 1
    Aborted = 2

    def __init__(self, text, owner, options, callback=None):
        self.text = text
        self.owner = owner
        self.options = options
        self.callback = callback
        self.status = Decision.Pending
        self.picked_option = None

    def abort(self):
        assert self.status == Decision.Pending
        self.status = Decision.Aborted

    def choose(self, option):
        assert option in self.options
        self.picked_option = option.data
        self.status = Decision.Decided
        print('Chose {}'.format(option.text))
        if self.callback:
            self.callback(self)

    def decide(self):
        assert self.status == Decision.Pending
        self.choose(self.options[0])  # TODO: implement properly

    def execute(self):
        self.decide()

    def run_commandline(self):
        print(f'{self.owner}: {self.text}')
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
