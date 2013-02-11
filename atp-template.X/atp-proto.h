#ifndef _PROTO_H_
#define _PROTO_H_

// You should define this function
void OnGetId();

void SendTest(unsigned char B, unsigned int H, unsigned long int I, char b, int h, long int i, float f);

// You should define this function
void OnTest(unsigned char B, unsigned int H, unsigned long int I, char b, int h, long int i, float f);

void SendError();

void SendId(unsigned long int id);

int processProto(int id,
            unsigned char *ucharv, int ucharc,
            unsigned int *ushortv, int ushortc,
            unsigned long int *uintv, int uintc,
            char *charv, int charc,
            int *shortv, int shortc,
            long int *intv, int intc,
            float *floatv, int floatc);

#endif
