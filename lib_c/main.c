/**
 * Entrypoint of our programs.
*/
#include <stdio.h>
#include <stdlib.h>

#define SLOT_NUMBER 256 

void *memory_slots[SLOT_NUMBER] = {0};

void cleanup() {
    for (size_t i = 0; i < SLOT_NUMBER; ++i) {
        if (memory_slots[i] != 0) {
            free(memory_slots[i]);
        }
    }
}

void reserve_slot(size_t slot, size_t size) {
    if (memory_slots[slot] != 0) {
        printf("Memory slot %zu is already in use", slot);
        cleanup();
        exit(1);
    }
    memory_slots[slot] = malloc(size);
    if (memory_slots[slot] == 0) {
        printf("Failed to reserve slot %zu, system error", slot);
        cleanup();
        exit(1);
    }
}

void print(int x) {
    printf("%d\n", x);
}

int main() {
    // %%main
    cleanup();
    return (0);
}
