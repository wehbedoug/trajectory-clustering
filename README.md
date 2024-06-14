# Trajectory Clustering Demo

This repository demonstrates techniques for clustering simulation trajectories.

The trajectories in this example come from the "NAV30" navigation benchmark
(TODO: cite). Each trajectory starts in a grid cell at the top-left, and ends in
a grid cell at the bottom-right. No two trajectories follow the same sequence of
grid cells. Furthermore, the trajectories may have differing lengths (i.e.
unequal amounts of data points), which can make clustering by mean squared error
and other metrics difficult.

We consider several distance metrics for trajectory clustering. These metrics
are capable of comparing the similarity of two trajectories even when their
lengths differ.

TODO: Explain each metric.




## Setup

TODO: Conda, requirements, etc.




## Configuration

`main.py` contains several global constants at the top of the file that control
the input data, output location and file type, and plotting options. There is
also a constant that allows you to choose the amounts of clusters to consider.

In `analyzer.py`, the function `_choose_group_to_split` contains a choice of
which group of trajectories to split. By default, we split the group with the
largest intra-group distance; that is, the group containing the two most
"dissimilar" trajectories, according to the specified metric of similarity. If
desired, we can simply split the group with the most trajectories; this is
faster to compute, but may not be the "right" choice for trajectory clustering.




## Example

Ensure your conda environment is set up according to the instructions above.
Then, run the example with the following command:

```bash
python main.py
```

If `SHOW_PLOT` is enabled, an interactive figure will be displayed for each
set of clustered trajectories.

If `SAVE_PLOT` is enabled, an image file will be created for each set of
clustered trajectories. You can configure the output directory and image file
type in `main.py`.
