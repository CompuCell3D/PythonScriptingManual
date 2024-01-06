.. _introduction:

Introduction
============

Simulations 

CompuCell3D simulations are a combination of CC3DML (CompuCell3D XML model specification format) and Python code. By itself, CC3DML is “static.” That means you specify initial cellular behaviors, and, throughout the simulation, those behavior descriptions remain unchanged. Python scripting, meanwhile, enables you to build complex simulations wherein the behaviors of individual cells change (according to user specification) as the simulation progresses. 
We assure you that unless you use Python “unwisely,” you will not hit any performance barrier for CompuCell3D simulations. It's true that there will be things that should be done in C++ because Python will be way too slow to handle certain tasks. However, throughout our years experience with CompuCell3D, we found that 90% of times Python will make your life way easier and will not impose ANY noticeable degradation in the performance. Based on our experience with biological modeling, it is by far more important to be able to develop models quickly than to have a clumsy but over-optimized code. If you have any doubts about this philosophy ask any programmer or professor of Software Engineering about the effects of premature optimization. With Python scripting you will be able to dramatically increase your productivity and it really does not matter if you know C++ or not. With Python you do not compile anything, just write script and run. If a small change is necessary, you edit source code and run again. You will waste no time dealing with compilation/installation of C/C++ modules and Python script you will write will run on any operating system (Mac, Windows, Linux). However, if you still need to develop high performance C++ modules, CompuCell3D and Twedit++ have excellent tools which make even C++ programing quite pleasurable. 
For C++ programming, check out the Developer Zone menu in Twedit++ to easily create your own module. 


