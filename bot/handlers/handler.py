class Handler:
    """
    Parent class for all handlers.
    """

    # Handler should be implemented in constructor
    # It must be subclass of `telegram.ext.Handler`
    # (like `CommandHandler`, `MessageHandler`)
    handler = None

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

        self._register_handler()

    def _register_handler(self):
        if self.handler is None:
            raise NotImplementedError()
        self.dispatcher.add_handler(self.handler)
