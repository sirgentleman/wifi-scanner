#define PY_SSIZE_T_CLEAN
#include <python3.8/Python.h>
#include <ifaddrs.h>
#include <stdio.h>

#define DEBUG 1

static PyObject*
get_interfaces(PyObject *self) {
    
    struct ifaddrs *ifaddrs, *ifa;
    PyObject *returnList = PyList_New(0);

    if(getifaddrs(&ifaddrs) == -1)
        printf("%s", "ERROR");

    for(ifa = ifaddrs; ifa != NULL; ifa = ifa->ifa_next) {
        PyList_Append(returnList, Py_BuildValue("[s:s, s:s]", "name", ifa->ifa_name, "netmask", ifa->ifa_netmask->sa_data));
    }

    return returnList;
}

static char nettoolbox_docs[] =
   "get_interfaces( ): Used to extract network interfaces.\n";

static PyMethodDef nettoolbox_funcs[] = {
   {"helloworld", (PyCFunction)get_interfaces, 
      METH_NOARGS, nettoolbox_docs},
      {NULL}
};

void inithelloworld(void) {
   Py_InitModule3("nettoolbox", nettoolbox_funcs,
                  "Helper module to play with local network informations");
}