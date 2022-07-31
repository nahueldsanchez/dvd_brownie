# Damn Vulnerable Defi Brownie version

This projects sole goal is to allow people that want to learn about Smart Contracts
Security through solving OpenZeppelin's challenges created by [@tinchoabbate](https://twitter.com/tinchoabbate) [https://www.damnvulnerabledefi.xyz/](https://www.damnvulnerabledefi.xyz/), without
worring about also learning Javascript. It was also a good execuse for me to start
playing with Brownie, a Python-based development framework for the EVM created by
[Ben Hauser (iamdefinitelyhuman)](https://github.com/eth-brownie/brownie)

I "ported" Martin's exercises to Brownie. This allowed me to solve them, while at the same time learning about Brownie and its inner workings.

You can use this repository to solve the following challenges:

1. [Unstoppable](https://github.com/nahueldsanchez/dvd_brownie/tree/master/unstoppable)
2. [Naive receiver](https://github.com/nahueldsanchez/dvd_brownie/tree/master/naive-receiver)
3. [Truster](https://github.com/nahueldsanchez/dvd_brownie/tree/master/truster)
4. [Side Entrance](https://github.com/nahueldsanchez/dvd_brownie/tree/master/side-entrance)
5. [The Rewarder](https://github.com/nahueldsanchez/dvd_brownie/tree/master/the-rewarder)
6. [Selfie](https://github.com/nahueldsanchez/dvd_brownie/tree/master/selfie)
7. [Compromised](https://github.com/nahueldsanchez/dvd_brownie/tree/master/compromised)
8. [Puppet](https://github.com/nahueldsanchez/dvd_brownie/tree/master/puppet)
9. [Puppet v2](https://github.com/nahueldsanchez/dvd_brownie/tree/master/puppet-v2)
10. [Free Rider](https://github.com/nahueldsanchez/dvd_brownie/tree/master/free-rider)

I'll continue porting the rest of the challenges once I'm able to solve them.

## How to use this project

I tried to change the least amount of things due to the fact that I'm a beginner
learning about all of this.

The idea is to leverage Brownie's flexibility in its testing suite and use it to test
our solutions for the challenges. Every challenge follows the same idea:

I created a test file called `<challenge_name>_test.py` that has a function called
`test_solution`. In this test, after setting up the scenario (see section below for more details)
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

The first step is to set up the scenario (again see below section for more details),
 after that you can write your solution within the test_solution() function in the test.py file.
the assertions at the end ensure that you have correctly solved the challenge.

For the challenges that I solved I included an `exploit.py` under the `scripts`
folder that contains code used for solving the challenge (this is a spoiler, don't read it before
thinking about the problem). The same applies for contracts named `AttackerContract`.
These are part of the solution, don't spoil yourself.

## Quick Start

0) Install Brownie in a virtual environment and activate it. The best way to do this is to follow this 
guide: https://iamdefinitelyahuman.medium.com/getting-started-with-brownie-part-1-9b2181f4cb99

_Note:_ that you will need dependencies including ganache-cli through node/npm (that will really be the only piece of JS you'll need)
The brownie install docs are very helpful for this as well: https://eth-brownie.readthedocs.io/en/stable/install.html

1) Clone this repository. You'll find different folders for each challenge.
2) Each of these folders is a different Brownie project.
3) Change directory to the challenge you want to solve. For example, truster.
4) If you'd like to interact with the contract, run the deploy.py setup scenario script. See section below for more information.
5) You can run `brownie test` to run all test. For most of the challenges I kept
the same tests that Martin created to check that the scenario is properly setup.
Your solution has to be implemented or called from the `test_solution` test.

_Note: you can use `brownie test -k test_solution` to run only the test with the
solution_

6) Write your solution in the `test_solution` placeholder that I left.
7) Test your solution running the tests, with `brownie test -k test_solution`. If the
solution is correct, test should pass.

## Setting up the Scenario 
To do this, we'll want to run the deploy.py script contained in the "scripts" folder. The way to do this is as follows:

0) Create a "\_\_init\_\_.py" file inside the scripts folder if it is not already there
1) Run command "brownie console" (ensure the dependencies are all installed - follow the links above in the Quick Start for more info)
2) execute "from scripts.deploy import scenario_setup" (where scenario_setup() is the name of the function)
3) Now you can call "scenario_setup()" which returns the contracts
4) You can now interact with the contract(s) via the brownie-cli; the contracts will have the same methods and functions to interact with as you see in the code itself

Please note that all of the steps above are to be able to interact with the exercise via the brownie console. If you only want to code your solution and test
it you can do as described above:

1) Write your solution in the file "test_solution.py" inside "tests"
2) Test it running: "brownie test -k test_solution"

## Blog posts and solutions

You can find my solutions in my Blog, links below:

- [Challenges Unstoppable and Naive Receiver](https://nahueldsanchez.com.ar/Solving-DVDChallenges-1-2/)
- [Challenges Truster and Side Entrance](https://nahueldsanchez.com.ar/Solving-DVDChallenges-3-4/)
- [Challenges The rewarder and Selfie](https://nahueldsanchez.com.ar/Solving-DVDChallenges-5-6)
- [Challenge Compromised](https://nahueldsanchez.com.ar/Solving-DVDChallenges-7/)
- [Challenge Puppet](https://nahueldsanchez.com.ar/Solving-DVDChallenges-8/)
- [Challenge Puppet v2](https://nahueldsanchez.com.ar/Solving-DVDChallenges-9/)
- [Challenge Free Rider](https://nahueldsanchez.com.ar/Solving-DVDChallenges-10/)
