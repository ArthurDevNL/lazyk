#include <iostream>
#include <vector>
#include <math.h>
#include <queue>

using namespace std;

class State
{
public:
    State(vector<vector<double>> probs) : k(0)
    {
        // Take the log of the probabilities
        for (int i = 0; i < probs.size(); i++)
        {
            vector<double> log_prob_row;
            for (int j = 0; j < probs[i].size(); j++)
            {
                log_prob_row.push_back(log(probs[i][j]));
            }
            log_probs.push_back(log_prob_row);
        }

        // Set the initial assignment to be the argmax of every row
        vector<double> initial_assignment;
        for (int i = 0; i < probs.size(); i++)
        {
            double max = -INFINITY;
            int argmax = -1;
            for (int j = 0; j < probs[i].size(); j++)
            {
                if (probs[i][j] > max)
                {
                    max = probs[i][j];
                    argmax = j;
                }
            }
            initial_assignment.push_back(argmax);
        }
        assignments = {initial_assignment};
    }
    int k;
    vector<vector<double>> assignments;
    vector<vector<double>> log_probs;
    priority_queue<int> queue;

    // Compute the cost of the current assignment by summing the log_probs
    double cost(vector<double> assignment)
    {
        double cost = 0;
        for (int i = 0; i < assignment.size(); i++)
        {
            cost += log_probs[i][assignment[i]];
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

    Lazyk &operator++()
    {        
        // While the priority queue is not empty
        while (!state_.queue.empty())
        {
            // Pop the top element
            int i = state_.queue.top();
            state_.queue.pop();

            

        }

        return *this;
    }
};

int main()
{
    State state({{0.5, 0.3, 0.2}, {0.2, 0.7, 0.1}});

    // Print the initial state
    for (int i = 0; i < state.assignments[0].size(); i++)
    {
        cout << state.assignments[0][i] << " ";
    }

    // print new line
    cout << endl;

    Lazyk start(state);

    while (start.state_.k != 11)
    {
        std::cout << start.state_.k << " ";
        ++start;
    }
    std::cout << std::endl;

    return 0;
}
