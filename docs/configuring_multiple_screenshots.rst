Configuring Multiple Screenshots
================================

Starting with CompuCell3d version 3.7.9 users have an option to save multiple screenshots directly from simulation running
in GUI or GUI-less mode. Keep in mind that there sia already another way of producing simulation screenshots that requires
users to first save complete snapshots (VTK-files) and then replaying them in the player and at that time users would take
screenshots.

The feature we present here is a very straightforward way to generate multiple screenshots with, literally, few clicks.

The process is very simple - you open up a simulation in the Player and use "camera button" on lattice configurations
you want to save. In doing so CompuCell3D will generate .json screenshot description file that will be saved with along
the simulation code som that from now on every run of the simulation will generate the same set of screenshots. Obviously
we can delete this file if we no longer wish to generate the screenshots.

Let's review all the steps necessary to configure multiple screenshots. First we need to enable screenshot output from
the configuration page:

|screenshots_config_4_conf|


Fig 1. Enable screenshot output - check box next to "Save image every Nth MCS" and choose screenshot output frequency

|screenshots_config_1|

Fig.2 Open up simulation and start running it. Press "Pause" and click "camera button" (the button next to
"Take screenshot" tool-tip) on the graphics configuration you would like to save.

|screenshots_config_2|

|screenshots_config_2|

Fig.2 Repeat the sam process on other graphics configurations you would like to output as screenshots. Here we are
adding screenshots for FGF field and for the cell field in 3D. See above




.. |screenshots_config_1| image:: images/screenshots_config_1.png
   :width: 3.5000in
   :height: 2.5526in


.. |screenshots_config_2| image:: images/screenshots_config_2.png
   :width: 3.5000in
   :height: 2.5526in

.. |screenshots_config_3| image:: images/screenshots_config_3.png
   :width: 3.5000in
   :height: 2.5526in

.. |screenshots_config_4_conf| image:: images/screenshots_config_4_conf.png
   :width: 3.5000in
   :height: 2.5526in








