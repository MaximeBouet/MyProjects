#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <signal.h>
#include <fcntl.h>

int main(){

    int fd[2];
    int pipeid = pipe(fd);

    int pid1 = fork();
    int pid2 = fork();

    if(pid1 <= -1){
        printf("Error while creating the child processes");
        exit(1);
    }

    if(pid2 <= -1){
        printf("Error while creating the child processes");
        exit(1);
    }   


    if(pid1 == 0 && pid2 != 0){
        //child ls
        close(fd[0]);
        printf("(PID=%d) Execution de l'instruction ls\n", pid1);
        dup2(fd[1],STDOUT_FILENO);
        close(fd[1]);
        execlp("ls", "ls", NULL);
    }
    
    if(pid2 == 0 && pid1 != 0){
        wait(NULL);
        close(fd[1]);
        printf("(PID=%d) Execution de l'instruction grep\n", pid2);
        dup2(fd[0], STDIN_FILENO);
        close(fd[0]);
        execlp("grep", "grep", "ex", STDIN_FILENO);
    }else if(pid1 != 0 && pid2 != 0){
        wait(NULL);
        printf("(PID=%d) Process parent\n", pid1);
    }
	

    return 0;
}
