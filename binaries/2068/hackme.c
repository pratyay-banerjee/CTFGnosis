// gcc -o hackme hackme.c -fPIE -pie -Wall -fomit-frame-pointer

#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 1514

int negchke(int n, const char *err) {
  if (n < 0) {
    perror(err);
    exit(1);
  }
  return n;
}

char real_password[50];

int check_password_correct(void) {
  char buf[50] = {0};

  puts("To download the flag, you need to specify a password.");
  printf("Length of password: ");
  int inlen = 0;
  if (scanf("%d\n", &inlen) != 1) {
    // peer probably disconnected?
    exit(0);
  }
  if (inlen <= 0 || inlen > 50) {
    // bad input length, fix it
    inlen = 90;
  }
  if (fread(buf, 1, inlen, stdin) != inlen) {
    // peer disconnected, stop
    exit(0);
  }
  return strcmp(buf, real_password) == 0;
}

void require_auth(void) {
  while (!check_password_correct()) {
    puts("bad password, try again");
  }
}

void handle_request(void) {
  alarm(60);
  setbuf(stdout, NULL);

  FILE *realpw_file = fopen("password", "r");
  if (realpw_file == NULL || fgets(real_password, sizeof(real_password), realpw_file) == NULL) {
    fputs("unable to read real_password\n", stderr);
    exit(0);
  }
  fclose(realpw_file);

  puts("Hi! This is the flag download service.");
  require_auth();

  char flag[50];
  FILE *flagfile = fopen("flag", "r");
  if (flagfile == NULL || fgets(flag, sizeof(flag), flagfile) == NULL) {
    fputs("unable to read flag\n", stderr);
    exit(0);
  }
  puts(flag);
}

int main(int argc, char **argv) {
  if (strcmp(argv[0], "reexec") == 0) {
    handle_request();
    return 0;
  }

  int ssock = negchke(socket(AF_INET6, SOCK_STREAM, 0), "unable to create socket");
  struct sockaddr_in6 addr = {
    .sin6_family = AF_INET6,
    .sin6_port = htons(PORT),
    .sin6_addr = /*IN6ADDR_LOOPBACK_INIT*/ IN6ADDR_ANY_INIT
  };
  int one = 1;
  negchke(setsockopt(ssock, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)), "unable to set SO_REUSEADDR");
  negchke(bind(ssock, (struct sockaddr *)&addr, sizeof(addr)), "unable to bind");
  negchke(listen(ssock, 16), "unable to listen");

  signal(SIGCHLD, SIG_IGN); /* no zombies */

  while (1) {
    int client_fd = negchke(accept(ssock, NULL, NULL), "unable to accept");
    pid_t pid = negchke(fork(), "unable to fork");
    if (pid == 0) {
      close(ssock);
      negchke(dup2(client_fd, 0), "unable to dup2");
      negchke(dup2(client_fd, 1), "unable to dup2");
      close(client_fd);
      negchke(execl("/proc/self/exe", "reexec", NULL), "unable to reexec");
      return 0;
    }
    close(client_fd);
  }
}