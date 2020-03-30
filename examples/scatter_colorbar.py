"""An example of the colorbar display on the scatter plot."""
import ternary
import matplotlib.pyplot as plt


def _en_to_enth(energy, concs, A, B, C):
    """Converts an energy to an enthalpy.

    Converts energy to enthalpy using the following formula:
    Enthalpy = energy - (energy contribution from A) - (energy contribution from B) -
        (energy contribution from C)
    An absolute value is taken afterward for convenience.
    
    Parameters
    ----------
    energy : float
        The energy of the structure
    concs : list of floats
        The concentrations of each element
    A : float
        The energy of pure A
    B : float
        The energy of pure B
    C : float
        The energy of pure C

    Returns
    -------
    enth : float
       The enthalpy of formation.
    """

    enth = abs(energy - concs[0]*A - concs[1] * B - concs[2] * C)
    return enth


def _energy_to_enthalpy(energy):
    """Converts energy to enthalpy.
    
    This function take the energies stored in the energy array and
    converts them to formation enthalpy.

    Parameters
    ---------
    energy : list of lists of floats
    
    Returns
    -------
    enthalpy : list of lists containing the enthalpies.
    """
    
    pureA = [energy[0][0], energy[0][1]]
    pureB = [energy[1][0], energy[1][1]]
    pureC = [energy[2][0], energy[2][1]]

    enthalpy = []
    for en in energy:
        c = en[2]
        conc = [float(i) / sum(c) for i in c]

        CE = _en_to_enth(en[0], conc, pureA[0], pureB[0], pureC[0])
        VASP = _en_to_enth(en[1], conc, pureA[1], pureB[1], pureC[1])

        enthalpy.append([CE, VASP, c])

    return enthalpy


def _find_error(vals):
    """Find the errors in the energy values.

    This function finds the errors in the enthalpys.

    Parameters
    ----------
    vals : list of lists of floats

    Returns
    -------
    err_vals : list of lists containing the errors.
    """

    err_vals = []
    for en in vals:
        c = en[2]
        conc = [float(i) / sum(c) for i in c]

        err = abs(en[0] - en[1])

        err_vals.append([conc, err])

    return err_vals


def _read_data(fname):
    """Reads data from file.

    Reads the data in 'fname' into a list where each list entry contains 
    [energy predicted, energy calculated, list of concentrations].

    Parameters
    ----------
    fname : str
        The name and path to the data file.
    
    Returns
    -------
    energy : list of lists of floats
       A list of the energies and the concentrations.
    """
    
    energy = []
    with open(fname,'r') as f:
        for line in f:
            CE = abs(float(line.strip().split()[0]))
            VASP = abs(float(line.strip().split()[1]))
            conc = [i for i in line.strip().split()[2:]]

            conc_f = []
            for c in conc:
                if '[' in c and ']' in c:
                    conc_f.append(int(c[1:-1]))
                elif '[' in c:
                    conc_f.append(int(c[1:-1]))
                elif ']' in c or ',' in c:
                    conc_f.append(int(c[:-1]))
                else:
                    conc_f.append(int(c))
            energy.append([CE, VASP, conc_f])
    return energy


def conc_err_plot(fname):
    """Plots the error in the CE data.
    
    This plots the error in the CE predictions within a ternary concentration diagram.

    Parameters
    ----------
    fname : string containing the input file name.
    """

    energies = _read_data(fname)
    enthalpy = _energy_to_enthalpy(energies)
    this_errors = _find_error(enthalpy)

    points = []
    colors = []
    for er in this_errors:
        concs = er[0]
        points.append((concs[0] * 100, concs[1] * 100, concs[2] * 100))
        colors.append(er[1])
    
    scale = 100
    figure, tax = ternary.figure(scale=scale)
    tax.boundary(linewidth=1.0)
    tax.set_title("Errors in Convex Hull Predictions.", fontsize=20)
    tax.gridlines(multiple=10, color="blue")
    tax.scatter(points, vmax=max(colors), colormap=plt.cm.viridis, colorbar=True, c=colors, cmap=plt.cm.viridis)

    tax.show()


if __name__ == "__main__":
    conc_err_plot('sample_data/scatter_colorbar.txt')
