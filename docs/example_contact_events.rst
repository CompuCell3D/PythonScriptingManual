How to Detect Contact
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single Contact Event
------------------------------------

At every time step, you should check each cell's neighbors, then mark a dictionary property
to prevent the event from happening again for the same cell.  
CC3D is not event-driven, so code to handle contact events should go in the ``step`` function. 
Here is how to trigger an action when two cells collide.

.. code-block:: python

    def start(self):
        #Add the `touching_macrophage_cell` attribute to every cell.
        for cell in self.cell_list:
            cell.dict['touching_macrophage_cell'] = False
        

    def step(self, mcs):
        """
        Check every bacteria to see if it is touching a macrophage.
        If it is, and it has never touched a macrophage, then set the property to True.
        """
        for cell in self.cell_list_by_type(self.BACTERIA):
            for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
                if neighbor: #Ensure we are not looking at the Medium
                    if neighbor.type == self.MACROPHAGE:
                        if cell.dict['touching_macrophage_cell'] == False:
                            cell.dict['touching_macrophage_cell'] = True
                            print("Contact happened!")

Periodic Contact Events
------------------------------------

Notice that this interaction can only happen once. 
If you want contact events to happen periodically, then you should limit how often the event triggers.
The below code shows how to trigger a contact event every 100 MCS.
Essentially, we check the previous time stamp of a contact event, ``last_cell_touch_time``,
to see if it was at least 100 MCS in the past.

.. code-block:: python

    def start(self):
        #Set the property to -100 so that the interaction can still happen on MCS=0.
        for cell in self.cell_list:
            cell.dict['last_cell_touch_time'] = -100

    def step(self, mcs):
    #...
                    if neighbor.type == self.MACROPHAGE:
                        if cell.dict['last_cell_touch_time'] - mcs >= 100:
                            print("Contact happened!")
                            cell.dict['last_cell_touch_time'] = mcs
                            #From here, you could change the cell's type or kill the cell
                            #if you wish to stop future interactions.

Using Contact to Transmit Cell Signals
------------------------------------------------------------------------

Cells that need to maintain contact for an extended period would use similar code. 
For example, a CD4 T cell receptor requires time for an interaction with an antigen-presenting cell
(Also called the MHC class II and TCR cell-cell interaction).

.. code-block:: python

    def start(self):
        #Now -1 is a placeholder value to show that there
        for cell in self.cell_list:
            cell.dict['signal_received'] = 0

    def step(self, mcs):
        for cell in self.cell_list_by_type(self.CD4_T_CELL):
            for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
                if neighbor and neighbor.type == self.AP_CELL:
                    if cell.dict['signal_received'] < 50:
                        cell.dict['signal_received'] += 1
                    elif cell.dict['signal_received'] == 50:
                        print("Signal sufficient!")
