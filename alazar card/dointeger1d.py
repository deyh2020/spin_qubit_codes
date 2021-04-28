# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:00:35 2021

@author: T7-2
"""
from contextlib import contextmanager
from typing import Callable, Sequence, Union, Tuple, List, Optional, Iterator
import os
import time

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from qcodes.dataset.measurements import Measurement, res_type, DataSaver
from qcodes.instrument.base import _BaseParameter
from qcodes.dataset.plotting import plot_by_id
from qcodes import config
ActionsT = Sequence[Callable[[], None]]

ParamMeasT = Union[_BaseParameter, Callable[[], None]]

AxesTuple = Tuple[matplotlib.axes.Axes, matplotlib.colorbar.Colorbar]
AxesTupleList = Tuple[List[matplotlib.axes.Axes],
                      List[Optional[matplotlib.colorbar.Colorbar]]]
AxesTupleListWithRunId = Tuple[int, List[matplotlib.axes.Axes],
                      List[Optional[matplotlib.colorbar.Colorbar]]]


def _process_params_meas(param_meas: ParamMeasT) -> List[res_type]:
    output = []
    for parameter in param_meas:
        if isinstance(parameter, _BaseParameter):
            output.append((parameter, parameter.get()))
        elif callable(parameter):
            parameter()
    return output


def _register_parameters(
        meas: Measurement,
        param_meas: List[ParamMeasT],
        setpoints: Optional[List[_BaseParameter]] = None
) -> None:
    for parameter in param_meas:
        if isinstance(parameter, _BaseParameter):
            meas.register_parameter(parameter,
                                    setpoints=setpoints)


def _register_actions(
        meas: Measurement,
        enter_actions: ActionsT,
        exit_actions: ActionsT
) -> None:
    for action in enter_actions:
        # this omits the possibility of passing
        # argument to enter and exit actions.
        # Do we want that?
        meas.add_before_run(action, ())
    for action in exit_actions:
        meas.add_after_run(action, ())



def _set_write_period(
        meas: Measurement,
        write_period: Optional[float] = None
) -> None:
    if write_period is not None:
        meas.write_period = write_period


@contextmanager
def _catch_keyboard_interrupts() -> Iterator[Callable[[], bool]]:
    interrupted = False
    def has_been_interrupted():
        nonlocal interrupted
        return interrupted
    try:
        yield has_been_interrupted
    except KeyboardInterrupt:
        interrupted = True
def _handle_plotting(
        datasaver: DataSaver,
        do_plot: bool = True,
        interrupted: bool = False
) -> AxesTupleList:
    """
    Save the plots created by datasaver as pdf and png

    Args:
        datasaver: a measurement datasaver that contains a dataset to be saved
            as plot.
            :param do_plot:

    """
    dataid = datasaver.run_id
    if do_plot == True:
        res = _create_plots(datasaver)
    else:
        res = dataid, None, None

    if interrupted:
        raise KeyboardInterrupt

    return res
def _create_plots(datasaver: DataSaver) -> AxesTupleList:
    dataid = datasaver.run_id
    plt.ioff()
    start = time.time()
    axes, cbs = plot_by_id(dataid)
    stop = time.time()
    print(f"plot by id took {stop - start}")
    mainfolder = config.user.mainfolder
    experiment_name = datasaver._dataset.exp_name
    sample_name = datasaver._dataset.sample_name
    storage_dir = os.path.join(mainfolder, experiment_name, sample_name)
    os.makedirs(storage_dir, exist_ok=True)
    png_dir = os.path.join(storage_dir, 'png')
    pdf_dif = os.path.join(storage_dir, 'pdf')
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(pdf_dif, exist_ok=True)
    save_pdf = True
    save_png = True
    for i, ax in enumerate(axes):
        if save_pdf:
            full_path = os.path.join(pdf_dif, f'{dataid}_{i}.pdf')
            ax.figure.savefig(full_path, dpi=500)
        if save_png:
            full_path = os.path.join(png_dir, f'{dataid}_{i}.png')
            ax.figure.savefig(full_path, dpi=500)
    plt.ion()
    res = dataid, axes, cbs
    return res
def dointeger1d(
    param_set: _BaseParameter, start: float, stop: float,
    num_points: int, delay: float,
    *param_meas: ParamMeasT,
    enter_actions: ActionsT = (),
    exit_actions: ActionsT = (),
    write_period: Optional[float] = None,
    do_plot: bool = True
) -> AxesTupleListWithRunId:
    """
    Perform a 1D scan of ``param_set`` from ``start`` to ``stop`` in
    ``num_points`` measuring param_meas at each step. In case param_meas is
    an ArrayParameter this is effectively a 2d scan.

    Args:
        param_set: The QCoDeS parameter to sweep over
        start: Starting point of sweep
        stop: End point of sweep
        num_points: Number of points in sweep
        delay: Delay after setting paramter before measurement is performed
        *param_meas: Parameter(s) to measure at each step or functions that
          will be called at each step. The function should take no arguments.
          The parameters and functions are called in the order they are
          supplied.
        enter_actions: A list of functions taking no arguments that will be
            called before the measurements start
        exit_actions: A list of functions taking no arguments that will be
            called after the measurements ends
        do_plot: should png and pdf versions of the images be saved after the
            run.

    Returns:
        The run_id of the DataSet created
    """
    meas = Measurement()
    _register_parameters(meas, (param_set,))
    _register_parameters(meas, param_meas, setpoints=(param_set,))
    _set_write_period(meas, write_period)
    _register_actions(meas, enter_actions, exit_actions)
    param_set.post_delay = delay

    # do1D enforces a simple relationship between measured parameters
    # and set parameters. For anything more complicated this should be
    # reimplemented from scratch
    with _catch_keyboard_interrupts() as interrupted, meas.run() as datasaver:
        for set_point in [2**i for i in range(start,stop,num_points)]:
           #         for set_point in np.linspace(start, stop, num_points):
            param_set.set(set_point)
            Alazar.sync_settings_to_card()
            ChannelC.prepare_channel()
            AWG_CPH.ch1_state(1)
            AWG_CPH.ch2_state(1)
            datasaver.add_result((param_set, set_point),
                                  *_process_params_meas(param_meas))
            AWG_CPH.ch1_state(0)
            AWG_CPH.ch2_state(0)
    return _handle_plotting(datasaver, do_plot, interrupted())
