/* 
 * File:   atp.h
 * Author: elie
 *
 * Created on 6 février 2013, 23:52
 */
#ifndef ATP_H
#define	ATP_H

void AtpInit();

void AtpSendBytes(char *bytes, int count);
void AtpSendText(char *str);
void AtpSendId();

#endif	/* ATP_H */

