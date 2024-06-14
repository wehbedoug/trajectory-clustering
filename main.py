import pickle
import pathlib

import analyzer
import plotter
import sim_trace

# Settings
DATA_DIR = "data"
DATA_FILE = "small"

SAVE_PLOTS = True
PLOTS_DIR = "outputs"
PLOTS_FILE_EXT = "png"
SHOW_PLOTS = False

NUM_CLUSTERS = [2, 4, 6]

def main():
    print("Loading...", flush=True)

    # We expect the pickle file to contain a list of 2-D numpy arrays.
    results_filename = f'{DATA_DIR}/{DATA_FILE}.pickle'
    infile = open(results_filename, 'rb')
    arrs = pickle.load(infile)
    infile.close()

    alyzer = analyzer.SimulationAnalyzer()

    # Convert each numpy array to a SimulationTrace object. This is necessary
    # so that two traces can be easily compared by reference equality, rather
    # than element-wise floating point value equality. It is also more similar
    # to the actual hybridpy NAV simulator outputs, which are complex objects.
    traces = []
    for arr in arrs:
        traces.append(sim_trace.SimulationTrace(arr))
    print(f"{len(traces)} traces, average length {round(sum([len(t.pts) for t in traces]) / len(traces), 1)} (min={min([len(t.pts) for t in traces])}, max={max([len(t.pts) for t in traces])})")

    pathlib.Path(PLOTS_DIR).mkdir(exist_ok=True)

    for metric in [
            "hausdorff",
            "average",
            "area",
            "frechet",
            #"lcss", "edit_distance",  #  NAV-specific, string-based mode sequence distance metrics;
                                       #  requires installation of hyst, hybridpy, hylaa, etc.
        ]:
        alyzer.set_distance_metric(metric)
        print(f"Splitting by {metric}...", flush=True)

        for num_groups in NUM_CLUSTERS:
            print(f"num_groups={num_groups}...")
            groups = alyzer.split_traces_into_N_groups(traces, num_groups)
            plotter.plot_traces_groups(
                groups,
                save=SAVE_PLOTS,
                show=SHOW_PLOTS,
                file_prefix=f"{PLOTS_DIR}/{DATA_FILE}",
                file_suffix=f"{num_groups}_{metric}",
                file_ext=PLOTS_FILE_EXT,
            )

if __name__ == "__main__":
    main()
