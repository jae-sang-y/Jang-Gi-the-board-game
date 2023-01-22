namespace PyBoardIterator
{
    int __init__(PyObject *self, PyObject *obj, PyObject *kwrags)
    {
        BoardIterator *board_iter = (BoardIterator *)self;
        Board *board = (Board *)obj;
        board_iter->ptr = (int *)board->actors;
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

    PyObject *__next__(PyObject *self)
    {
        BoardIterator *board_iter = (BoardIterator *)self;
        if (board_iter->cnt < map_w * map_h)
        {
            return Py_BuildValue("(i,i,i)", board_iter->cnt / map_h, board_iter->cnt % map_h, board_iter->ptr[board_iter->cnt++]);
        }
        else
        {
            PyErr_SetNone(PyExc_StopIteration);
            return NULL;
        }
    }

    PyMethodDef methodMap[] = {
        {NULL},
    };
    PyMemberDef memberMap[] = {
        {NULL}};
};

static PyTypeObject *GetBoardIteratorType()
{
    static PyTypeObject pytype{};
    pytype.tp_name = "PyBoardIterator";
    pytype.tp_basicsize = sizeof(BoardIterator);
    pytype.tp_flags = Py_TPFLAGS_DEFAULT;
    pytype.tp_init = PyBoardIterator::__init__;
    pytype.tp_new = PyBoardIterator::__new__;
    pytype.tp_iternext = PyBoardIterator::__next__;
    pytype.tp_methods = PyBoardIterator::methodMap;
    pytype.tp_members = PyBoardIterator::memberMap;
    PyType_Ready(&pytype);

    return &pytype;
};
