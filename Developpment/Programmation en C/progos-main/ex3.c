#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(){
    int fd[2];
    int fd2[2];
    int pipeid = pipe(fd);
    int pipeid2 = pipe(fd2);

    if(pipeid <= -1 || pipeid2 <= -1){
        printf("Error while creating the pipe");
        exit(1);
    }

    int pid = fork();

    if(pid <= -1){
        printf("Error while creating the child process");
        exit(1);
    }

    if(pid == 0){
        //child
        close(fd[1]);
        int nbr = 0;
        read(fd[0], &nbr, sizeof(nbr));
        close(fd[0]);
        int nbr2 = nbr*5;
        write(fd2[1], &nbr2, sizeof(nbr2));
        close(fd2[1]);
    }else{
        //parent
        int nbr = 0;
        printf("Entrez un nombre:\n");
        scanf("%d", &nbr);
        write(fd[1], &nbr, sizeof(nbr));
        close(fd2[1]);
        read(fd2[0], &nbr, sizeof(nbr));
        close(fd2[0]);
        printf("Nombre retourné par le child: %d\n", nbr);
    }

    return 0;
}