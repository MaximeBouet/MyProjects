#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(){
    int pipetab[2];
    int pipeid = pipe(pipetab);

    if(pipeid <= -1){
        printf("Error while creating the pipe\n");
        exit(1);
    }

    /* pid = 0 : child
           > 0 : parent
           < 0 : error
    */
    int pid = fork();
    if(pid <= -1){
        printf("Error while creating new process\n");
        exit(1);
    }
    // Child
    if(pid == 0){
        close(pipetab[0]);
        char msg[64];
        printf("Entrez une phrase:\n");
        fgets(msg,64,stdin);
        int size = sizeof(msg);
        write(pipetab[1], &size, sizeof(int));
        write(pipetab[1], &msg, sizeof(msg)); // pipetab[1] : write mode
        close(pipetab[1]);

    }else{ // Parent
        wait(NULL);
        close(pipetab[1]);
        int size = 0;
        read(pipetab[0], &size, sizeof(int));
        char output[size];
        read(pipetab[0], &output, size); // pipetab[0] : read mode
        printf("Valeur saisie par l'enfant: %s\n", output);
        close(pipetab[0]);
    }
    return 0;
}