# Damn Vulnerable Defi Brownie version

This project solely goal is to allow people that wants to learn about Smart Contracts
Security through solving OpenZeppelin's challenges created by [@tinchoabbate](https://twitter.com/tinchoabbate) [https://www.damnvulnerabledefi.xyz/](https://www.damnvulnerabledefi.xyz/), without
worring about also learning Javascript. It was also a good execuse for me to start
playing with Brownie, a Python-based development framework for the EVM created by
[Ben Hauser (iamdefinitelyhuman)](https://github.com/eth-brownie/brownie)

I "ported" Martin's exercises to Brownie. This allowed me to solve them (so far 1 to 5),
while at the same time learning about Brownie and its inner workings.

You can use this repository to solve the following challenges:

1. [Unstoppable](https://github.com/nahueldsanchez/dvd_brownie/tree/master/unstoppable)
2. [Naive receiver](https://github.com/nahueldsanchez/dvd_brownie/tree/master/naive-receiver)
3. [Truster](https://github.com/nahueldsanchez/dvd_brownie/tree/master/truster)
4. [Side Entrance](https://github.com/nahueldsanchez/dvd_brownie/tree/master/side-entrance)
5. [The Rewarder](https://github.com/nahueldsanchez/dvd_brownie/tree/master/the-rewarder)
6. [Selfie](https://github.com/nahueldsanchez/dvd_brownie/tree/master/selfie)
7. [Compromised](https://github.com/nahueldsanchez/dvd_brownie/tree/master/compromised)
8. [Puppet](https://github.com/nahueldsanchez/dvd_brownie/tree/master/puppet)

I'll continue porting the rest of the challenges once I'm able to solve them.

## How to use this project

I tried to change the least amount of things due to the fact that I'm a beginner
learning about all of this.

The idea is to leverage Brownie's flexibility in its testing suite and use it to test
our solutions for the challenges. Every challenge follows the same idea:

I created a test file called `<challenge_name>_test.py` that has a test called
`test_solution`. In this test, after setting up the scenario (that's already done)
you can write your solution, for example, let's see the test for `truster` challenge:

```Python
def test_solution():
    damn_valuable_token, truster_lender_pool = scenario_setup()
    # Solution goes here
    # Write your exploit
    # :) Good lock
    # Attacker is using accounts[1]
    #
    # SOLUTION GOES HERE
    #
    assert damn_valuable_token.balanceOf(accounts[1]) == TOKENS_IN_POOL
    assert damn_valuable_token.balanceOf(truster_lender_pool) == 0
```

As you can see, the scenario is set up and after that you can write your solution.
the assertions at the end ensure that you have correctly solved the challenge.

For the challenges that I solved I included an `exploit.py` under the `scripts`
folder that contains code used for solving the challenge (don't read it before
thinking about the problem). The same applies for contracts named `AttackerContract`.
These are part of the solution, don't spoil yourself.

## Quick Start

0) Install Brownie in a virtual environment and activate it.
1) Clone this repository. You'll find different folders for each challenge.
2) Each of these folders is a different Brownie project.
3) Change directory to the challenge you want to solve. For example, truster.
4) You can run `brownie test` to run all test. For most of the challenges I kept
the same tests that Martin created to check that the scenario is properly setup.
Your solution has to be implemented or called from the `test_solution` test.

_Note: you can use `brownie test -k test_solution` to run only the test with the
solution_

5) Write your solution in the `test_solution` placeholder that I left.
6) Test your solution runing the tests, with `brownie test -k test_solution`. If the
solution is correct, test should pass.

## Blog posts and solutions

You can find my solutions in my Blog, links below:

- [Challenges Unstoppable and Naive Receiver](https://nahueldsanchez.com.ar/Solving-DVDChallenges-1-2/)
- [Challenges Truster and Side Entrance](https://nahueldsanchez.com.ar/Solving-DVDChallenges-3-4/)
- [Challenges The rewarder and Selfie](ttps://nahueldsanchez.com.ar/Solving-DVDChallenges-5-6)
