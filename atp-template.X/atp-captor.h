#ifndef _CAPTOR_H_
#define _CAPTOR_H_

#define BOARD_ID 2
#define BOARD_NAME Captor
#define BOARD_PROCESSOR processCaptor

void SendValue(unsigned long int id, float value);

// You should define this function
void OnGetValue(unsigned long int id);

int processCaptor(int id,
            unsigned char *ucharv, int ucharc,
            unsigned int *ushortv, int ushortc,
            unsigned long int *uintv, int uintc,
            char *charv, int charc,
            int *shortv, int shortc,
            long int *intv, int intc,
            float *floatv, int floatc);

#endif
