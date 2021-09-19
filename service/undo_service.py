class UndoRedoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UndoService:
    def __init__(self):
        self._history = []
        self._index = 0
        self._flag = False

    def recordOperation(self, operation):
        """
        Record the operation
        :param operation:
        :return:
        """
        if self._flag:
            return
        if self._index < len(self._history):
            self._history = self._history[:self._index]
        self._history.append(operation)
        self._index += 1

    def undo(self):
        """
        Undo function
        :return:
        """
        if self._index == 0:
            raise UndoRedoException('No more undos!')
        self._index -= 1
        self._flag = True
        self._history[self._index].undo()
        self._flag = False

    def redo(self):
        """
        Redo function
        :return:
        """
        if self._index == len(self._history):
            raise UndoRedoException('No more redos')
        self._flag = True
        self._history[self._index].redo()
        self._index += 1
        self._flag = False


class FunctionCall:
    def __init__(self, function, *parameters):
        self._function = function
        self._params = parameters

    def call(self):
        """
        Executes the function
        :return:
        """
        self._function(*self._params)


class Operation:
    def __init__(self, undoFunction, redoFunction):
        self._undo = undoFunction
        self._redo = redoFunction

    def undo(self):
        self._undo.call()

    def redo(self):
        self._redo.call()


# class CascadeOperation:
#    def __init__(self):
#        self._operation = []
#
#    def append(self, func):
#        self._operation.append(func)
#
#    def undo(self):
#        for elem in self._operation:
#            elem.undo()
#
#    def redo(self):
#        for elem in self._operation:
#            elem.redo()