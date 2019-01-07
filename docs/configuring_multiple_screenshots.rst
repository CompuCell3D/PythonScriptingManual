Configuring Multiple Screenshots
================================

Starting with CompuCell3d version 3.7.9 users have an option to save multiple screenshots directly from simulation running
in GUI or GUI-less mode. Keep in mind that there sia already another way of producing simulation screenshots that requires
users to first save complete snapshots (VTK-files) and then replaying them in the player and at that time users would take
screenshots.

The feature that we present here is a very straightforward way to generate multiple screenshots with , literally, few clicks.

The process is very simple - you open up a simulation in the Player and use "camera button" on lattice configurations
you want to save. In doing so CompuCell3D will generate .json screenshot description file that will be saved with along
the simulation code som that from now on every run of the simulation will generate the same set of screenshots. Obviously
we can delete this file if we no longer wish to generate the screenshots.

Let's review all the steps necessary to configure multiple screenshots:

Fig.1 Open up simulation and start running it. Press "Pause" and click "camera button" on the graphics
 configuration you would like to save.









