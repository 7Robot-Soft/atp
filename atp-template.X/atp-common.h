// Fichier auto-généré à partir de la version 1303020239 du fichier de protocole

#ifndef _COMMON_H_
#define _COMMON_H_

void SendError();

// You should define this function
void OnGetId();

void SendId(unsigned char id);

void SendTest(unsigned char B, unsigned int H, unsigned long int I, char b, int h, long int i, float f);

// You should define this function
void OnTest(unsigned char B, unsigned int H, unsigned long int I, char b, int h, long int i, float f);

int processCommon(int id,
            unsigned char *ucharv, int ucharc,
            unsigned int *ushortv, int ushortc,
            unsigned long int *uintv, int uintc,
            char *charv, int charc,
            int *shortv, int shortc,
            long int *intv, int intc,
            float *floatv, int floatc);

#endif
