#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>  // for usleep

#define ROWS 6
#define COLS 7

// Parse JSON manually to extract board and time_limit
int main() {
    char buffer[4096];
    if (!fgets(buffer, sizeof(buffer), stdin)) {
        fprintf(stderr, "Failed to read input\n");
        return 1;
    }

    int board[ROWS][COLS] = {0};
    int time_limit = 1000;  // default ms

    // Parse time_limit field
    char *time_ptr = strstr(buffer, "\"time_limit\"");
    if (time_ptr) {
        time_ptr = strchr(time_ptr, ':');
        if (time_ptr) {
            time_limit = atoi(time_ptr + 1);
        }
    }

    // Simulate some processing delay (e.g. evaluation)
    usleep(time_limit * 200);  // 20% of time used

    // Parse board field (very naive parser)
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

    // Prefer center-first strategy
    int preferred_cols[] = {3, 2, 4, 1, 5, 0, 6};
    for (int i = 0; i < 7; i++) {
        int col = preferred_cols[i];
        if (board[0][col] == 0) {
            printf("%d\n", col);
            return 0;
        }
    }

    // fallback
    printf("0\n");
    return 0;
}
