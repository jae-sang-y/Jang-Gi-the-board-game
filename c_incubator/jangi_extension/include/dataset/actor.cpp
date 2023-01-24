#include "../dataset/actor.h"
struct PyActor {
    PyObject_HEAD
//    pyObject* firdt;
    int actor_code;
};

PyMemberDef Actor_members[] = {
    {"actor_code", T_INT, offsetof(PyActor, actor_code), 0, NULL},
    {NULL, 0, 0, 0, NULL }
};

static void Actor_dealloc(PyActor* self) {
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject*
Actor_new(PyTypeObject* cls, PyObject *args, PyObject *kwds)
{
    PyActor* self;
    self = (PyActor*)cls->tp_alloc(cls, 0);
    if (self != NULL) {
        self->actor_code = 0;
    }
    return (PyObject*) self;
}

static int
Actor_init(PyActor* self, PyObject *args, PyObject *kwds)
{
    static char* kwlist[] = {"actor_type", "is_red", NULL};
    int t_actor_type = 0;
    bool t_is_red = 0;
    PyObject* t_action_type_enum = NULL;

    if (
        !PyArg_ParseTupleAndKeywords(
            args,
            kwds,
            "|Ob",
            kwlist,
            &t_action_type_enum,
            &t_is_red
        )
    ) {
        return -1;
    }

    t_actor_type = PyLong_AsLong(
        PyObject_GetAttr(
            t_action_type_enum,
            PyUnicode_FromString("value")
        )
    );

    if (t_is_red == 0 && t_actor_type != 0)
    {
        t_actor_type += 7;
    }

    self->actor_code = t_actor_type;
    return 0;
}

static PyObject*
Actor_to_actor_code(PyActor* self) {
    PyObject* result = Py_BuildValue("i", self->actor_code);
    return result;
}

static PyObject*
Actor_actor_type_getter(PyActor* self) {

    PyObject* kwargs = Py_BuildValue("{si}", "value", actor_get_actor_type(self->actor_code));;


    PyObject* result = PyObject_Call(
        po_actor_type, PyTuple_New(0), kwargs
    );

    return result;
}

static PyObject*
Actor_is_red_getter(PyActor* self) {
    PyObject* result = Py_BuildValue("i", actor_is_red(self->actor_code));
    return result;
}

static PyObject*
Actor_move_cases(PyActor* self, PyObject *args, PyObject *kwds) {
    PyObject *t_board, *t_pos;
    static char* kwlist[] = {"board", "pos", NULL};
    Pos t_c_pos;
    Board t_c_board;


    if (
        !PyArg_ParseTupleAndKeywords(
            args,
            kwds,
            "OO",
            kwlist,
            &t_board,
            &t_pos
        )
    ) {
        return NULL;
    }


    int rc = PyArg_ParseTuple(t_pos, "ii", &t_c_pos.x, &t_c_pos.y);

    PyObject* board_data = PyObject_GetAttr(
        t_board,
        PyUnicode_FromString("data")
    );
    for (int x = 0; x < 9; ++x)
    {
        PyObject* column = PyList_GetItem(
            board_data,
            x
        );
        for (int y = 0; y < 10; ++y)
        {
            t_c_board.actor_code[x][y] = ((PyActor*)
//            PyObject_GetAttr(
                PyList_GetItem(
                    column,
                    y
                )
//                PyUnicode_FromString("value")
//                )
            )->actor_code;
        }
    }


    PyObject* result = PyList_New(0);
    for (const auto& move_case : actor_move_cases(
            self->actor_code,
            t_c_board,
            t_c_pos
        )
    ) {

        PyObject* tup = Py_BuildValue("(i,i)", move_case.x, move_case.y);

        PyList_Append(result, tup);

    }

    return result;
}

PyMethodDef Actor_methods[] = {
    {"to_actor_code", (PyCFunction)Actor_to_actor_code, METH_NOARGS, NULL},
    {"move_cases", (PyCFunction)Actor_move_cases, METH_VARARGS|METH_KEYWORDS, NULL},
    {NULL, NULL, 0 , NULL},
};

PyGetSetDef Actor_props[] = {
    {"actor_type", (getter) Actor_actor_type_getter, NULL, NULL, NULL},
    {"is_red"    , (getter) Actor_is_red_getter    , NULL, NULL, NULL},
    {NULL},
};

PyTypeObject ActorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "jangi_extension.Actor",
    sizeof(PyActor),
    NULL, /* tp_itemsize */
    (destructor)Actor_dealloc, /* tp_dealloc */
    NULL, /* tp_print */
    NULL, /* tp_getattr */
    NULL, /* tp_setattr */
    NULL, /* tp_reserved */
    NULL, /* tp_repr */
    NULL, /* tp_as_number */
    NULL, /* tp_as_sequence */
    NULL, /* tp_as_mapping */
    NULL, /* tp_hash */
    NULL, /* tp_call */
    NULL, /* tp_str */
    NULL, /* tp_getattro */
    NULL, /* tp_setattro */
    NULL, /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    NULL, /* tp_doc */
    NULL, /* tp_traverse */
    NULL, /* tp_clear */
    NULL, /* tp_richcompare */
    NULL, /* tp_weaklistoffset */
    NULL, /* tp_iter */
    NULL, /* tp_iternext */
    Actor_methods, /* tp_methods */
    Actor_members, /* tp_members */
    Actor_props, /* tp_getset */
    NULL, /* tp_base */
    NULL, /* tp_dict */
    NULL, /* tp_descr_get */
    NULL, /* tp_descr_set */
    NULL, /* tp_dictoffset */
    (initproc)Actor_init, /* tp_init */
    NULL, /* tp_alloc */
    Actor_new, /* tp_new */
    NULL, /* tp_free */
};


void setup_actor(PyObject *m)
{
    printf("Hello 0\n");
    Py_INCREF(&ActorType);
    printf("Hello 00\n");
    PyType_Ready(&ActorType);
    printf("Hello 000\n");
    PyModule_AddObject(m, "Actor", (PyObject*)&ActorType);
    printf("Hello 0000\n");
}