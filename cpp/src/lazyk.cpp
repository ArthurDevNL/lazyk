#include <iostream>
#include <vector>
#include <math.h>
#include <queue>
#include <unordered_set>
#include <algorithm>
#include <unordered_map>
#include <optional>

using namespace std;

struct vector_hash
{
    size_t operator()(const std::vector<int> &vec) const
    {
        size_t seed = vec.size();
        for (const auto &i : vec)
        {
            seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

struct assignment
{
    vector<int> argsrt_assignment;
    double cost;
};


struct CompareAssignment
{
    bool operator()(const assignment& lhs, const assignment& rhs) const
    {
        // The priority_queue returns the largest element first,
        // so we need to reverse the comparison to prioritize by smallest cost.
        return lhs.cost > rhs.cost;
    }
};


class State
{
public:
    State(vector<vector<double>> probs) : k(0)
    {
        // Take the log of the probabilities
        for (int i = 0; i < probs.size(); i++)
        {
            vector<double> log_prob_token;
            for (int j = 0; j < probs[i].size(); j++)
            {
                log_prob_token.push_back(-log(probs[i][j]));
            }
            log_probs.push_back(log_prob_token);
        }

        // Compute the argsort of the log_probs
        for (int i = 0; i < log_probs.size(); i++)
        {
            vector<int> argsort_token;
            for (int j = 0; j < log_probs[i].size(); j++)
            {
                argsort_token.push_back(j);
            }
            sort(argsort_token.begin(), argsort_token.end(), [&](int a, int b)
                 { return log_probs[i][a] < log_probs[i][b]; });
            argsrt_log_probs.push_back(argsort_token);
        }

        // Set y0 to be 0 for every token
        vector<int> y0(probs.size(), 0);

        frontier = {y0};
        argsrt_assignments = {y0};
        next_best.insert({y0, 0});

        // Add y0 to the queue with its cost
        queue.push({y0, cost(y0)});
    }

    // Initial pre-computed useful values
    vector<vector<int>> argsrt_log_probs;
    vector<vector<double>> log_probs;

    // Current state stuff
    int k;
    unordered_set<vector<int>, vector_hash> frontier;
    unordered_map<vector<int>, int, vector_hash> next_best;
    vector<vector<int>> argsrt_assignments;
    priority_queue<assignment, vector<assignment>, CompareAssignment> queue;

    // Compute the cost of the current assignment by summing the log_probs
    double cost(vector<int> argsrt_assignment)
    {
        double cost = 0;
        for (int i = 0; i < argsrt_assignment.size(); i++)
        {
            int idx = argsrt_log_probs[i][argsrt_assignment[i]];
            cost += log_probs[i][idx];
        }
        return cost;
    }

    bool operator!=(const State &other) const
    {
        return k != other.k;
    }
};

class Lazyk
{
public:
    Lazyk(State state) : state_(state)
    {
    }
    State state_;

    bool operator!=(const Lazyk &other) const
    {
        return state_ != other.state_;
    }

    State operator*() const
    {
        return state_;
    }

    vector<int> *nextBest(vector<int> argsrt_assignment)
    {
        if (state_.next_best[argsrt_assignment] == state_.log_probs.size())
        {
            // We have already computed the next best for this assignment. Return null
            return nullptr;
        }

        // Get the token index for the next best change
        int next_best_i = state_.next_best[argsrt_assignment];

        // Get the i-th best change
        vector<double> next_diffs;
        for (int j = 0; j < state_.log_probs[next_best_i].size(); j++)
        {
            // If we reached the last label for this assignment, set it to infinity
            if (argsrt_assignment[next_best_i] == state_.log_probs[0].size())
            {
                next_diffs.push_back(INFINITY);
            }
            else
            {
                int prob_idx = state_.argsrt_log_probs[next_best_i][argsrt_assignment[next_best_i]];
                double curr_log_prob = state_.log_probs[next_best_i][prob_idx];
                double next_log_prob = state_.log_probs[next_best_i][j];
                next_diffs.push_back(state_.log_probs[next_best_i][j] - state_.log_probs[next_best_i][argsrt_assignment[next_best_i]]);
            }
        }

        // Get the argsort of the diffs
        vector<int> argsrt_next_diffs;
        for (int j = 0; j < next_diffs.size(); j++)
        {
            argsrt_next_diffs.push_back(j);
        }
        sort(argsrt_next_diffs.begin(), argsrt_next_diffs.end(), [&](int a, int b)
             { return next_diffs[a] < next_diffs[b]; });

        // Set the next best to be the next best change by creating a copy of argsrt_assignment and incrementing the next best
        vector<int> *next_best = new vector<int>(argsrt_assignment);
        (*next_best)[next_best_i] = argsrt_next_diffs[state_.next_best[argsrt_assignment]];
        return next_best;
    }

    void addNextBest(vector<int> argsrt_assignment)
    {
        vector<int> *yj = nextBest(argsrt_assignment);

        // While yj is not null and exists in the frontier, find the next best
        while (yj != nullptr && state_.frontier.find(*yj) != state_.frontier.end())
        {
            state_.next_best[argsrt_assignment]++;
            yj = nextBest(argsrt_assignment);
        }

        if (yj != nullptr)
        {
            // Add yj to the frontier
            state_.frontier.insert(*yj);

            // Add the argsrt_assignment to the queue with the cost of yj
            state_.queue.push({argsrt_assignment, state_.cost(*yj)});
        }
    }

    Lazyk &operator++()
    {
        if (state_.queue.empty())
        {
            // Fail
            return *this;
        }

        // Increment k
        state_.k++;

        // Pop the top element
        assignment yk = state_.queue.top();
        state_.queue.pop();

        // Get the next best state
        vector<int> *next_best = nextBest(yk.argsrt_assignment);

        // throw an exception if next best is null because we shouldn't have queued it then
        if (next_best == nullptr)
        {
            throw "Next best should not be null";
        }

        addNextBest(yk.argsrt_assignment);
        addNextBest(*next_best);

        // Set next_best on the current state
        return *this;
    }
};

int main()
{
    State state({{0.5, 0.3, 0.2}, {0.2, 0.7, 0.1}});

    // Print the initial state
    for (int i = 0; i < state.argsrt_assignments[0].size(); i++)
    {
        cout << state.argsrt_assignments[0][i] << " ";
    }

    // print new line
    cout << endl;

    Lazyk start(state);

    int i = 0;
    while (start.state_.k != 11 && i < 20)
    {
        std::cout << start.state_.k << " ";
        ++start;
        i++;
    }
    std::cout << std::endl;

    return 0;
}
