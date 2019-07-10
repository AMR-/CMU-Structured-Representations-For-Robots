# CMU-Structured-Representations-For-Robots
Code to go along with the Master's Thesis "Structured Representations for Behaviors of Autonomous Robots" by Aaron M. Roth

In the **Interactive_TAIG** folder, find sample code for the Interactive TAIG demonstration.

In the **RobotNavigation** folder, find code for the OpenAI compatible RobotNavigation environment.

RobotNavigation requires the following pip packages:

    gym 0.12.1+
    numpy 1.16.3+
    Pillow 6.0.0+

Robot Navigation A can be instantiated with

```python
env = RobotNavEnv(random_hole_pos=False, is_state_cart=False, include_stage_boolean=False)
```

Robot Navigation B can be instantiated with

```python
env = RobotNavEnv(random_hole_pos=False, is_state_cart=True, include_stage_boolean=True)
```

If you use RobotNavigation in a project, please cite the following papers (bibtex found below):

 Aaron M. Roth, Nicholay Topin, Pooyan Jamshidi, and Manuela Veloso. Conservative q-improvement: Reinforcement learning for an interpretable decision-tree policy. In _arXiv 1907.01180_, 2019

 Tom M Mitchell and Sebastian B Thrun. "Explanation-based neural network learning for robot control." _In Advances in neural information processing systems,_ pages 287–294, 1993.

Bibtex:

    @article{roth2019conservative,
         title={Conservative Q-Improvement: Reinforcement Learning for an Interpretable Decision-Tree Policy},
         author={Roth, Aaron M and Topin, Nicholay and Jamshidi, Pooyan and Veloso, Manuela},
         journal={arXiv preprint arXiv:1907.01180},
         year={2019}
    }

    @inproceedings{mitchell1993explanation,
        title={Explanation-based neural network learning for robot control},
        author={Mitchell, Tom M and Thrun, Sebastian B},
        booktitle={Advances in neural information processing systems},
        pages={287--294},
        year={1993}
    }
