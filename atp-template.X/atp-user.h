/* 
 * File:   atp-user.h
 * Author: elie
 *
 * Created on 8 f�vrier 2013, 23:25
 */

#ifndef ATP_USER_H
#define	ATP_USER_H

// Num�ro du p�riph�rique
#define BOARD_ID 5

// Vitesse de transmission, d�faut : 115200
#define BAUDRATE 9600

// Taille des buffers de transmission
// Doit �tre sup�rieur � la longueur maximal du plus long paquet envoy�
// Valeur conseill� : 64, valeur minimal conseill� : 32
#define BUF_SIZE 64


// Priorit� de RX INTERRUPT, doit �tre sup�rieur ou �gal � 1
#define RECV_PRIO 5
// Priorit� de TX INTERRUPT, doit �tre strictement sup�rieur � RECV_PRIO
// Vous pouvez envoyer des paquets seulement depuis des interruption de priorit�
// inf�rieur strictement � SEND_PRIO (ie si vous voulez envoyer un paquet depuis
// une interruption d�clench� par un capteur, cette interruption doit �tre de
// priorit� strictement inf�rieur � SEND_PRIO ; rien ne vous emp�che d?utiliser
// des interruptions de priorit� sup�rieur � �gal � SEND_PRIO tant que vous
// n?envoy� aucun paquet).
#define SEND_PRIO 6


#define MAX_UCHAR 8
#define MAX_USHORT 8
#define MAX_UINT 8
#define MAX_CHAR 8
#define MAX_SHORT 8
#define MAX_INT 8
#define MAX_FLOAT 8

#endif	/* ATP_USER_H */

