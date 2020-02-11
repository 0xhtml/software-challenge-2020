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
    Py_DECREF(items);

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
    Py_DECREF(items);

    return nonemptyfields;
}

static PyObject* color(PyObject* self, PyObject* args){
    PyObject* colorfields = PySet_New(NULL);

    PyObject* fields;
    char* color;
    PyArg_ParseTuple(args, "Os", &fields, &color);

    PyObject* items = PyDict_Items(fields);
    Py_ssize_t len = PyList_Size(items);
    Py_ssize_t size;
    PyObject *item, *key, *val, *lastitem;
    char *itemcolor, *del;
    for (Py_ssize_t i = 0; i < len; i++){
        item = PyList_GetItem(items, i);
        key = PyTuple_GetItem(item, 0);
        val = PyTuple_GetItem(item, 1);
        size = PyList_Size(val);
        if (size == 0)
            continue;
        lastitem = PyList_GetItem(val, size - 1);
        PyArg_ParseTuple(lastitem, "ss", &itemcolor, &del);
        if(strcmp(itemcolor, color) == 0) {
            PySet_Add(colorfields, key);
        }
        Py_DECREF(item);
    }
    Py_DECREF(items);

    return colorfields;
}

static PyObject* hash(PyObject* self, PyObject* args){
    PyObject* fields;
    PyArg_ParseTuple(args, "O", &fields);

    PyObject* keys = PyDict_Keys(fields);
    int len = (int)PyList_Size(keys);
    char hash[len];
    PyList_Sort(keys);

    Py_ssize_t size;
    char *color, *type, val, overflow;
    PyObject *pieces, *piece;
    for (Py_ssize_t i = 0; i < len; i++){
        hash[i] = 1;

        pieces = PyDict_GetItem(fields, PyList_GetItem(keys, i));
        size = PyList_Size(pieces);

        for (Py_ssize_t j = 0; j < size; j++){
            piece = PyList_GetItem(pieces, j);
            PyArg_ParseTuple(piece, "ss", &color, &type);

            val = 1;
            if (strcmp(type, "BEE") == 0){
                val = val << 3;
            } else if (strcmp(type, "BEETLE") == 0){
                val = (val << 3) + 1;
            } else if (strcmp(type, "ANT") == 0){
                val = (val << 3) + 2;
            } else if (strcmp(type, "GRASSHOPPER") == 0) {
                val = (val << 3) + 3;
            } else if (strcmp(type, "SPIDER") == 0) {
                val = (val << 3) + 4;
            }
            if (strcmp(color, "RED") == 0){
                val = val << 1;
            } else if (strcmp(color, "BLUE") == 0){
                val = (val << 1) + 1;
            }

            overflow = hash[i] >> 4;
            hash[i] = (hash[i] << 4) + val + overflow;
        }
    }
    Py_DECREF(keys);

    return Py_BuildValue("y", hash);
}

static PyMethodDef methods[] = {
    {"neighbours", neighbours, METH_VARARGS, "Get neighbours of a field."},
    {"empty", empty, METH_VARARGS, "Get empty fields on board."},
    {"nonempty", nonempty, METH_VARARGS, "Get non empty fields on board."},
    {"color", color, METH_VARARGS, "Get fields of color on board."},
    {"hash", hash, METH_VARARGS, "Generate hash of fields."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "csocha", NULL, -1, methods
};

PyMODINIT_FUNC PyInit_csocha(void) {
    return PyModule_Create(&module);
}
