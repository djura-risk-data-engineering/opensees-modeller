import openseespy.opensees as ops

from .foundations import add_foundations
from .floors import add_floors
from .joints import add_joints
from .beams import add_beams
from .columns import add_columns
from .infills import add_infills
from .gravity import do_gravity


def build_model(infills=True) -> None:
    """Adds the numerical model to the OpenSees domain.
    """
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    # Rigid-like material
    ops.uniaxialMaterial('Elastic', 99999, 1000000000.0)

    # Define components of foundations
    add_foundations()
    # Define components of joints
    add_joints()
    # Define components of floors
    add_floors()
    # Define components of beams
    add_beams()
    # Define components of columns
    add_columns()
    # Perform static analysis under gravity loads
    do_gravity()
    # Define components of infills (after gravity, unstressed)
    if infills:
        add_infills()
