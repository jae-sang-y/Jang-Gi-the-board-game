namespace PyBoard
{
    int __init__(PyObject *self, PyObject *args, PyObject *kwrags)
    {
        Board *board = (Board *)self;
        board->init();

        return 0;
    }

    PyObject *__new__(PyTypeObject *cls, PyObject *args, PyObject *kwargs)
    {
        return cls->tp_alloc(cls, 0);
    }

    PyObject *__alloc__(PyTypeObject *cls, Py_ssize_t nitmes)
    {
        return PyType_GenericAlloc(cls, nitmes);
    }
    PyObject *is_ended_game(PyObject *self, void *)
    {
        Board *board = (Board *)self;
        if (board->is_ended_game())
            Py_RETURN_TRUE;
        else
            Py_RETURN_FALSE;
    }

    PyObject *__iter__(PyObject *self)
    {
        return PyObject_CallOneArg((PyObject *)GetBoardIteratorType(), self);
    }

    PyMethodDef methodMap[] = {
        //PyMethodDef{"__iter__", __iter__, METH_NOARGS, nullptr},
        {NULL},
    };
    PyMemberDef memberMap[] = {
        PyMemberDef{
            "turn_own_team",
            T_INT,
            offsetof(Board, turn_own_team),
            READONLY},
        PyMemberDef{
            "actors",
            T_INT,
            offsetof(Board, actors),
            READONLY},
        {NULL}};
    PyGetSetDef getsetMap[] = {
        PyGetSetDef{"is_ended_game", is_ended_game, nullptr, nullptr, nullptr},
        {NULL}};
};

static PyTypeObject *GetBoardType()
{
    static PyTypeObject pytype{};
    pytype.tp_name = "Board";
    pytype.tp_basicsize = sizeof(Board);
    pytype.tp_flags = Py_TPFLAGS_DEFAULT;
    pytype.tp_init = PyBoard::__init__;
    pytype.tp_new = PyBoard::__new__;
    pytype.tp_iter = PyBoard::__iter__;
    pytype.tp_methods = PyBoard::methodMap;
    pytype.tp_members = PyBoard::memberMap;
    pytype.tp_getset = PyBoard::getsetMap;
    PyType_Ready(&pytype);
    return &pytype;
};
