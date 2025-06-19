# tools-handlers

Formalised abstraction for handlers.

Structures Python based applications into separate handlers. Especially useful together with `tools-arg-parse`.

The general idea is to define the action of an application in a class matching interface `IHandler`. This organises argument definitions and implicit attribute usage.

The interface looks like this:
```
class IHandler(ABC):

    Args = None

    def __init__(self, args):
        self.args = self.arg_cls()(args)

    @classmethod
    def arg_cls(cls):
        return cls.Args

    @abstractmethod
    def handle(self, *_):
        raise NotImplementedError()
```

And a sample handler might look like:
```
class HandlerModelTest(IHandler):
    class Args:
        def __init__(self, args):
            self.hidden_layer_size = args.hidden_layer_size
            self.tensor_handler = args.tensor_handler
            self.use_checkpoint = args.use_checkpoint
            self.batch_offset = args.batch_offset
            self.batch_size = args.batch_size
            self.use_cuda = args.use_cuda()
            self.datasets = args.datasets
            self.testing = args.testing
            self.points = args.points
            self.impl = args.impl

    def handle(self, *_):
        log_handler = LogHandler()
        tester = Tester(self.args, log_handler)
        tester.test()
```

Especially when using `argparse` where avoiding implicit argument reading by making them explicit at the top of the class.

Meaning that argument classes are now married to handler classes and defined in their context. Making argument passing explicit and auto-completable.

The actual `handle()` method allows for more arguments to be passed in principle. Allowing a degree of extensibility during implementation.

It's there to enable as opposed to limit. At the same time it shouldn't be used to pass what are arguments just for convenience.

Furthermore, handlers are resolved at invocation only via `importlib`. This means that we only import required dependencies when and if we need them in a given handler.

There's a possible complaint to be made that we require running of the application to know if we have all imports present in our env. And that's correct in simpler cases.

At the same time, it immediately decouples handler dependencies. Meaning depending on complexity of the use-case we can use several pyenvs depending on action invoked.

Furthermore. Some imports like `torch` or `open3d` take a long time to resolve. And if our action doesn't require them to be imported it degradates unrelated invocations.

And as a final note. It also sets us up for installable handlers over time.