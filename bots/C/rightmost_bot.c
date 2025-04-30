#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define ROWS 6
#define COLS 7

int main() {
    char buffer[4096];
    if (!fgets(buffer, sizeof(buffer), stdin)) {
        return 1;
    }

    int board[ROWS][COLS] = {0};
    int time_limit = 1000;

    char *time_ptr = strstr(buffer, "\"time_limit\"");
    if (time_ptr) {
        time_ptr = strchr(time_ptr, ':');
        if (time_ptr) {
            time_limit = atoi(time_ptr + 1);
        }
    }

    usleep(time_limit * 500);  // optional

    int r = 0, c = 0;
    char *p = strchr(buffer, '[');
    while (p && r < ROWS) {
        p++;
        if (*p == '[') {
            c = 0;
            p++;
            while (*p && *p != ']') {
                if (*p >= '0' && *p <= '9') {
                    board[r][c++] = *p - '0';
                }
                p++;
            }
            r++;
        }
    }

    for (int col = COLS - 1; col >= 0; col--) {
        if (board[0][col] == 0) {
            printf("%d\n", col);
            return 0;
        }
    }

    printf("0\n");
    return 0;
}
