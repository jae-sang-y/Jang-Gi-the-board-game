#include "board_in_c.hpp"
#include "c/board.cpp"
#include "bridge/board_iterator.hpp"
#include "bridge/board.hpp"

static struct PyModuleDef samplemodule = {
    PyModuleDef_HEAD_INIT,
    "board_in_c", /* name of module */
    "Board in C", /* Doc string (may be NULL) */
    -1,           /* Size of per-interpreter state or -1 */
    nullptr       /* Method table */
};

PyMODINIT_FUNC PyInit_board_in_c(void)
{
    static PyObject *module = PyModule_Create(&samplemodule);
    PyModule_AddType(module, GetBoardType());
    pre_init();
    return module;
}