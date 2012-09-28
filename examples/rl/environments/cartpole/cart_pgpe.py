#!/usr/bin/env python
#########################################################################
# Reinforcement Learning with PGPE on the CartPoleEnvironment 
#
# Requirements: pylab (for plotting only). If not available, comment the
# last 3 lines out
#########################################################################
__author__ = "Thomas Rueckstiess, Frank Sehnke"
__version__ = '$Id$' 

from pybrain.tools.example_tools import ExTools
from pybrain.tools.shortcuts import buildNetwork
from pybrain.rl.environments.cartpole import CartPoleEnvironment, BalanceTask
from pybrain.rl.agents import OptimizationAgent
from pybrain.optimization import PGPE
from pybrain.rl.experiments import EpisodicExperiment

batch=1 #number of samples per learning step
prnts=100 #number of learning steps after results are printed
epis=int(4000/batch/prnts) #number of roleouts
numbExp=10 #number of experiments
et = ExTools(batch, prnts) #tool for printing and plotting

for runs in range(numbExp):
    # create environment
    env = CartPoleEnvironment()    
    # create task
    task = BalanceTask(env, 200, desiredValue=None)
    # create controller network
    net = buildNetwork(4, 1, bias=False)
    # create agent with controller and learner (and its options)
    agent = OptimizationAgent(net, PGPE(storeAllEvaluations = True))
    et.agent = agent
    # create the experiment
    experiment = EpisodicExperiment(task, agent)

    #Do the experiment
    for updates in range(epis):
        for i in range(prnts):
            experiment.doEpisodes(batch)
        et.printResults((agent.learner._allEvaluations)[-50:-1], runs, updates)
    et.addExps()
et.showExps()
