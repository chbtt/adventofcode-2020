#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MASK_LEN        36
#define MASK_STRING     "mask = "
#define MASK_STRING_LEN 7
#define MEM_STRING      "mem["
#define MEM_STRING_LEN  4
#define MAX_NUM_ENTRIES 1024

void parseMemLine(
    char* p_line,
    size_t l_line,
    size_t* p_memoryIndex,
    uint64_t* p_memoryValue
) {
    char* p_currPos = NULL;

    // there is at least one more character at *(p_line + MEM_STRING_LEN)
    *p_memoryIndex = (size_t) strtol(p_line + MEM_STRING_LEN, &p_currPos, 10);

    // "] = "
    p_currPos += 4;

    if((p_currPos - p_line) >= l_line)
    {
        printf("Encountered weird memory line (no value), exiting.\n");
        exit(EXIT_FAILURE);
    }

    *p_memoryValue = (uint64_t) strtol(p_currPos, &p_currPos, 10);
}

ssize_t getIndexIfPresent(
    uint64_t* p_array,
    size_t l_array,
    uint64_t value
) {
    for(ssize_t i = 0; i < l_array; i++)
    {
        if(p_array[i] == value)
        {
            return i;
        }
    }

    return ((ssize_t) -1);
}

uint64_t applyValueMask(
    char* p_mask,
    uint64_t value
) {
    uint64_t valueWithMask = 0;
    size_t currBitIndex = 0;

    for(ssize_t i = MASK_LEN - 1; i >= 0; i--)
    {
        switch(p_mask[i])
        {
            case '0': 
                break;
            case '1': 
                valueWithMask += UINT64_C(1) << currBitIndex;
                break;
            default: 
                valueWithMask += ((value >> currBitIndex) & UINT64_C(1)) > 0 ? (UINT64_C(1) << currBitIndex) : 0;
                break;
        }

        currBitIndex += 1;
    }

    return valueWithMask;
}

void decodeVersion1(
    uint64_t memoryIndex,
    uint64_t memoryValue,
    char* p_mask,
    uint64_t* p_indicesV1,
    uint64_t* p_valuesV1,
    size_t* pl_memory
) {
    uint64_t memoryValueWithMask = applyValueMask(p_mask, memoryValue);
    ssize_t indexIfPresent = getIndexIfPresent(p_indicesV1, *pl_memory, memoryIndex);

    // index not yet present -> append
    if(indexIfPresent == -1)
    {
        p_indicesV1[*pl_memory] = memoryIndex;
        p_valuesV1[*pl_memory] = memoryValueWithMask;
        *pl_memory += 1;

        return;
    }

    // index already present -> update
    if(indexIfPresent >= 0)
    {
        p_valuesV1[indexIfPresent] = memoryValueWithMask;

        return;
    }

    // this should never be reached
    printf("Version 1 decoder chip is broken, exiting.\n");
    exit(EXIT_FAILURE);
}

int main(
    int argc,
    char* argv[]
) {
    FILE*   p_file = NULL;
    char*   p_currLine = NULL;
    size_t  l_currLine = 0;
    ssize_t charsRead = -1;

    char* p_mask = NULL;
    uint64_t memoryIndex = 0;
    uint64_t memoryValue = 0;
    uint64_t sum = 0;
    uint64_t* p_valuesV1 = NULL;
    uint64_t* p_indicesV1 = NULL;
    size_t l_memoryV1 = 0;

    if (argc != 2)
    {
        printf("Usage: ./day14_p1 <path-to-input-data>\n");
        exit(EXIT_FAILURE);
    }
    p_file = fopen(argv[1], "r");
    if (p_file == NULL)
    {
        printf("Usage: ./day14_p1 <path-to-input-data>\n");
        exit(EXIT_FAILURE);
    }

    p_mask      = (char*)     malloc(MASK_LEN * sizeof(char));
    p_valuesV1  = (uint64_t*) malloc(MAX_NUM_ENTRIES * sizeof(uint64_t));
    p_indicesV1 = (uint64_t*) malloc(MAX_NUM_ENTRIES * sizeof(uint64_t));
    if (   p_mask == NULL
        || p_valuesV1 == NULL
        || p_indicesV1 == NULL)
    {
        printf("Could not allocate memory, exiting.\n");
        exit(EXIT_FAILURE);
    }

    while ((charsRead = getline(&p_currLine, &l_currLine, p_file)) != -1)
    {
        if(    (l_currLine >= (MASK_STRING_LEN + MASK_LEN))
            && (strncmp(p_currLine, MASK_STRING, MASK_STRING_LEN) == 0))
        {
            strncpy(p_mask, (p_currLine + 7), MASK_LEN);

            continue;
        }
        
        if(   (l_currLine > MEM_STRING_LEN) 
                && (strncmp(p_currLine, MEM_STRING, MEM_STRING_LEN) == 0))
        {
            parseMemLine(p_currLine, l_currLine, &memoryIndex, &memoryValue);
            decodeVersion1(memoryIndex, memoryValue, p_mask, p_indicesV1, p_valuesV1, &l_memoryV1);

            continue;
        }

        // this should never be reached
        printf("Encountered weird start of line, exiting.\n");
        exit(EXIT_FAILURE);
    }

    sum = 0;
    for(size_t i = 0; i < l_memoryV1; i++) {
        sum += p_valuesV1[i];
    }

    printf("Puzzle 1 sum: %" PRIu64 "\n", sum);

    fclose(p_file);
    if (p_currLine)
        free(p_currLine);

    return 0;
}
