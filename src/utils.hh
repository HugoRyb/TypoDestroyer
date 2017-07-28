#pragma once
#include <string>
#include "trie_node.hh"

int lev_max(MyString& new_word, const char* s1, size_t len1, const std::string& s2, int maxDist);
int lev_zero(MyString& new_word, const char* s1, size_t len1, const std::string& s2);
void init_dist();
