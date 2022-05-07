#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>

int main(int argc, char **argv) {
    void *handle;
    char *error;

    handle = dlopen ("./libhello.so", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    
    // resolve Add symbol and assign to fn ptr

    void (*print_hello)()  = dlsym(handle, "PrintHello");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
        exit(1);
    }

    print_hello();

    // close file handle when done
    dlclose(handle);
}