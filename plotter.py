import numpy as np
import matplotlib.pyplot as plt

import sim_trace


def plot_traces_groups(traces_groups, save=True, show=False, file_prefix="", file_suffix="", file_ext="png"):
    # Add gridlines
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlabel("x Position")
    plt.ylabel("y Position")
    major_ticks = np.arange(0, 100, 1)
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.grid(which='both')
    plt.gca().set_aspect('equal')

    all_colors = ['red', 'blue', 'lime', 'orange', 'magenta', 'cyan', 'green', 'grey', 'darkkhaki', 'silver', 'darkgrey', 'mediumslateblue', 'limegreen', 'palegreen', 'sienna', 'peachpuff', 'saddlebrown', 'cadetblue', 'cornflowerblue', 'indigo', 'palevioletred', 'lightslategray', 'salmon', 'fuchsia', 'pink', 'darkolivegreen', 'navy', 'hotpink', 'darksalmon', 'lightblue', 'crimson', 'aquamarine', 'goldenrod', 'olivedrab', 'gainsboro', 'sandybrown', 'mediumvioletred', 'powderblue', 'gray', 'tan', 'lightseagreen', 'khaki', 'deepskyblue', 'mediumaquamarine', 'springgreen', 'coral', 'darkturquoise', 'darkgreen', 'slategrey', 'rebeccapurple', 'thistle', 'darkviolet', 'darkgoldenrod', 'blanchedalmond', 'orangered', 'purple', 'mediumturquoise', 'darkgray', 'turquoise', 'mediumblue', 'lawngreen', 'darkseagreen', 'darkred', 'darkmagenta', 'brown', 'firebrick', 'darkslateblue', 'palegoldenrod', 'lightgreen', 'steelblue', 'chartreuse', 'aqua', 'midnightblue', 'blueviolet', 'tomato', 'lightsalmon', 'slateblue', 'lightslategrey', 'darkorange', 'mediumspringgreen', 'mediumpurple', 'dodgerblue', 'lavender', 'skyblue', 'wheat', 'lightsteelblue', 'lightcoral', 'forestgreen', 'moccasin', 'burlywood', 'orchid', 'violet', 'dimgrey', 'darkcyan', 'mediumorchid', 'olive', 'lightskyblue', 'darkslategray', 'plum', 'mediumseagreen', 'chocolate', 'paleturquoise', 'seagreen', 'deeppink', 'darkblue', 'lightgrey', 'darkorchid', 'maroon', 'gold', 'lightcyan', 'dimgray', 'rosybrown', 'peru', 'slategray', 'indianred', 'lightgray', 'lightpink', 'teal', 'darkslategrey', 'bisque', 'royalblue', 'papayawhip']

    for group, color in zip(traces_groups, all_colors):
        for trace in group:
            assert isinstance(trace, sim_trace.SimulationTrace)
            pts = trace.pts
            plt.plot(pts[:, 0], pts[:, 1], color=color, alpha=0.7, linewidth=1.0)

    if save:
        print(f"Saving plot in {file_prefix}_{file_suffix}.{file_ext}")
        plt.savefig(f"{file_prefix}_{file_suffix}.{file_ext}")
    if show:
        plt.show()
    plt.close()
