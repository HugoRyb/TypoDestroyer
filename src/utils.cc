#include <string>
#include <algorithm>
#include <iostream>
#include "utils.hh"
#include "output_element.hh"

inline static int min(int a, int b, int c) {
    return std::min(a, std::min(b, c));
}

static int dist[500][500];

void init_dist() {
    for (int i = 0; i < 500; i++) {
        dist[i][0] = i;
        dist[0][i] = i;
    }
}

int lev_max(char* s1, size_t len1, const std::string &s2, int maxDist, int prevLen) {
    size_t len2 = s2.length();
    prevLen = prevLen < 1 ? 1 : prevLen;

    for (int i = prevLen; i <= len1; i++) {
        int needToContinue = 0;
        for (int j = 1; j <= len2; j++) {
            int swapCost = s1[i - 1] == s2[j - 1] ? 0 : 1;
            dist[i][j] = min(dist[i - 1][j] + 1, dist[i][j - 1] + 1, dist[i - 1][j - 1] + swapCost);
            if (i > 1 && j > 1 && s1[i - 1] == s2[j - 2] && s1[i - 2] == s2[j - 1]) {
                dist[i][j] = std::min(dist[i][j], dist[i - 2][j - 2] + swapCost);
            }
            needToContinue = needToContinue || (dist[i][j] <= maxDist);
        }
        if (!needToContinue)
            return maxDist + 1;
    }
    return dist[len1][len2];
}
