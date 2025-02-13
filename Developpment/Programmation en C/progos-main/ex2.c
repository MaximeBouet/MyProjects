#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>
#define START 0;
#define END 1;

int main(){
    int tab[] = {12,1,3,6,78,45,64,14}; // SUM = 223
    int tabSize = sizeof(tab)/sizeof(int);
    int fd[2];
    int pipeid = pipe(fd);

    if(pipeid <= -1){
        printf("Error while creating the pipe");
        exit(1);
    }

    int pid = fork();

    if(pid <= -1){
        printf("Error while creating the child process");
        exit(1);
    }

    int index = END;

    if(pid == 0){
        //child
        index = START;
    }

    int sum = 0;
    for(int i = 0+((tabSize/2)*index); i < tabSize/2 + (tabSize/2)*index; i++){
        sum += tab[i];
    }

    if(pid == 0){
        //child
        close(fd[0]);
        write(fd[1], &sum, sizeof(sum));
        close(fd[1]);
    }else{
        //parent
        wait(NULL);
        int sum2 = 0;
        read(fd[0], &sum2, sizeof(sum));
        close(fd[0]);
        printf("Tab sum = %d\n", sum+sum2);
    }

    return 0;
}