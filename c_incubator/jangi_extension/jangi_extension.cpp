#include <stdio.h>
#define PY_SSIZE_T_CLEAN 1
#include <Python.h>
#include <structmember.h>
#include <modsupport.h>

static struct PyModuleDef jangi_extension_module = {
    PyModuleDef_HEAD_INIT,
    "jangi_extension",
    NULL,
    -1,
    NULL
};

static PyObject *md_actor_type;
static PyObject *po_actor_type;

#include "include/dataset/actor.cpp"

PyMODINIT_FUNC
PyInit_jangi_extension(void)
{
    PyObject *m;
    m = PyModule_Create(&jangi_extension_module);
    if (m == NULL)
        return NULL;

    md_actor_type = PyImport_ImportModule("dataset.actor_type");
    if (md_actor_type == NULL)
        return NULL;

    po_actor_type = PyObject_GetAttr(
        md_actor_type,
        PyUnicode_FromString("ActorType")
    );
    if (po_actor_type == NULL)
        return NULL;

    setup_actor(m);

    return m;
}