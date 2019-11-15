# Robotics praktikum

## Using NAO robot model on V-REP simulator

### Manage the NAO robot scene

#### Start the V-REP program

from command line: `$ vrep.sh`

#### Create new robot scene

from the main menu, select `File\ New scene`

#### Choose physics engine `Open Dynamics Engine`

from the main menu, select `Simulation\ Using ODE physics engine`

#### Choose NAO robot model from `Model browser`

from the toolbox `[Model browser]\ robots\ mobile\ NAO.ttm`, drag and drop the
robot to the simulating page

#### Start/ stop/ suspend robot scene simulation

from the main menu, select `Simulation\ <Start>/<Stop>/<Suspend> simulation`

#### Save the robot scene

from the main menu, select `File\ Save scene`

#### Open an existed robot scene

from the main menu, select `File\ Open scene`

#### Scene properties

Scene properties can be examined, adjusted, or added new objects, objects by
expanding (right click on items) the toolbox `[Scene hierarchy]\ [sub-menus]`:

* Cameras
* Floor
* Lights
* Robot (NAO)
* ...

### Program (using python) to control the NAO robot model

NOTE: The default V-REP's NAO robot model has a pre-recorded joints movements
for demonstrating the robot walking, so the robot starts walking when starting
the simulation. It should be removed these codes from the scene before program
to control the NAO robot:

from the toolbox `[Scene hierarchy]\ NAO\ JointRecorder`, select the sub-menu
(right click) `Edit\ Delete selected objects`

#### Enabling the remote API (client side)

copy files `vrep.py, vrepConst.py` from `[V-REP's installation directory]/programming/remoteApiBindings/python`,
and file `remoteApi.dll (windows), or remoteApi.dylib (linux) or remoteApi.so (macos)`
from `[V-REP's installation directory]/programming/remoteApiBindings/lib/lib/<PLATFORM, ARCH>/`
to your programming folder
(see <http://www.coppeliarobotics.com/helpFiles/en/remoteApiClientSide.htm>)

#### References

V-REP API framework <http://www.coppeliarobotics.com/helpFiles/en/apisOverview.htm>
