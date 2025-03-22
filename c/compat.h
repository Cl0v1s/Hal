#include <stdlib.h>
#include <sys/time.h>

#ifndef COMPAT_H
#define COMPAT_H

// compat 
struct timeval milisStartTimeval;

void initMillis() {
    gettimeofday(&milisStartTimeval, NULL);
}

unsigned long millis() {
    struct timeval now;
    gettimeofday(&now, NULL);
    return ((now.tv_sec - milisStartTimeval.tv_sec) * 1000000 + now.tv_usec - milisStartTimeval.tv_usec) / 1000;
}

long int local_random(int max) {
    return rand() % max;
}

#endif