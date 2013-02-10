#include <p33Fxxxx.h>      /* Includes device header file                     */
#include <stdint.h>        /* Includes uint16_t definition                    */
#include <stdbool.h>       /* Includes true/false definition                  */
#include <timer.h>         /* Include timer fonctions                         */
#include <libpic30.h>
#include <uart.h>
#include <string.h>

#include "atp.h"
#include "atp-user.h"
#include "header.h"

#if SEND_PRIO <= RECV_PRIO
#error "SEND_PRIO must be strictely superior than RECV_PRIO"
#endif
#if SEND_PRIO > 7
#error "SEND_PRIO must be inferior or equal to 7"
#endif
#if RECV_PRIO < 1
#error "RECV_PRIO must be superior or equal to 1"
#endif

#define BRGVAL ((FCY / BAUDRATE / 16) - 1)

void sendInit();
void recvInit();

void AtpInit() {

    sendInit();
    recvInit();

    OpenUART1(UART_EN & UART_IDLE_CON & UART_IrDA_DISABLE & UART_MODE_FLOW
        & UART_UEN_00 & UART_DIS_WAKE & UART_DIS_LOOPBACK
        & UART_DIS_ABAUD & UART_UXRX_IDLE_ONE & UART_BRGH_SIXTEEN
        & UART_NO_PAR_8BIT & UART_1STOPBIT,
          UART_INT_TX_BUF_EMPTY & UART_IrDA_POL_INV_ZERO
        & UART_SYNC_BREAK_DISABLED & UART_TX_ENABLE & UART_TX_BUF_NOT_FUL & UART_INT_RX_CHAR
        & UART_ADR_DETECT_DIS & UART_RX_OVERRUN_CLEAR,
          BRGVAL);

    int config = UART_RX_INT_EN & UART_TX_INT_EN;
    switch (RECV_PRIO) {
        case 1:
            config &= UART_RX_INT_PR1;
            break;
        case 2:
            config &= UART_RX_INT_PR2;
            break;
        case 3:
            config &= UART_RX_INT_PR3;
            break;
        case 4:
            config &= UART_RX_INT_PR4;
            break;
        case 5:
            config &= UART_RX_INT_PR5;
            break;
        case 6:
            config &= UART_RX_INT_PR6;
            break;
        case 7:
            config &= UART_RX_INT_PR7;
            break;
    }
    switch (SEND_PRIO) {
        case 2:
            config &= UART_TX_INT_PR2;
            break;
        case 3:
            config &= UART_TX_INT_PR3;
            break;
        case 4:
            config &= UART_TX_INT_PR4;
            break;
        case 5:
            config &= UART_TX_INT_PR5;
            break;
        case 6:
            config &= UART_TX_INT_PR6;
            break;
        case 7:
            config &= UART_TX_INT_PR7;
            break;
    }
    ConfigIntUART1(config);

    __builtin_write_OSCCONL(OSCCON & 0xBF);
     _RP5R = 3; // RP5 (pin 14) = U1TX (p.167)
    _U1RXR = 6; // RP6 (pin 15) = U1RX (p.165)
    __builtin_write_OSCCONL(OSCCON | 0x40);
}

//##############################################################################


typedef struct {
    char buf[BUF_SIZE];
    int begin;
    int end;
    int full;
    int flag;
} buffer;

volatile buffer buffers[SEND_PRIO];

volatile int runLevel;

void sendInit() {
    int i;
    for (i = 0 ; i < SEND_PRIO ; i++) {
        buffer buf = buffers[i];
        buf.begin = 0;
        buf.end = 0;
        buf.full = 0;
        buf.flag = 0;
    }
    runLevel = -1;
}

void AtpSendText(char *str)
{
    AtpSendBytes(str, strlen(str));
}

void AtpSendId() {
    char bytes[5] = { 129, 255, 1, 5, 128 };
    AtpSendBytes(bytes, 5);
}

void AtpSendError() {
    char bytes[5] = { 129, 0, 128 };
    AtpSendBytes(bytes, 3);
}

void AtpSendBytes(char *bytes, int count)
{
    if (count == 0) return; // no data !

    int prio = INTTREGbits.ILR3; // cpu pending interrupt priority level

    int end = buffers[prio].end;

    int pos;
    for (pos = 0 ; pos < count ; pos++) {
        buffers[prio].buf[end++] = bytes[pos];
        if (end == BUF_SIZE) end = 0;
        if (end == buffers[prio].begin) {
            buffers[prio].full = 1;
            if (prio == RECV_PRIO) {
                buffers[prio].end = end;
                buffers[prio].flag = 1;
                IFS0bits.U1TXIF = 1;
            }
            while (buffers[prio].full);
        }
    }

    buffers[prio].end = end;
    buffers[prio].flag = 1;
    IFS0bits.U1TXIF = 1;
}

//##############################################################################

int packetState;
int packetId;
int packetDataType;
int packetData[16];
int packetDataLen;
int packetDataPtr;

unsigned char ucharv[MAX_UCHAR];
int ucharc;
unsigned int ushortv[MAX_USHORT];
int ushortc;
unsigned long int uintv[MAX_UINT];
int uintc;
char charv[MAX_CHAR];
int charc;
int shortv[MAX_SHORT];
int shortc;
long int intv[MAX_INT];
int intc;
float floatv[MAX_FLOAT];
int floatc;

void processPacket() {
    led = led ^ 1;
    if (packetId == 254) {
        AtpSendId();
    }
#ifdef ANSWER_ERROR
    else {
        AtpSendError();
    }
#endif
}

void recvInit() {
    packetState = 1;
    packetId = 0;
    packetDataType = 0;
    packetDataLen = 0;
    packetDataPtr = 0;
    ucharc = 0;
    ushortc = 0;
    uintc = 0;
    charc = 0;
    shortc = 0;
    intc = 0;
    floatc = 0;
}

int checkDataType(unsigned int type) {
    switch (type) {
        case 1:
        case 2:
        case 4:
        case 17:
        case 18:
        case 20:
        case 36:
            return 1;
        default:
            return 0;
    }
}

void recv(unsigned int pending) {
    switch (packetState) {
        case 1:
            if (pending == 129) {
                packetState = 2;
                ucharc = 0;
            } else {
                // error
            }
            break;
        case 2:
            packetId = pending;
            packetState = 3;
            break;
        case 3:
            if (pending == 128) {
                processPacket();
                packetState = 1;
            } else if (checkDataType(pending)) {
                packetDataType = pending;
                packetState = 4;
                packetDataLen = pending & 0b1111;
                packetDataPtr = 0;
            } else {
                // error
                packetState = 1;
            }
            break;
        case 4:
            packetData[packetDataPtr++] = pending;
            if (packetDataPtr == packetDataLen) {
                float f;
                switch (packetDataType) {
                    case 1:
                        ucharv[ucharc++] = packetData[0];
                        break;
                    case 2:
                        ushortv[ushortc] = packetData[0] << 8;
                        ushortv[ushortc++] &= packetData[1];
                        break;
                    case 4:
                        uintv[uintc] = (unsigned long int)packetData[3] << 24;
                        uintv[uintc] &= (unsigned long int)packetData[2] << 16;
                        uintv[uintc] &= packetData[1] << 8;
                        uintv[uintc++] &= packetData[0];
                        break;
                    case 17:
                        charv[charc++] = packetData[0];
                        break;
                    case 18:
                        shortv[shortc] = packetData[0] << 8;
                        shortv[shortc++] &= packetData[1];
                        break;
                    case 20:
                        intv[intc] = (long int)packetData[3] << 24;
                        intv[intc] &= (long int)packetData[2] << 16;
                        intv[intc] &= packetData[1] << 8;
                        intv[intc++] &= packetData[0];
                        break;
                    case 36:
                        ((char*)&f)[3] = packetData[3];
                        ((char*)&f)[2] = packetData[2];
                        ((char*)&f)[1] = packetData[1];
                        ((char*)&f)[0] = packetData[0];
                        floatv[floatc++] = f;
                        /*floatv[floatc] = (long int)packetData[3] << 24;
                        floatv[floatc] &= (long int)packetData[2] << 16;
                        floatv[floatc] &= (long int)packetData[1] << 8;
                        floatv[floatc++] &= (long int)packetData[0];*/
                        //floatv[floatc++] = i;
                        break;
                }
                packetState = 3;
            }
            break;
    }
}

//##############################################################################

/*************************************************
 *          RX Interrupt
 *
 *************************************************/


void __attribute__((interrupt, no_auto_psv)) _U1RXInterrupt(void)
{
    _U1RXIF = 0;      // On baisse le FLAG

    while(DataRdyUART1()) {
        recv(ReadUART1());
    }
}

/*************************************************
 *          TX Interrupt
 *
 *************************************************/

void updateRunLevel() {
    int i;
    for (i = RECV_PRIO ; i >= 0 ; i--) {
        if (buffers[i].flag) {
            runLevel = i;
            return;
        }
    }
    runLevel = -1;
}

void __attribute__((__interrupt__, no_auto_psv)) _U1TXInterrupt(void)
{
    IFS0bits.U1TXIF = 0; // clear TX interrupt flag

    if (runLevel < 0) {
        updateRunLevel();
    }
    
    while (!U1STAbits.UTXBF && runLevel >= 0) {
        if (buffers[runLevel].begin != buffers[runLevel].end || buffers[runLevel].full) {
            buffers[runLevel].full = 0;
            WriteUART1(buffers[runLevel].buf[buffers[runLevel].begin++]);
            if (buffers[runLevel].begin == BUF_SIZE) buffers[runLevel].begin = 0;
        }
        if (buffers[runLevel].begin == buffers[runLevel].end) {
            buffers[runLevel].flag = 0;
            updateRunLevel();
        }
    }
}