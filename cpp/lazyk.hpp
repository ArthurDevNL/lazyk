#include <iostream>  
#include <vector>  
#include <math.h>  
#include <queue>  
#include <unordered_set>  
#include <algorithm>  
#include <unordered_map>  
#include <optional>  
#include <numeric>  
  
using namespace std;  
  
struct vector_hash;  
struct assignment;  
struct CompareAssignment;  
  
class State;  
class Lazyk;  
  
struct vector_hash {  
    size_t operator()(const std::vector<int> &vec) const;  
};  
  
struct assignment {  
    vector<int> argsrt_assignment;  
    double cost;  
};  
  
struct CompareAssignment {  
    bool operator()(const assignment &lhs, const assignment &rhs) const;  
};  
  
class State {  
public:  
    State(vector<vector<double>> probs);  
  
    vector<vector<int>> argsrt_log_probs;  
    vector<vector<double>> log_probs;  
  
    int k;  
    unordered_set<vector<int>, vector_hash> frontier;  
    unordered_map<vector<int>, int, vector_hash> next_best;  
    unordered_map<vector<int>, vector<int>, vector_hash> next_diff_cache;  
    vector<vector<int>> argsrt_assignments;  
    priority_queue<assignment, vector<assignment>, CompareAssignment> queue;  
    ulong max_k;  
  
    double argsrt_cost(vector<int> argsrt_assignment);  
    double cost(vector<int> assignment);  
  
    bool operator!=(const State &other) const;  
};  
  
class Lazyk {  
public:  
    Lazyk(State state);  
  
    State state_;  
  
    bool operator!=(const Lazyk &other) const;  
    State operator*() const;  
    vector<int> *nextBest(vector<int> argsrt_assignment);  
    void addNextBest(vector<int> argsrt_assignment);  
    vector<int> get_assignment();  
    bool end();  
    Lazyk &operator++();  
};  
