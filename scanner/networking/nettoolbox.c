#define PY_SSIZE_T_CLEAN
#include <python3.9/Python.h>
#include <ifaddrs.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if.h>

static PyObject*
get_interfaces(PyObject *self) {
    
    struct ifaddrs *ifaddr = NULL, *ifa = NULL;
    PyObject *returnList = PyList_New(0);
    if(getifaddrs(&ifaddr) == -1)
        perror("ERROR");

    for(ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if(ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_INET) {
            if((ifa->ifa_flags & IFF_LOOPBACK) != 0 || (ifa->ifa_flags & IFF_UP) == 0)
                continue;

            void *tmpAddrPtr = &((struct sockaddr_in *)(ifa->ifa_addr))->sin_addr;

            char addressBuffer[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, tmpAddrPtr, addressBuffer, INET_ADDRSTRLEN);
            
            tmpAddrPtr = &((struct sockaddr_in *)(ifa->ifa_netmask))->sin_addr;
            char maskBuffer[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, tmpAddrPtr, maskBuffer, INET_ADDRSTRLEN);
            PyList_Append(returnList, Py_BuildValue("{s:s, s:s, s:s}", "name", ifa->ifa_name, "address", addressBuffer, "mask", maskBuffer));
        }
    }

    freeifaddrs(ifaddr);
    return returnList;
}

static char nettoolbox_docs[] =
   "get_interfaces( ): Used to extract network interfaces.\n";

static PyMethodDef nettoolbox_funcs[] = {
   {"get_interfaces", (PyCFunction)get_interfaces, 
      METH_NOARGS, nettoolbox_docs},
      {NULL}
};

static struct PyModuleDef Nettoolbox = {
    PyModuleDef_HEAD_INIT,
    "nettoolbox",
    "Usage: helper module to play with local network informations",
    -1,
    nettoolbox_funcs
};

PyMODINIT_FUNC PyInit_nettoolbox(void) {
    return PyModule_Create(&Nettoolbox);
}