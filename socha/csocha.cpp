#include <Python.h>

static PyObject* neighbours(PyObject* self, PyObject* args){
    int x;
    int y;

    PyArg_ParseTuple(args, "(ii)", &x, &y);

    return Py_BuildValue(
        "(ii),(ii),(ii),(ii),(ii),(ii)",
        x + 1, y,
        x + 1, y - 1,
        x, y - 1,
        x - 1, y,
        x - 1, y + 1,
        x, y + 1
    );
}

static PyObject* empty(PyObject* self, PyObject* args){
    PyObject* emptyfields = PySet_New(NULL);

    PyObject* fields;
    PyArg_ParseTuple(args, "O", &fields);

    PyObject* items = PyDict_Items(fields);
    Py_ssize_t len = PyList_Size(items);
    PyObject *item, *key, *val;
    for (Py_ssize_t i = 0; i < len; i++){
        item = PyList_GetItem(items, i);
        key = PyTuple_GetItem(item, 0);
        val = PyTuple_GetItem(item, 1);
        if(PyList_Size(val) == 0) {
            PySet_Add(emptyfields, key);
        }
        Py_DECREF(item);
    }

    return emptyfields;
}

static PyObject* nonempty(PyObject* self, PyObject* args){
    PyObject* nonemptyfields = PySet_New(NULL);

    PyObject* fields;
    PyArg_ParseTuple(args, "O", &fields);

    PyObject* items = PyDict_Items(fields);
    Py_ssize_t len = PyList_Size(items);
    PyObject *item, *key, *val;
    for (Py_ssize_t i = 0; i < len; i++){
        item = PyList_GetItem(items, i);
        key = PyTuple_GetItem(item, 0);
        val = PyTuple_GetItem(item, 1);
        if(PyList_Size(val) != 0) {
            PySet_Add(nonemptyfields, key);
        }
        Py_DECREF(item);
    }

    return nonemptyfields;
}


static PyMethodDef methods[] = {
    {"neighbours", neighbours, METH_VARARGS, "Get neighbours of a field."},
    {"empty", empty, METH_VARARGS, "Get empty fields on board."},
    {"nonempty", nonempty, METH_VARARGS, "Get non empty fields on board."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "csocha", NULL, -1, methods
};

PyMODINIT_FUNC PyInit_csocha(void) {
    return PyModule_Create(&module);
}
