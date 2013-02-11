// Fichier auto-généré à partir de la version 1302110058 du fichier de protocole

#include "atp.h"

__attribute__((weak)) void OnGetValue(unsigned long int id) {}

void SendValue(unsigned long int id, float value) {
    char bytes[] = { 
            129,
            2,
            4,
            ((char*)&id)[0],
            ((char*)&id)[1],
            ((char*)&id)[2],
            ((char*)&id)[3],
            36,
            ((char*)&value)[0],
            ((char*)&value)[1],
            ((char*)&value)[2],
            ((char*)&value)[3],
            128
        };
    SendBytes(bytes, 13);
}

int processCaptor(int id,
            unsigned char *ucharv, int ucharc,
            unsigned int *ushortv, int ushortc,
            unsigned long int *uintv, int uintc,
            char *charv, int charc,
            int *shortv, int shortc,
            long int *intv, int intc,
            float *floatv, int floatc) {
    if (id == 1) {
        OnGetValue(uintv[0]);
        return 1;
    }
    return 0;
}
