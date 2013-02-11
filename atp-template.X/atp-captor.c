// Fichier auto-généré à partir de la version 1302110058 du fichier de protocole

#include "atp.h"

__attribute__((weak)) void OnGetValue(unsigned char id) {}

__attribute__((weak)) void OnSetThreshold(unsigned char id, float threshold) {}

void SendValue(unsigned char id, float value) {
    char bytes[] = { 
            129,
            2,
            1,
            id,
            36,
            ((char*)&value)[0],
            ((char*)&value)[1],
            ((char*)&value)[2],
            ((char*)&value)[3],
            128
        };
    SendBytes(bytes, 10);
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
        OnGetValue(ucharv[0]);
        return 1;
    }
    if (id == 3) {
        OnSetThreshold(ucharv[0],
            floatv[0]);
        return 1;
    }
    return 0;
}
