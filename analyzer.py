import similaritymeasures
import scipy

import sim_trace

# NAV-specific, string-based mode sequence distance metrics;
# requires installation of hyst, hybridpy, hylaa, etc.
"""
import edit_distance
import difflib
"""

class SimulationAnalyzer:
    def __init__(self, distance_metric="average"):
        self.distance_metric = distance_metric

    def set_distance_metric(self, distance_metric):
        self.distance_metric = distance_metric

    def extract_2d_pts_from_trace(self, trace):
        assert isinstance(trace, sim_trace.SimulationTrace)
        return trace.pts

    def _distances_trace1_pts_to_trace2(self, trace1, trace2):
        '''
        For each point in trace1, get the minimum distance to trace2
        '''
        trace1_arr = self.extract_2d_pts_from_trace(trace1)
        trace2_arr = self.extract_2d_pts_from_trace(trace2)

        distances = []
        for pt in trace1_arr:
            dist = scipy.spatial.distance.cdist([pt], trace2_arr, metric='euclidean').min()
            distances.append(dist)

        return distances

    def _average_distance_between_traces(self, trace1, trace2):
        distances_1_to_2 = self._distances_trace1_pts_to_trace2(trace1, trace2)
        distances_2_to_1 = self._distances_trace1_pts_to_trace2(trace2, trace1)

        avg_1_to_2 = sum(distances_1_to_2) / len(distances_1_to_2)
        avg_2_to_1 = sum(distances_2_to_1) / len(distances_2_to_1)

        return (avg_1_to_2 + avg_2_to_1) / 2

    def _max_distance_between_traces(self, trace1, trace2):
        distances_1_to_2 = self._distances_trace1_pts_to_trace2(trace1, trace2)
        distances_2_to_1 = self._distances_trace1_pts_to_trace2(trace2, trace1)
        return max([max(distances_1_to_2), max(distances_2_to_1)])

    def _hausdorff_distance_between_traces(self, trace1, trace2):
        '''
        This is the exact same as _max_distance_between_traces.
        '''
        trace1_arr = self.extract_2d_pts_from_trace(trace1)
        trace2_arr = self.extract_2d_pts_from_trace(trace2)

        # Directed Hausdorff distance is not symmetric. See scipy documentation,
        # as well as Equations (1) and (2) in
        #       A. A. Taha and A. Hanbury, "An efficient algorithm for calculating the exact Hausdorff distance."
        #       IEEE Transactions On Pattern Analysis And Machine Intelligence, vol. 37 pp. 2153-63, 2015.
        #       https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7053955
        hausdorff_1_to_2 = scipy.spatial.distance.directed_hausdorff(trace1_arr, trace2_arr)
        hausdorff_2_to_1 = scipy.spatial.distance.directed_hausdorff(trace2_arr, trace1_arr)
        ret_val = max(hausdorff_1_to_2[0], hausdorff_2_to_1[0])

        return ret_val

    def _area_between_traces(self, trace1, trace2):
        trace1_arr = self.extract_2d_pts_from_trace(trace1)
        trace2_arr = self.extract_2d_pts_from_trace(trace2)

        ret_val = similaritymeasures.area_between_two_curves(trace1_arr, trace2_arr)
        return ret_val

    def _frechet_distance_between_traces(self, trace1, trace2):
        trace1_arr = self.extract_2d_pts_from_trace(trace1)
        trace2_arr = self.extract_2d_pts_from_trace(trace2)

        ret_val = similaritymeasures.frechet_dist(trace1_arr, trace2_arr)
        return ret_val

    def _lcss(self, lst1, lst2):
        """
        Finds the longest common subsequence among two lists of strings.

        Params:
            lst1 - list of strings
            lst2 - list of strings
        Returns:
            a tuple (int, list(str)) of the length and elements of the longest subsequence
        """
        matcher = difflib.SequenceMatcher(None, lst1, lst2, autojunk=False)
        lcss = []
        for block in matcher.get_matching_blocks():
            matching_subseq = lst1[block.a : (block.a + block.size)]
            lcss += matching_subseq

        return len(lcss), lcss

    def _lcss_distance_between_traces(self, trace1, trace2):
        """
        NOTE: Not technically a valid distance metric. Distance between a trace
        and itself will not be zero.
        """
        seq1 = ModeSeqData.get_mode_seq_from_trace(trace1).split(',')
        seq2 = ModeSeqData.get_mode_seq_from_trace(trace2).split(',')

        length, subseq = self._lcss(seq1, seq2)

        # Distance should decrease for similar traces.
        ret_val = 2
        if length != 0:
            ret_val = 1 / length
        return ret_val

    def calculate_distance_between_traces(self, trace1, trace2):
        if self.distance_metric == "average":
            return self._average_distance_between_traces(trace1, trace2)
        elif self.distance_metric == "edit_distance":
            return self._edit_distance_between_traces(trace1, trace2)
        elif self.distance_metric == "maximum":
            return self._max_distance_between_traces(trace1, trace2)
        elif self.distance_metric == "hausdorff":
            return self._hausdorff_distance_between_traces(trace1, trace2)
        elif self.distance_metric == "area":
            return self._area_between_traces(trace1, trace2)
        elif self.distance_metric == "frechet":
            return self._frechet_distance_between_traces(trace1, trace2)
        elif self.distance_metric == "lcss":
            return self._lcss_distance_between_traces(trace1, trace2)
        else:
            raise ValueError(f"Unknown distance metric: {self.distance_metric}")

    def find_most_distant_trace(self, nominal_trace, traces):
        largest_distance = 0
        most_distant_trace = nominal_trace
        for t in traces:
            distance = self.calculate_distance_between_traces(nominal_trace, t)
            if distance > largest_distance and t != nominal_trace:
                most_distant_trace = t
                largest_distance = distance

        return most_distant_trace

    def _split_traces_group(self, list_of_traces):
        if len(list_of_traces) <= 1:
            raise ValueError("Cannot split group of fewer than two traces.")

        trace1 = list_of_traces[0]
        trace2 = self.find_most_distant_trace(trace1, list_of_traces)

        # Ensure that each list has at least one trace, but do not double-count
        # the nominal traces.
        out1 = [trace1]
        out2 = [trace2]
        traces_copy = [t for t in list_of_traces]
        traces_copy.remove(trace1)
        traces_copy.remove(trace2)

        for t in traces_copy:
            diff1 = self.calculate_distance_between_traces(trace1, t)
            diff2 = self.calculate_distance_between_traces(trace2, t)
            if diff1 < diff2:
                out1.append(t)
            else:
                out2.append(t)

        assert(len(out1) + len(out2) == len(list_of_traces))
        assert(len(out1) > 0)
        assert(len(out2) > 0)
        return out1, out2

    def _find_largest_group(self, traces_groups):
        ret_val = (0, traces_groups[0])
        for i, group in enumerate(traces_groups):
            if len(group) > len(group):
                ret_val = (i, group)
        return ret_val

    def _get_average_distance(self, traces):
        diffs = []
        for t1 in traces:
            t2 = self.find_most_distant_trace(t1, traces)
            diff = self.calculate_distance_between_traces(t1, t2)
            diffs.append(diff)
        return sum(diffs) / len(diffs)

    def _get_max_distance(self, traces):
        diffs = []
        for t1 in traces:
            t2 = self.find_most_distant_trace(t1, traces)
            diff = self.calculate_distance_between_traces(t1, t2)
            diffs.append(diff)
        return max(diffs)

    def _find_group_with_largest_intragroup_distance(self, traces_groups):
        ret_val = (0, traces_groups[0])
        highest = 0
        for idx, group in enumerate(traces_groups):
            max_intragroup_distance = self._get_max_distance(group)
            if max_intragroup_distance > highest:
                highest = max_intragroup_distance
                ret_val = (idx, group)
        return ret_val

    def _choose_group_to_split(self, traces_groups):
        #return self._find_largest_group(traces_groups)
        return self._find_group_with_largest_intragroup_distance(traces_groups)

    def split_traces_into_N_groups(self, traces, N):
        traces_groups = [traces]
        idx, grp = (0, traces_groups[0])

        while len(traces_groups) < N and len(grp) > 1:
            traces_groups.pop(idx)
            new1, new2 = self._split_traces_group(grp)
            traces_groups.append(new1)
            traces_groups.append(new2)
            idx, grp = self._choose_group_to_split(traces_groups)
        return traces_groups

    def _get_init_point_from_repr_trace(self, trace):
        # Return point(4D)
        return trace['traces'][0].points[0]

    def _edit_distance_between_traces(self, trace1, trace2):
        seq1 = ModeSeqData.get_mode_seq_from_trace(trace1).split(',')
        seq2 = ModeSeqData.get_mode_seq_from_trace(trace2).split(',')

        remove_repeats = True
        sort_modes = False

        if remove_repeats:
            seq1 = list(set(seq1))
            seq2 = list(set(seq2))
        if sort_modes:
            seq1.sort()
            seq2.sort()

        seq_matcher = edit_distance.SequenceMatcher(seq1, seq2)

        #return 1 / (seq_matcher.ratio() + 0.001)
        return seq_matcher.distance()
